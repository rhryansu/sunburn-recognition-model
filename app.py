from flask import Flask, render_template, request
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename
#from werkzeug.datastructures import  FileStorage
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import os 
  
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
  
@app.route('/')
def upload_f():
    return render_template('upload.html')
  
def finds():
    test_datagen = ImageDataGenerator(rescale = 1./255)
    vals = ["Second_degree", "First_degree"]
    test_dir = 'uploaded'
    test_generator = test_datagen.flow_from_directory(
            test_dir,
            target_size =(255, 255),
            color_mode ="rgb",
            shuffle = False,
            class_mode ='categorical',
            batch_size = 1)
  
    pred = model.predict_generator(test_generator)
    print(pred)
    print(np.argmax(pred,axis = 1))
    indexs = np.argmax(pred,axis = 1)
    print(vals)
    return str(vals[indexs[0]])
  
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        val = finds()
        return render_template('pred.html', ss = val)
  
if __name__ == '__main__':
    app.run()