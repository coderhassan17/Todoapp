from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    s_no = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"{self.s_no}-{self.title}"

@app.route('/', methods=["GET", "POST"])
def main():
    alltodo = Todo.query.all()  

    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    return render_template("todo.html", alltodo=alltodo)        
@app.route('/update/<int:s_no>',methods=["GET", "POST"])
def update(s_no):
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(s_no=s_no).first() 
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(s_no=s_no).first() 
    return render_template("update.html", todo=todo)        
        
@app.route('/delete/<int:s_no>')
def delete(s_no):
    todo = Todo.query.filter_by(s_no=s_no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/complete/<int:s_no>', methods=["POST"])
def complete_task(s_no):
    todo = Todo.query.get_or_404(s_no)
    todo.completed = not todo.completed  # Toggle completion status
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.app_context().push()
    db.create_all()
    app.run(debug=True, host = "0.0.0.0")

