import requests


try:
        # Set up the request parameters
        satoshis = 100
        url = 'http://localhost:5000/qr-code?satoshis=' + str(satoshis)

        headers = {'Content-type': 'application/json'}
        response = requests.get(url, headers=headers)
        # Check if the response is successful and contains the image
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'image/png'
        with open('test_qr_code.png', 'wb') as f:
            f.write(response.content)

except Exception as e:
        print("An error occurred while testing the QR code generation functionality:", e)

