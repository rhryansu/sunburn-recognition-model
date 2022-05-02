from flask import Flask, render_template, request
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename
#from werkzeug.datastructures import  FileStorage
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import os 
from tensorflow.keras.preprocessing import image
  
#try:
#    import shutil
#    shutil.rmtree('uploaded / image')
#    % cd uploaded % mkdir image % cd ..
#    print()
#except:
#    pass
  
model = tf.keras.models.load_model('model')
app = Flask(__name__)
  
app.config['UPLOAD_FOLDER'] = 'uploaded/image'
save_pic_name = 'one_img.png'
img_path = os.path.join(app.config['UPLOAD_FOLDER'], save_pic_name) 
  
@app.route('/')
def upload_f():
    return render_template('upload.html')
  
def finds():
    # test_datagen = ImageDataGenerator(rescale = 1./255)
    vals = ["Second_degree", "First_degree"]
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
    return str(vals[np.argmax(pred)])
  
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(img_path)
        val = finds()
        return render_template('pred.html', ss = val)
  
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")