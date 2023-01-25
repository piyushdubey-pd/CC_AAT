from flask import Flask, render_template, request, redirect,url_for
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from bson.errors import InvalidId


client = MongoClient("mongodb+srv://piyushd:CCAATFLASK@cluster0.mmecdla.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.ccaat

# <-- DEMO insert into database -->
# db.items.insert_one({
#     "title":"Do dishes",
#     "urgen": 3,
#     "completed" : False,
#     "description" : "all the dishes are to be done before night"
# })

app = Flask(__name__)
title = "TODO List"
heading = "ToDoRem"

def redirect_url():
    return request.args.get('next') or \
        request.referrer or \
            url_for('index')

@app.route("/list")
def lists ():
	#Display the all Tasks
	todos_l = db.items.find()
	a1="active"
	return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route("/")
@app.route("/uncompleted")
def tasks ():
	#Display the Uncompleted Tasks
	todos_l = db.items.find({"done":"no"})
	a2="active"
	return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading)


@app.route("/completed")
def completed ():
	#Display the Completed Tasks
	todos_l = db.items.find({"done":"yes"})
	a3="active"
	return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading)

@app.route("/done")
def done ():
	#Done-or-not ICON
	id=request.values.get("_id")
	task=db.items.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		db.items.update_one({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		db.items.update_one({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	redir=redirect_url()	# Re-directed URL i.e. PREVIOUS URL from where it came into this one

#	if(str(redir)=="http://localhost:5000/search"):
#		redir+="?key="+id+"&refer="+refer

	return redirect(redir)

#@app.route("/add")
#def add():
#	return render_template('add.html',h=heading,t=title)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	db.items.insert_one({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
	return redirect("/list")

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	db.items.delete_one({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=db.items.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	id=request.values.get("_id")
	db.items.update_one({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})
	return redirect("/")

@app.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(refer=="id"):
		try:
			todos_l = db.items.find({refer:ObjectId(key)})
			if not todos_l:
				return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading,error="No such ObjectId is present")
		except InvalidId as err:
			pass
			return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading,error="Invalid ObjectId format given")
	else:
		todos_l = db.items.find({refer:key})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

@app.route("/about")
def about():
	return render_template('credits.html',t=title,h=heading)

if __name__ == "__main__":
	app.run(host="0.0.0.0")
	
	
	
	
	# env = os.environ.get('FLASK_ENV', 'development')
	# port = int(os.environ.get('PORT', 5000))
	# debug = False if env == 'production' else True
	# app.run(debug=True)
	# app.run(port=port, debug=debug)

# client.close()

#set FLASK_APP=app.py
#flask run