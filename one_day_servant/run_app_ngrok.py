from flask import Flask, render_template, request, redirect, url_for, session, flash
from pyngrok import ngrok
import threading
import mysql.connector

# ---------------------- Flask App ----------------------
app = Flask(__name__, template_folder="frontend", static_folder="frontend")
app.secret_key = "secretkey"

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # your MySQL username
        password="password", # your MySQL password
        database="one_day_servant"
    )

# ---------------------- Routes ----------------------
@app.route("/")
def home():
    return render_template("index.html")

# Example: Add more routes like register, login, dashboard...
# (Copy your routes from app.py here if needed)

# ---------------------- Run Flask ----------------------
def run_flask():
    app.run(port=5000, debug=True)

# ---------------------- Start ngrok ----------------------
def start_ngrok():
    url = ngrok.connect(5000)
    print(f"Public URL: {url}")

# ---------------------- Main ----------------------
if __name__ == "__main__":
    # Start ngrok tunnel in a thread
    threading.Thread(target=start_ngrok).start()
    # Start Flask app
    run_flask()
