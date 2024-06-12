from flask import Blueprint, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import cv2

home_bp = Blueprint('home', __name__, template_folder='templates', static_folder='static')

# Define the upload folder path
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@home_bp.route('/', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        if 'image' not in request.files:
            print('No file part')
            return redirect(request.url)
        img = request.files['image']
        if img.filename == '':
            print('No selected file')
            return redirect(request.url)
        
        if img:
            # Save the uploaded image to the upload folder
            filename = secure_filename(img.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            img.save(file_path)
            
            # Read the image file
            img_cv = cv2.imread(file_path)
            
            # Process the image with OpenCV (e.g., detect QR code)
            detector = cv2.QRCodeDetector()
            val, _, _ = detector.detectAndDecode(img_cv)
            print('QR Code data:', val)
            
            # Delete the image after processing
            os.remove(file_path)
            
            return render_template('scan_qr.html', data=val)
    return render_template('scan_qr.html')
