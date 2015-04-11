import os
from flask import *
from flask.ext.login import LoginManager
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class User():
	users = {}

	def __init__(self, username, password):
		self.username = username
		self.password = password
		User.users[username] = self

def getUser(username, password, add=False):
	if add:
		User.users[username] = User(username, password)
	this_user = User.users.get(username, None)
	if this_user is None:
		return None
	if this_user.password == password:
		return this_user
	return None

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = StringField('password', validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.user = None

	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False
		user = getUser(self.username.data, self.password.data)
		if user is None:
			return False
		self.user = user
		return True

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
'facebook': {
'id': '470154729788964',
'secret': '010cc08bd4f51e34f3f3e684fbdea8a7'
}
}
lm = LoginManager()
lm.init_app(app)

@app.route('/')
def home():
	return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		return redirect('/')
	return render_template('login.html', form=form)

if __name__ == '__main__':
	User('kbrady', 't')
	app.run(debug=True, host='0.0.0.0')
