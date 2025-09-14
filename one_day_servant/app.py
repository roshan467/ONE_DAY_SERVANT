from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "secretkey"

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # change to your MySQL username
        password="password", # change to your MySQL password
        database="one_day_servant"
    )

# ---------------------- Home ----------------------
@app.route("/")
def home():
    if 'role' in session:
        if session['role'] == 'user':
            return redirect(url_for('user_dashboard'))
        elif session['role'] == 'servant':
            return redirect(url_for('servant_dashboard'))
    return render_template("index.html")

# ---------------------- Registration ----------------------
@app.route("/register/user", methods=['GET', 'POST'])
def register_user():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password, phone, address) VALUES (%s,%s,%s,%s,%s)",
            (name, email, password, phone, address)
        )
        conn.commit()
        conn.close()
        flash("Registration Successful! Please login.", "success")
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route("/register/servant", methods=['GET', 'POST'])
def register_servant():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        skill = request.form['skill']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO servants (name, email, password, phone, skill) VALUES (%s,%s,%s,%s,%s)",
            (name, email, password, phone, skill)
        )
        conn.commit()
        conn.close()
        flash("Servant registered successfully!", "success")
        return redirect(url_for('home'))
    return render_template("register_servant.html")

# ---------------------- Login / Logout ----------------------
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        # Check in users
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        # Check in servants
        cur.execute("SELECT * FROM servants WHERE email=%s AND password=%s", (email, password))
        servant = cur.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['user_id']
            session['role'] = 'user'
            session['name'] = user['name']
            flash("Logged in successfully as User!", "success")
            return redirect(url_for('user_dashboard'))
        elif servant:
            session['servant_id'] = servant['servant_id']
            session['role'] = 'servant'
            session['name'] = servant['name']
            flash("Logged in successfully as Servant!", "success")
            return redirect(url_for('servant_dashboard'))
        else:
            flash("Invalid credentials!", "danger")
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('home'))

# ---------------------- Dashboards ----------------------
@app.route("/user/dashboard")
def user_dashboard():
    if 'role' not in session or session['role'] != 'user':
        flash("Access denied!", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM servants WHERE availability=TRUE")
    servants = cur.fetchall()
    conn.close()
    return render_template("user_dashboard.html", servants=servants)

@app.route("/servant/dashboard")
def servant_dashboard():
    if 'role' not in session or session['role'] != 'servant':
        flash("Access denied!", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM bookings WHERE servant_id=%s", (session['servant_id'],))
    bookings = cur.fetchall()
    conn.close()
    return render_template("servant_dashboard.html", bookings=bookings)

# ---------------------- Booking ----------------------
@app.route("/book", methods=['GET', 'POST'])
def book_service():
    if 'role' not in session or session['role'] != 'user':
        flash("Access denied!", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM servants WHERE availability=TRUE")
    servants = cur.fetchall()
    conn.close()

    if request.method == "POST":
        servant_id = request.form['servant_id']
        service_type = request.form['service_type']
        user_id = session['user_id']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO bookings (user_id, servant_id, service_type) VALUES (%s,%s,%s)",
            (user_id, servant_id, service_type)
        )
        conn.commit()
        conn.close()
        flash("Booking Successful!", "success")
        return redirect(url_for('user_dashboard'))

    return render_template("book_service.html", servants=servants)

@app.route("/book/<int:servant_id>", methods=['POST'])
def book_servant(servant_id):
    if 'role' not in session or session['role'] != 'user':
        flash("Access denied!", "danger")
        return redirect(url_for('login'))

    hours = int(request.form['hours'])
    total_price = int(request.form['total_price'])

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO bookings (servant_id, hours, total_price) VALUES (%s,%s,%s)",
        (servant_id, hours, total_price)
    )
    conn.commit()
    conn.close()
    flash(f"Servant booked successfully for {hours} hours! Total: ₹{total_price}", "success")
    return redirect(url_for('user_dashboard'))

# ---------------------- Other Pages ----------------------
@app.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/servant")
def servant_page():
    return render_template("servant.html")

@app.route("/booking")
def booking_page():
    return render_template("booking.html")

# ---------------------- Run App ----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)



