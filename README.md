# Chatbot Application

Welcome to the Chatbot Application! This project allows you to interact with a chatbot using a Flask web application.

## Setup

### Prerequisites

Before you begin, ensure you have the following installed on your computer:

1. **Python 3.7 or later:** You can download and install it from [python.org](https://www.python.org/downloads/).

2. **Virtual Environment (Optional but recommended):** This helps to create an isolated environment for your project.

### Installation

Follow these steps to set up the Chatbot Application:

1. **Clone the repository:**

    Open your terminal or command prompt and run:

    ```bash
    git clone https://github.com/your-username/chatbot-application.git
    ```

2. **Navigate to the project directory:**

    Change into the project directory:

    ```bash
    cd chatbot
    ```

3. **Create and activate a virtual environment:**

    If you're new to virtual environments, these commands will help set it up:

    ```bash
    python -m venv venv
    ```

    On Windows, use:

    ```bash
    .\venv\Scripts\activate
    ```

    On Unix or MacOS, use:

    ```bash
    source venv/bin/activate
    ```

4. **Install project dependencies:**

    Install the required packages for the Chatbot Application:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Now that your environment is set up, let's run the application:

1. **Run the application:**

    Start the Flask application by running:

    ```bash
    python app.py
    ```

   The application will be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000).

2. **Interact with the chatbot:**

    Open your web browser and visit the provided URL to talk to the chatbot.

## Project Structure

Here's a brief overview of the project structure:

- **`app.py`:** Main Flask application file.
- **`echomodel.py`:** Custom chatbot model (you can replace this with your actual model).
- **`requirements.txt`:** List of project dependencies.
- **`templates/`:** HTML templates for rendering web pages.

Feel free to explore and modify the code to customize your Chatbot Application!

