from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
import re
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from echomodel import EchoModel  # Import your custom model class

app = Flask(__name__)
CORS(app)
app.secret_key = 'xyzsdfg'

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site1.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define an abstract class for language models
class LanguageModel:
    def predict(self, user_input):
        pass

# Define the OpenAI language model class
class OpenAILanguageModel(LanguageModel):
    def __init__(self, api_key):
        self.llm = OpenAI(openai_api_key=api_key)

    def predict(self, user_input):
        return self.llm.predict(user_input)

# Define your custom language model class
class YourCustomLanguageModel(LanguageModel):
    def __init__(self, model_data):
        # Initialize your custom language model
        pass

    def predict(self, user_input):
        # Implement the prediction logic for your custom model
        pass

# Choose the language model you want to use (replace with your actual key or data)
# language_model = OpenAILanguageModel(api_key="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")
# Alternatively, use your custom language model
# language_model = YourCustomLanguageModel(model_data="your_model_data")
language_model = EchoModel()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    chats = db.relationship('Chats', backref='user', lazy=True)

class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    input_data = db.Column(db.Text, nullable=False)
    output_data = db.Column(db.Text, nullable=False)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('guest_action') == 'true':
            # User is logging in as a guest
            session['loggedin'] = True
            session['userid'] = -1
            session['name'] = 'Guest'
            session['email'] = 'guest@example.com'
            session['guest'] = True  # Set a session variable to identify the user as a guest

            return redirect(url_for('user'))

        elif 'email' in request.form and 'password' in request.form:
            # User is a registered user, proceed with the existing logic
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()

            if user:
                if user.password == password:
                    session['loggedin'] = True
                    session['userid'] = user.id
                    session['name'] = user.name
                    session['email'] = user.email
                    return redirect(url_for('user'))
                else:
                    flash('Incorrect password. Please try again.', 'error')
            else:
                flash('User not found. Please register or check your email.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        user_name = request.form['name']
        password = request.form['password']
        email = request.form['email']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Account already exists! Please log in.', 'error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address! Please enter a valid email.', 'error')
        elif not user_name or not password or not email:
            flash('Please fill out the form completely.', 'error')
        else:
            new_user = User(name=user_name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    flash('Successfully logged out', 'success')
    return redirect(url_for('login'))

@app.route('/user')
def user():
    user_id = session.get('userid')
    is_guest = session.get('guest')

    # Check if the user is logged in (either registered or guest)
    if user_id is not None:
        if user_id >= 0:
            # User is a registered user, retrieve user data
            user_data = User.query.filter_by(id=user_id).first()
            if user_data:
                conversations = user_data.chats
                return render_template('index.html', conversations=conversations, user=user_data, is_guest=False)
            else:
                flash('User data not found.', 'error')
        else:
            # User is a guest, handle guest logic
            return render_template('index.html', is_guest=True)
    else:
        flash('User not logged in. Please log in.', 'error')

    return redirect(url_for('login'))

# Define a route for handling POST requests containing user input
@app.route('/data', methods=['POST'])
def get_data():
    data = request.get_json()
    text = data.get('data')
    user_input = text

    try:
        # Use the selected language model to get a response
        output = language_model.predict(user_input)

        # Save the conversation data to the database if the user is a registered user
        user_id = session.get('userid')
        if user_id is not None and user_id >= 0:
            conversation_data = Chats(owner=user_id, input_data=user_input, output_data=output)
            db.session.add(conversation_data)
            db.session.commit()

        # Return the response in JSON format
        return jsonify({"response": True, "message": output})
    except Exception as e:
        app.logger.error(f'Error: {str(e)}')
        error_message = 'An error occurred while processing your request.'
        return jsonify({"message": error_message, "response": False})

if __name__ == "__main__":
    try:
        with app.app_context():
            print("Creating tables...")
            db.create_all()
            print("Tables created.")
    except Exception as e:
        print(f"An error occurred during table creation: {e}")

    app.run(debug=True)
