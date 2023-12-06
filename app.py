from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import timezone, datetime

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.flask_db
todos = db.todos


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        content = request.form['content']
        priority = request.form['priority']
        todos.insert_one({'content': content, 'priority': priority, 'complete': False, 'date': datetime.now(timezone.utc)})
        return redirect(url_for('index'))

    all_todos = todos.find().collation({'locale': 'en'}).sort('content')
    return render_template('index.html', todos=all_todos) 

@app.route('/<id>/complete/', methods=['POST'])
def complete(id):
    completion = request.form['completion']
    new_completion = False if completion == 'true' else True
    todos.update_one({"_id": ObjectId(id)}, {"$set": {"complete": new_completion}})
    return redirect(url_for('index'))

@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))