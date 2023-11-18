# Chatbot Application

Welcome to the Chatbot Application! This project allows you to interact with a chatbot using a Flask web application.

## Setup

### Prerequisites

Before you begin, ensure you have the following installed on your computer:

1. **Python 3.7 or later:** You can download and install it from [python.org](https://www.python.org/downloads/).

2. **Git:** If you're on Windows, download and install Git from [git-scm.com](https://git-scm.com/download/win). Linux users can install Git through their package manager:

    On Ubuntu or Debian:

    ```bash
    sudo apt-get update
    sudo apt-get install git
    ```

    On Fedora:

    ```bash
    sudo dnf install git
    ```

    On CentOS:

    ```bash
    sudo yum install git
    ```

3. **Virtual Environment (Optional but recommended):** This helps to create an isolated environment for your project.

### Installation

Follow these steps to set up the Chatbot Application:

1. **Open your terminal or Command Prompt:**

    - On **Windows:** Press `Win + R`, type `cmd`, and press Enter.
    - On **Linux:** Press `Ctrl + Alt + T` or use the terminal shortcut for your distribution.

2. **Navigate to the directory where you want to clone the repository:**

    ```bash
    cd path\to\your\desired\directory
    ```

3. **Clone the repository:**

    ```bash
    git clone git@github.com:b-aragu/chatbot.git
    ```

    This will clone the repository using the SSH protocol.

4. **Navigate to the project directory:**

    ```bash
    cd chatbot
    ```

5. **Create and activate a virtual environment:**

    If you're new to virtual environments, these commands will help set it up:

    ```bash
    python -m venv venv
    ```

    On Windows, use:

    ```bash
    .\venv\Scripts\activate
    ```

    On Linux, use:

    ```bash
    source venv/bin/activate
    ```

6. **Install project dependencies:**

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

