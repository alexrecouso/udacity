import sys
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#dunderscore name creates an app named after the name of our file
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://alexrecouso@localhost:5432/todoappajax'
#this connects to the db, although you need to manually create it
db = SQLAlchemy(app)

class Todo(db.Model): #creates the table that will store the todo items
    __tablename__= 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id}: {self.description}>'

db.create_all() #creates the tables

@app.route('/todos/create', methods=['POST'])
#'/' is the index route
def create():
    error=False
    body = {}
    try:
        descript = request.form.get_json()['description'] #this will come back as a dictionary with key 'description'
        todo = Todo(description=descript)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
        #now we have to redirect to the index so it queries Todo table and renders html again
    except:
        error = True
        db.session.rollback()
        print(system.exec_info())
    finally:
        db.session.close() #SHOULD BE CALLED BEFORE RETURN STATEMENT
    if error:
        abort(400)
    else:
        return jsonify(body)
         #will return json data to the client based on whatever we pass in as a json object

@app.route('/')
def index():
    #this index method is the controller in the MVC Model
    #tells what the user will be view next - do a select on the database and use index.html to know how to show that data
    return render_template('index.html', data=Todo.query.all())
    #method render_template allows us to render an html
    #by default looks for it on a folder called 'templates' on the same directory
    #we can pass a variable called data which could be a list (i.e. a query)
    #we insert a jinja for loop on the index.html file
