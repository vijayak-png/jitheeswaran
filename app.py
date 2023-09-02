from flask import Flask, request, jsonify, render_template, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('next_page.html')

@app.route('/save_csv', methods=['POST'])
def save_csv():
    data = request.get_json()
    csv_content = data.get('csvContent', '')

    try:
        with open('templates/news_frade.csv', 'a') as file:
            file.write(csv_content + '\n')

        response = {'message': 'CSV file saved successfully'}
        return jsonify(response), 200
    except Exception as e:
        response = {'message': 'Error saving CSV file'}
        return jsonify(response), 500

if __name__ == '__main__':
    app.run()
def download_csv():
    try:
        csv_content = ""
        headlines = request.args.getlist('headline')  # Get the headlines from query parameters

        if headlines:
            csv_content = "Headline\n" + "\n".join(headlines)

        with open('static/news_frade.csv', 'w') as file:
            file.write(csv_content)
        return send_file('static/news_frade.csv', as_attachment=True)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run()
