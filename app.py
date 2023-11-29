from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
import uuid
import re
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from echomodel import EchoModel  # Import your custom model class

app = Flask(__name__)
CORS(app)
app.secret_key = 'xyzsdfg'

# Define the generate_unique_session_id function
def generate_unique_session_id():
    """
    Generate a unique session ID using UUID.

    Returns:
        str: A string representation of the unique session ID.
    """
    return str(uuid.uuid4())

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site1.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define an abstract class for language models
class LanguageModel:
    """An abstract class representing a language model."""
    def predict(self, user_input):
        """Make a prediction based on user input.

        Args:
            user_input (str): The input provided by the user.

        Returns:
            str: The model's prediction.
        """
        pass

# Define the OpenAI language model class
class OpenAILanguageModel(LanguageModel):
    """A class representing the OpenAI language model."""
    def __init__(self, api_key):
        """Initialize the OpenAI language model.

        Args:
            api_key (str): The API key for accessing the OpenAI language model.
        """
        self.llm = OpenAI(openai_api_key=api_key)

    def predict(self, user_input):
        """Make a prediction using the OpenAI language model.

        Args:
            user_input (str): The input provided by the user.

        Returns:
            str: The model's prediction.
        """
        return self.llm.predict(user_input)

# Define your custom language model class
class YourCustomLanguageModel(LanguageModel):
    """A class representing a custom language model."""
    def __init__(self, model_data):
        """Initialize the custom language model.

        Args:
            model_data (str): Data required for initializing the custom model.
        """
    def __init__(self, model_data):
        """Initialize the custom language model.

        Args:
            model_data (str): Data required for initializing the custom model.
        """
        # Initialize your custom language model
        pass

    def predict(self, user_input):
        """Make a prediction using the custom language model.

        Args:
            user_input (str): The input provided by the user.

        Returns:
            str: The model's prediction.
        """
        # Implement the prediction logic for your custom model
        pass

# Choose the language model you want to use (replace with your actual key or data)
# language_model = OpenAILanguageModel(api_key="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")
# Alternatively, use your custom language model
# language_model = YourCustomLanguageModel(model_data="your_model_data")
language_model = EchoModel()

class User(db.Model):
    """A class representing a user in the system."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    chats = db.relationship('Chats', backref='user', lazy=True)

class Chats(db.Model):
    """A class representing chat data."""
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    input_data = db.Column(db.Text, nullable=False)
    output_data = db.Column(db.Text, nullable=False)
    session_id = db.Column(db.String(50), nullable=True)  # Add session_id field

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login requests.

    Returns:
        Response: A response to the login request.
    """
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
    """Handle user registration requests.

    Returns:
        Response: A response to the registration request.
    """
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
    """Handle user logout requests.

    Returns:
        Response: A response to the logout request.
    """
    session_id = session.get('session_id')
    user_id = session.get('userid')

    # Print conversation data for the current session before logout
    if user_id is not None and user_id >= 0 and session_id is not None:
        session_conversations = Chats.query.filter_by(owner=user_id, session_id=session_id).all()
        print(f"Conversations for Session {session_id} before logout:", session_conversations)

    session.clear()  # Clear the session, including the session ID
    flash('Successfully logged out', 'success')
    return redirect(url_for('login'))
@app.route('/new_session', methods=['GET'])
def start_new_session():
    """Start a new session for the user.

    Returns:
        Response: A response to the request for starting a new session.
    """
    session_id = generate_unique_session_id()  # Generate a new session ID
    session['session_id'] = session_id  # Set the new session ID

    # Redirect to the login page or any other page where a new session can be established
    return redirect(url_for('user'))

@app.route('/user')
def user():
    """Handle requests related to user data.

    Returns:
        Response: A response to the request for user data.
    """
    user_id = session.get('userid')
    is_guest = session.get('guest')

    if user_id is not None:
        if user_id >= 0:
            user_data = User.query.filter_by(id=user_id).first()
            if user_data:
                current_session_id = session.get('session_id')

                # Set session_id if it doesn't exist or is None
                if current_session_id is None:
                    current_session_id = generate_unique_session_id()
                    session['session_id'] = current_session_id

                    # Check if it's the user's first login
                    existing_conversations = Chats.query.filter_by(owner=user_data.id).all()

                    if not existing_conversations:
                        # Create a system-generated welcome message
                        welcome_message = (
                            "Welcome to [Your Application Name]! This is your first login."
                                     )
                        flash(welcome_message, 'info')



                # Retrieve conversation data for the current session
                current_session_chats = Chats.query.filter_by(owner=user_id, session_id=current_session_id).all()

                # Retrieve previous sessions
                previous_sessions = db.session.query(Chats.session_id).filter_by(owner=user_id).distinct().all()

                return render_template('index.html',
                                       current_session_chats=current_session_chats,
                                       previous_sessions=previous_sessions,
                                       user=user_data,
                                       is_guest=False,
                                       session_id=current_session_id)
            else:
                flash('User data not found.', 'error')
        else:
            return render_template('index.html', is_guest=True)
    else:
        flash('User not logged in. Please log in.', 'error')

    return redirect(url_for('login'))

# Add this route to fetch conversation for a specific session ID
@app.route('/fetch_conversation/<string:session_id>', methods=['GET'])
def fetch_conversation(session_id):
    """Fetch conversation data for a specific session ID.

    Args:
        session_id (str): The session ID for which conversation data is requested.

    Returns:
        jsonify: A JSON response containing conversation data.
    """
    user_id = session.get('userid')
    if user_id is not None and user_id >= 0:
        if session_id == "null":
            # Handle the case where session ID is "null"
            return jsonify([])
        
        conversation_data = Chats.query.filter_by(owner=user_id, session_id=session_id).all()

        # Print statements for debugging
        print(f"Conversation Data for Session {session_id}:", conversation_data)

        conversation_list = [{
            "input_data": chat.input_data,
            "output_data": chat.output_data
        } for chat in conversation_data]
        return jsonify(conversation_list)
    else:
        return jsonify([])

# Add this route to fetch sessions ids
@app.route('/fetch_sessions_Ids', methods=['GET'])
def fetch__sessions_Ids():
    """Fetch session IDs for the current user.

    Returns:
        jsonify: A JSON response containing session IDs.
    """
    user_id = session.get('userid')
    if user_id is not None and user_id >= 0:
        previous_sessions = db.session.query(Chats.session_id).filter_by(owner=user_id).distinct().all()

        # Filter out null session IDs before returning
        filtered_sessions = [session_id[0] for session_id in previous_sessions if session_id[0] is not None]

        # Print statements for debugging
        print("Previous Sessions:", filtered_sessions)

        return jsonify(filtered_sessions)
    else:
        return jsonify([])


# Define a route for handling POST requests containing user input
@app.route('/data', methods=['POST'])
def get_data():
    """Handle POST requests containing user input.

    Returns:
        jsonify: A JSON response containing the model's prediction.
    """
    data = request.get_json()
    text = data.get('data')
    user_input = text

    try:
        # Use the selected language model to get a response
        typing_speed = data.get('typing_speed', 3)  # Use a default value if not provided
        llm_temperature = data.get('llm_temperature', 0.7)  # Use a default value if not provided
        output = language_model.predict(user_input, typing_speed=typing_speed, llm_temperature=llm_temperature)

        # Save the conversation data to the database if the user is a registered user
        user_id = session.get('userid')
        session_id = session.get('session_id')  # Retrieve the session_id from the session

        if user_id is not None and user_id >= 0:
            conversation_data = Chats(owner=user_id, input_data=user_input, output_data=output, session_id=session_id)
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
