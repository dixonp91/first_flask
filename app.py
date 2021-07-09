from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#init database
db = SQLAlchemy(app)

#create db model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #create fuction to return a string
    def __repr__(self):
        return '<Name %r>' % self.id

subscribers = []

@app.route("/")
def index():
    
    return render_template('index.html')

@app.route("/about")
def about():
    names = ['jon', 'wes', 'brit', 'dan', 'cal', 'ash','elle']
    return render_template('about.html', names=names)

@app.route("/subscribe")
def subscribe():

    return render_template('subscribe.html')

@app.route("/form", methods=[ "POST"])
def form():
    first_name= request.form.get('first_name')
    last_name=request.form.get('last_name')
    email=request.form.get('email')

    subscribers.append(f"{first_name} {last_name} || {email}")

    return render_template('form.html', subscribers=subscribers)

@app.route("/friends", methods =['GET', 'POST'])
def friends():
    if request.method == "POST":
        friend_name = request.form['name']
        new_name = Friends(name=friend_name)

        #push to DB
        try:
            db.session.add(new_name)
            db.session.commit()
            return redirect('/friends')
        except:
            return "Error no new friends"

    else:
        friends = Friends.query.order_by(Friends.date_added)
        return render_template('friends.html', friends=friends)

@app.route("/update/<int:id>", methods = ['GET', 'POST'])
def update(id):
    friend_to_update = Friends.query.get_or_404(id)

    if request.method == 'POST':
        friend_to_update.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return 'Error no such friend'

    else:
        return render_template('update.html', friend_update = friend_to_update)

@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete = Friends.query.get_or_404(id)

    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        db.session.rollback()
        return "There was an error "