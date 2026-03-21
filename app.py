from flask import Flask, render_template, request, jsonify
from delete_mails import delete_mails

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/delete', methods=['POST'])
def delete():
    data = request.json
    try:
        # Anahtar kelimeleri virgülle ayırılmış stringe dönüştür
        keywords = data['keywords'].strip().split('\n')  # Enter ile ayırılmış
        keywords = [k.strip() for k in keywords if k.strip()]  # Boşlukları temizle
        
        result = delete_mails(
            email=data['email'],
            password=data['password'],
            keywords=keywords,  # ← Yeni parametre
            delete_from=data.get('delete_from'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date')
        )
        return jsonify({'status': 'success', 'deleted': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)