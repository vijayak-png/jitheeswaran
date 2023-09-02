from flask import Flask, request, jsonify, render_template, redirect, url_for
import csv

app = Flask(__name__)

# Define the path to the CSV file
csv_file_path = "D:\\cxo\\profile.csv"

# Function to read data from CSV and store it in a dictionary
def read_csv_data():
    data = {}
    with open(csv_file_path, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header row
        for row in reader:
            email, password = row[0], row[1]
            data[email] = password
    return data

# Store CSV data in memory
csv_data = read_csv_data()

# Endpoint to render the HTML login form
@app.route('/')
def login_page():
    return render_template('login.html')

# Endpoint to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    try:
        # Get form data from the request
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the provided email exists in the CSV data
        if email in csv_data:
            # Check if the provided password matches the stored password
            if csv_data[email] == password:
                # Redirect to the next page on successful login
                return redirect(url_for('next_page'))
        
        # If login fails, show an error message
        return jsonify({"error": "Invalid login credentials."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint for the next page after successful login
@app.route('/next_page')
def next_page():
    return render_template('next_page.html')

# Endpoint to render the HTML signup form
@app.route('/signup')
def signup_page():
    return render_template('signup.html')

# Endpoint to handle signup form submission
@app.route('/signup', methods=['POST'])
def signup():
    try:
        # Get form data from the request
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the provided email already exists in the CSV data
        if email in csv_data:
            return jsonify({"error": "Email already exists."}), 400

        # Save the new signup data to the CSV file (add your CSV writing logic here)

        # Redirect to the 'sub.html' page upon successful signup
        return redirect(url_for('sub_page'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to render the 'sub.html' page
@app.route('/sub')
def sub_page():
    return render_template('sub.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
