# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a picture of Lei.
# The result is returned as json. For example:
#
# $ curl -F "file=@Lei.jpg" http://127.0.0.1:5001
#
# Returns:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_Lei": true
# }
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

import face_recognition
import os
from flask import Flask, jsonify, request, redirect

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Is this a picture of Lei?</title>
    <h1>Upload a picture and see if it's a picture of Lei!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''


def detect_faces_in_image(file_stream):
    # Pre-calculated face encoding of Lei generated with face_recognition.face_encodings(img)
    known_face_encoding = [ -7.11279139e-02,   1.22983426e-01,   9.43208709e-02,
        -9.80862603e-02,  -5.62107340e-02,  -1.13418177e-01,
        -3.41067091e-02,  -1.03000261e-01,   1.80417880e-01,
        -1.28590673e-01,   2.60902017e-01,  -5.28102778e-02,
        -2.31831089e-01,  -1.20943777e-01,  -1.18304119e-02,
         2.12682739e-01,  -2.63827473e-01,  -1.31882846e-01,
        -3.79452892e-02,   6.36274517e-02,   1.16968818e-01,
        -5.68333082e-03,   6.53189123e-02,   9.24607515e-02,
        -1.10706650e-01,  -3.65827292e-01,  -1.09532066e-01,
        -4.89493124e-02,  -3.25149447e-02,  -5.63860461e-02,
        -4.14457135e-02,   1.66441184e-02,  -1.86966389e-01,
        -8.32565427e-02,   4.55041341e-02,   4.77054641e-02,
        -5.37577504e-03,  -9.99786258e-02,   1.88284889e-01,
        -4.34060432e-02,  -3.17130208e-01,  -9.24870092e-03,
         1.07365608e-01,   2.20936790e-01,   1.92348659e-01,
        -3.57511826e-03,  -7.89884571e-03,  -1.37902081e-01,
         1.47062644e-01,  -1.69987291e-01,   2.68517509e-02,
         1.37726620e-01,   7.92049393e-02,   3.47217992e-02,
         5.64628132e-02,  -1.26240745e-01,   4.28142771e-02,
         1.97092205e-01,  -1.52313545e-01,  -4.75524627e-02,
         9.80981588e-02,  -1.13969058e-01,   1.41255334e-02,
        -7.71122053e-02,   1.80308685e-01,   4.20256369e-02,
        -1.55654013e-01,  -1.65867761e-01,   9.80149508e-02,
        -1.35042816e-01,  -3.52980942e-02,   7.89564252e-02,
        -1.40327811e-01,  -1.67225391e-01,  -3.22533518e-01,
        -6.69084489e-02,   3.26776028e-01,   7.79186338e-02,
        -1.95328668e-01,   3.09872329e-02,  -6.37697130e-02,
        -3.18884850e-04,   8.46827924e-02,   2.22686246e-01,
        -3.60342301e-03,   7.39280358e-02,  -1.24281608e-01,
         3.39172035e-03,   1.52438313e-01,  -3.70022580e-02,
         4.53025289e-02,   2.79059619e-01,   3.86235863e-03,
         5.15902229e-02,   2.50814687e-02,   1.53597444e-04,
        -1.30407274e-01,   2.60672532e-02,  -1.58413738e-01,
         2.08218973e-02,  -2.57265642e-02,  -1.23384539e-02,
        -4.91752885e-02,   1.27612531e-01,  -1.66174620e-01,
         6.71795756e-02,   1.86525863e-02,   3.15388553e-02,
         1.70767847e-02,  -1.96357295e-02,  -2.57047955e-02,
        -1.43892497e-01,   4.57158387e-02,  -2.13898152e-01,
         1.08701408e-01,   1.60893574e-01,   3.47987339e-02,
         1.04937002e-01,   6.40898123e-02,   8.40381980e-02,
        -3.67956609e-02,  -5.64739220e-02,  -2.06414968e-01,
         4.14526872e-02,   1.06759161e-01,  -6.46827072e-02,
         1.07223623e-01,  -5.93802482e-02]

    lei_image = face_recognition.load_image_file("Lei.jpg")
    print(face_recognition.face_encodings(lei_image)[0])
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)

    face_found = False
    is_Lei = False

    if len(unknown_face_encodings) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face of Lei
        match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
        if match_results[0]:
            is_Lei = True

    # Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_Lei": is_Lei
    }
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
