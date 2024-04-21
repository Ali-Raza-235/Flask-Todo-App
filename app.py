from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"


db = SQLAlchemy(app=app)

class Todo(db.Model):
    __tablename__ = 'todo'  # This should match the actual table name in your database
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

 

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        todo_title = request.form['title']
        todo_desc = request.form['desc']
    # with app.app_context():
    #     db.create_all()
        data = Todo(title=todo_title, desc=todo_desc)
        db.session.add(data)
        db.session.commit()

    alltodo = Todo.query.all()

    return render_template('index.html', alltodo = alltodo)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        todo_title = request.form['title']
        todo_desc = request.form['desc']
        data = Todo.query.filter_by(sno=sno).first()
        data.title = todo_title
        data.desc = todo_desc
        db.session.add(data)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
