import datetime
import time
from flask import Flask
from flask import request
from flask import render_template
from notmuch import Database
from notmuch import Query

app = Flask(__name__)
app.debug = True 
db = Database()

@app.route("/")
def index():
    db = Database()
    msgs = Query(db, 'inbox').search_messages()
    return render_template('index.html',msgs=list(msgs)[:100])

@app.route("/search",methods=['GET','POST'])
def search():
    if request.method == 'POST':
        msgs = list(Query(db, request.form.get('search')).search_messages())
    else:
        msgs = list(Query(db, request.args.get('q')).search_messages())
    return render_template('index.html',msgs=list(msgs)[:100])

@app.route("/dateSearch",methods=['GET','POST'])
def datesearch():
    if request.method == 'POST':
        tTo = datetime.datetime.strptime(request.form.get('to'), "%d %B, %Y").timetuple()
        tFrom = datetime.datetime.strptime(request.form.get('from'), "%d %B, %Y").timetuple()
        #to=int(time.mktime(tTo)),from=int(time.mktime(tFrom))
        msgs = list(Query(db,'%i..%i'%(int(time.mktime(tFrom)),int(time.mktime(tTo))) ).search_messages())
        return render_template('dateSearch.html',msgs=msgs)
        #msgs = list(Query(db, request.form.get('search')).search_messages())

    return render_template('dateSearch.html')


@app.route("/message/<messageid>")
def viewmessage(messageid):
    msgs = list(Query(db, 'id:%s'%messageid).search_messages())
    msgParts = list(msgs[0].get_message_parts())
    mail = msgParts[0].as_string()
    return render_template('index.html',msgs=list(msgs)[:100],view=True,mail=mail)


if __name__ == "__main__":
    app.run('0.0.0.0',8000)
