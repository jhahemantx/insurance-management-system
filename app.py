from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector, sqlite3
from datetime import timedelta

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=10)

def init_db():
    with sqlite3.connect('insurance.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS policies (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            policy_name TEXT,
                            policy_type TEXT,
                            premium_amount REAL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS claims (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            policy_id INTEGER,
                            claim_date TEXT,
                            claim_amount REAL,
                            status TEXT,
                            FOREIGN KEY (policy_id) REFERENCES policies (id))''')
        

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="insurance_db_py"
)
cursor = db.cursor()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists in the database
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        
        if user:
            flash('Email is already registered! Please log in.', 'warning')
            return redirect(url_for('login'))  # Redirect to login if already registered
        else:
            # Insert the new user into the database
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            db.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

# User dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

# Add insurance policy
@app.route('/add_policy', methods=['GET', 'POST'])
def add_policy():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        policy_name = request.form['policy_name']
        policy_type = request.form['policy_type']
        premium_amount = request.form['premium_amount']
        user_id = session['user_id']
        cursor.execute("INSERT INTO policies (user_id, policy_name, policy_type, premium_amount) VALUES (%s, %s, %s, %s)", (user_id, policy_name, policy_type, premium_amount))
        db.commit()
        return redirect(url_for('view_policies'))

    return render_template('add_policy.html')

# View policies
@app.route('/view_policies')
def view_policies():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    cursor.execute("SELECT * FROM policies WHERE user_id = %s", (user_id,))
    policies = cursor.fetchall()
    return render_template('view_policies.html', policies=policies)

# Add claim
@app.route('/add_claim', methods=['GET', 'POST'])
def add_claim():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        policy_id = request.form['policy_id']
        claim_date = request.form['claim_date']
        claim_amount = request.form['claim_amount']
        status = "Pending"
        cursor.execute("INSERT INTO claims (policy_id, claim_date, claim_amount, status) VALUES (%s, %s, %s, %s)", (policy_id, claim_date, claim_amount, status))
        db.commit()
        return redirect(url_for('view_claims'))

    return render_template('add_claim.html')

# View claims
@app.route('/view_claims')
def view_claims():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    query = """
        SELECT policies.policy_name, claims.claim_date, claims.claim_amount, claims.status
        FROM claims
        JOIN policies ON claims.policy_id = policies.id
        WHERE policies.user_id = %s
    """
    cursor.execute(query, (user_id,))
    claims = cursor.fetchall()

    return render_template('view_claims.html', claims=claims)


@app.route('/logout')
def logout():
    # Clear the session data
    session.pop('user_id', None)
    return redirect(url_for('login'))




if __name__ == "__main__":
    app.run(debug=True)
