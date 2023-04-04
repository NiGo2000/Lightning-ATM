from io import BytesIO
import time
from flask import Flask, request, send_file
from flask_cors import CORS
import qrcode
import utilities

app = Flask(__name__)
CORS(app)

@app.route('/total-deposits')
def total_deposits():
    # Hier wird der Gesamt-Einzahlungsbetrag aus der Datenbank abgerufen
    # und als JSON-Objekt zurückgegeben
    total_eur = utilities.get_total_eur()
    return {'total_deposits': total_eur}
    
@app.route('/total-price')
def total_price():
    # Hier wird der Gesamt-Preis in Satoshi aus der Datenbank abgerufen
    # und als JSON-Objekt zurückgegeben
    total_eur = utilities.get_total_eur()
    total_satoshi = utilities.calculate_satoshi(total_eur)
    return {'total_price_satoshi': total_satoshi, 'total_price_eur': total_eur}


@app.route('/qr-code')
def qr_code():
    # Hier werden die notwendigen Parameter aus der Anfrage abgerufen
    satoshis = request.args.get('satoshis')
    qr_size = request.args.get('qr_size', default=200, type=int)

    # Hier wird der Lightning Invoice generiert
    #lightning_invoice = utilities.generate_lightning_invoice(satoshis)

    # Hier wird der QR-Code generiert
    #qr_text = 'lightning:' + lightning_invoice

    qr_text = "google.de"
    qr = qrcode.QRCode(version=None, box_size=10, border=4)
    qr.add_data(qr_text)
    qr.make(fit=True)

    # Hier wird das generierte Bild als Datei zurückgegeben
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')

@app.route('/check-payment')
def check_payment():
    # Hier wird der Wahrheitswert für check_payment aus der Datenbank abgerufen
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 5:
            check_payment = True
            return {'check_payment': check_payment}
        time.sleep(0.1)

@app.route('/cancel')
def cancel():
    utilities.reset()
    return {'reset': True}

if __name__ == '__main__':
    app.run(debug=True)
