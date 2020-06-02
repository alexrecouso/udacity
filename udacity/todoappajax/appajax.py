import sys
from flask import Flask, render_template, jsonify, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
#dunderscore name creates an app named after the name of our file
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://alexrecouso@localhost:5432/todoapp'
#this connects to the db, although you need to manually create it
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Todo(db.Model): #creates the table that will store the todo items
    __tablename__= 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo {self.id}: {self.description}>'

#db.create_all() #creates the tables
#since we are using migrations we dont need the above line

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed #coming from our ajax request
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todo/create', methods=['POST'])
#'/' is the index route
def create():
    error = False
    try:
        descript = request.form.get('description', '') #2nd is a default empty string in case nothing comes in
        todo = Todo(description=descript)
        db.session.add(todo)
        db.session.commit()
    except:
        db.session.rollback() #avoid potential implicit commits done by the database on closing a connection
        error=True
        print(sys.exec_info()) #need to import sys module
    finally:
        db.session.close() #Good practice is to close connections at the end of every session used in a controller, to return the connection back to the connection pool
    #now we have to redirect to the index so it queries Todo table and renders html again
    if error:
        abort(400)
    else:
        return redirect(url_for('index'))

@app.route('/')
def index():
    #this index method is the controller in the MVC Model
    #tells what the user will be view next - do a select on the database and use index.html to know how to show that data
    return render_template('index.html', data=Todo.query.order_by('id').all())
    #method render_template allows us to render an html
    #by default looks for it on a folder called 'templates' on the same directory
    #we can pass a variable called data which could be a list (i.e. a query)
    #we insert a jinja for loop on the index.html file
