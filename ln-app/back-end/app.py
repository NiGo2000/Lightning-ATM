from io import BytesIO
import json
import time
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import qrcode
import utilities
import requests

app = Flask(__name__)
CORS(app)

@app.route('/total-price')
def total_price():
    try:
        # get the total price in Satoshi from the database
        total_eur = utilities.get_total_eur()
        total_satoshi = utilities.calculate_satoshi(total_eur)
        return {'total_price_satoshi': total_satoshi, 'total_price_eur': total_eur, 'error_message': None}
    except Exception as e:
        error_message = "Error fetching total price from database: {}".format(str(e))
        return {'total_price_satoshi': None, 'total_price_eur': None, 'error_message': error_message}


@app.route('/qr-code')
def qr_code():
    # Here the necessary parameters are retrieved from the request
    lnurl = request.args.get('lnurl')
    qr_size = request.args.get('qr_size', default=200, type=int)
    
    # The QR code is generated here
    qr_text = lnurl

    qr = qrcode.QRCode(version=None, box_size=10, border=4)
    qr.add_data(qr_text)
    qr.make(fit=True)

    # Here the generated image is returned as a file
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')

@app.route('/create-lnurl-withdraw-link')
def create_lnurl_withdraw_link():
    satoshis_buffer = request.args.get('satoshis')

    satoshis = int(satoshis_buffer)
    # The Lightning Invoice is generated here
    lnurl_withdraw_link = utilities.create_lnurl_withdraw_link(satoshis)
    
    if lnurl_withdraw_link is not None:
        return {'lnurl': lnurl_withdraw_link["lnurl"], 'error': None}
    else:
        return {'error': "balance is too low"}
    
@app.route('/check-withdrawal-link')
def check_withdrawal_link():
    lnurl = utilities.check_withdrawal_link()
    
    if lnurl is False:
        return jsonify(False)
    else:
        return lnurl
    
@app.route('/check-payment')
def check_payment():
    lnurl = request.args.get('lnurl')
    payment_success = utilities.check_withdraw_link_status(lnurl)
    
    if payment_success is not True:
        return {'payment': 'False'}
    else:
        return {'payment': 'True'}

@app.route('/cancel')
def cancel():
    utilities.reset()
    return {'reset': True}

if __name__ == '__main__':
    app.run(debug=True)
