from flask import Flask, request, jsonify, render_template
from docx import Document
import io
from datetime import datetime
import smtplib
from email.message import EmailMessage
import pandas as pd
import requests

app = Flask(__name__)

# Load the CSV data
csv_file_path = r'D:\cxo\templates\news_frade.csv'
data = pd.read_csv(csv_file_path)

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'  # Gmail SMTP server
SMTP_PORT = 587  # TLS port for Gmail
SMTP_USERNAME = '220701108@rajalakshmi.edu.in'
SMTP_PASSWORD = 'tynnexpotghncbsd'

# Trusted dictionary for real news detection
trusted_dictionary = {
    "breaking": 1,
    "announcement": 1,
    "official": 1,
    "confirmed": 1,
}

# GPT API configuration
GPT_API_URL = "https://api.openai.com/v1/engines/davinci-codex/completions"
GPT_API_KEY = "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"


def call_gpt_api(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GPT_API_KEY}"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 100
    }
    response = requests.post(GPT_API_URL, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return ""

def check_meaning(original_text, generated_text):
    # Convert both texts to lowercase for case-insensitive comparison
    original_text_lower = original_text.lower()
    generated_text_lower = generated_text.lower()

    # Split texts into words
    original_words = original_text_lower.split()
    generated_words = generated_text_lower.split()

    # Check if at least one keyword from original text is present in generated text
    for keyword in original_words:
        if keyword in generated_words:
            return True
    
    return False

def split_text_into_lines(text, max_line_length):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_line_length:
            if current_line:
                current_line += " "
            current_line += word   
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

@app.route('/')
def index():
    return render_template('popup.html')

@app.route('/predict', methods=['POST'])
def predict():
    user_headline = request.json.get('title', '')

    if not user_headline:
        return jsonify({'error': 'No headline provided'})

    # Call GPT API to generate text for user headline
    gpt_response_user = call_gpt_api(f"Match the meaning of: '{user_headline}'")

    # Check if generated text matches the meaning of user headline
    meaning_matched_user = check_meaning(user_headline, gpt_response_user)

    # Check if the user-provided headline is present in the CSV data
    if user_headline in data['title'].values:
        prediction = "REAL"
        show_report_form = False
        percentage_matched = 100  # You can set this to 100 since it's a direct match
    else:
        # Call GPT API to generate text for data headlines
        gpt_responses_data = [call_gpt_api(f"Match the meaning of: '{headline}'") for headline in data['title']]
        
        # Check if generated text matches the meaning of data headlines
        meaning_matched_data = [check_meaning(data_headline, gpt_response) for data_headline, gpt_response in zip(data['title'], gpt_responses_data)]

        # Calculate the percentage of data headlines with matching meaning
        percentage_matched = sum(meaning_matched_data) / len(meaning_matched_data) * 100
        
        # Determine prediction and show_report_form based on user and data headline meanings
        if meaning_matched_user or percentage_matched >= 50:
            prediction = "REAL"
            show_report_form = False
        else:
            prediction = "FAKE"
            show_report_form = True

    return jsonify({'prediction': prediction, 'show_report_form': show_report_form, 'percentage_matched': percentage_matched})
@app.route('/report', methods=['POST'])
def report():
    user_website = request.json.get('website')
    fake_news = request.json.get('fake_news')

    if user_website is None or fake_news is None:
        return jsonify({'error': 'Please provide both website and fake_news parameters'})

    docx_template_path = r"D:\cxo\c.docx"  # Update with your DOCX template path
    doc = Document(docx_template_path)

    # Replace placeholders with user-provided data
    placeholders = {
        "{current_date}": datetime.now().strftime('%Y-%m-%d'),
        "{user_website}": user_website,
        "{fake_news}": fake_news
    }

    for paragraph in doc.paragraphs:
        for placeholder, value in placeholders.items():
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, value)

    # Create a BytesIO buffer to hold the modified DOCX data
    modified_docx_buffer = io.BytesIO()
    doc.save(modified_docx_buffer)
    modified_docx_buffer.seek(0)  # Reset the buffer position

    # Send the report via email
    recipient_email = '220701108@rajalakshmi.edu.in'  # Update with the recipient's email
    send_email(modified_docx_buffer.getvalue(), recipient_email)  # Include docx_data argument

    return jsonify({'message': 'Report generated and sent successfully'})



def send_email(docx_data, recipient_email):
    msg = EmailMessage()
    msg.set_content('Please find the attached report.')

    msg['Subject'] = 'Fake News Report'
    msg['From'] = SMTP_USERNAME
    msg['To'] = recipient_email

    # Attach the modified DOCX report
    msg.add_attachment(docx_data, maintype='application', subtype='vnd.openxmlformats-officedocument.wordprocessingml.document', filename='report.docx')

    # Set up the SMTP server and send the message
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)