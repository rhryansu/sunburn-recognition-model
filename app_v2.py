# import email
# from tkinter import E
# from urllib import response
from flask import Flask, render_template, request
from flask_mail import *
#from werkzeug import secure_filename
# from werkzeug.utils import secure_filename
# #from werkzeug.datastructures import  FileStorage
# from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image

# try:
#    import shutil
#    shutil.rmtree('uploaded / image')
#    % cd uploaded % mkdir image % cd ..
#    print()
# except:
#    pass

model = tf.keras.models.load_model('model')
app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'monashietp04@gmail.com'
app.config['MAIL_PASSWORD'] = 'Monashie.tp04'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

app.config['UPLOAD_FOLDER'] = 'uploaded/image'
save_pic_name = 'one_img.png'
img_path = os.path.join(app.config['UPLOAD_FOLDER'], save_pic_name)


@app.route('/')
def upload_f():
    return render_template('upload.html')


def finds():
    # test_datagen = ImageDataGenerator(rescale = 1./255)
    vals = [2, 1]
    # test_dir = 'uploaded'
    # test_generator = test_datagen.flow_from_directory(
    #         test_dir,
    #         target_size =(255, 255),
    #         color_mode ="rgb",
    #         shuffle = False,
    #         class_mode ='categorical',
    #         batch_size = 1)
    # img_path = os.path.join(app.config['UPLOAD_FOLDER'], save_pic_path)
    # img_path = '/content/app/uploaded/image/WX20220424-1754202x.png'
    img = image.load_img(img_path, target_size=(64, 64))
    x = image.img_to_array(img)/255.0
    x = np.expand_dims(x, axis=0)

    # pred = model.predict_generator(test_generator)
    pred = model.predict(x)
    print(pred)
    result = vals[np.argmax(pred)]
    return result


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        e = request.form['email']
        f.save(img_path)
        val = finds()

        email_sender(val, e)
        # name = 'Diagnosis Report'
        # html = render_template('pred.html' name=name)
        # pdf = pdfkit.from_string(html, False)
        # response = make_response(pdf)
        # response.headers["Content-Type"] = "application/pdf"
        # response.headers["Content-Disposition"] = "inline; filename=Report.pdf"

        return render_template('index.html')


def email_sender(degree, recipients):

    e = str(recipients)

    if degree == 1:
        msg = Message(subject="Protecturskin Sunburn Recognition Report",
                      body="Here's the diagnosis report.", sender='monashietp04@gmail.com', recipients=[e])
        with app.open_resource("./templates/f_degree.pdf") as fp:
            msg.attach("f_degree.pdf", "application/pdf", fp.read())
            mail.send(msg)
    else:
        msg = Message(subject="Protecturskin Sunburn Recognition Report",
                      body="Here's the diagnosis report.", sender='monashietp04@gmail.com', recipients=[e])
        with app.open_resource("./templates/s_degree.pdf") as fp:
            msg.attach("s_degree.pdf", "application/pdf", fp.read())
            mail.send(msg)


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
