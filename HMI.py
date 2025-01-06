#!/usr/bin/env python3

from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index_test.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    # Retrieve the form data
    action = request.form['action']  # Delivery or Reception
    #weight = request.form['weight']
    door_ramp = request.form['door_ramp']
    location_combined = request.form['location_combined']

    # Create data string for QR code
    qr_data = f"J&M_R{action}{door_ramp}{location_combined}"

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Send the image to the browser
    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

