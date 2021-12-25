from flask import Flask, render_template,redirect ,url_for , request
from pyngrok import ngrok
import os
import numpy as np
import cv2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

app =  Flask (__name__)

app.config['UPLOAD_FOLDER']  = "static"
savedModel=load_model('my_model150')
@app.route('/')
def welcome():
    return redirect('/login')

@app.route('/home', methods = ['POST', 'GET'])
def home():
    # neu la get request:
    if request.method == "POST":
        #day la port

        #lay file mà nguoi dung upload
        image_file = request.files['file']
        print(image_file.filename)
        print(app.config['UPLOAD_FOLDER'])
        path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        #path_to_save = os.path.join(app.config['UPLOAD_FOLDER'],image_file)
        image_file.save(path_to_save)
        #xử lý tương tự trong moldel

        #test_image = path_to_save
        test_image = cv2.imread(path_to_save)
        test_image = cv2.resize( test_image , (224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = savedModel.predict(test_image)
        #training_set.class_indices
        print(result)
        if result[0][0] == 0:
            prediction = 'yes'
            return render_template('index.html', msg='có u não')
        else:
            prediction = 'no'
            return render_template('index.html', msg='không có u não')
        #print(prediction)
    else:
        # Nếu là GET thì hiển thị giao diện upload
        return render_template('index.html')

    #return "Day la home"
@app.route('/login')
def login():
    error = None
    if request.method == 'GET':
        if request.args.get('username') != 'admin' or request.args.get('password') != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)
#start server
if __name__ == '__main__' :
    app.run(host = '0.0.0.0', port=9999, debug=True) 
