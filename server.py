import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from isql import isql
import unicodedata
import mysql.connector

count=1
level=1
user=''
data_user=''
sc1=''

school = [
        ['class', ['classid', 'classroom']], 
        ['student', ['studentid', 'classid', 'name', 'dob(Date Of Birth)', 'grade(standard)', 'address']],
        ['teaching', ['profid', 'classid', 'field']],
        ['professor', ['profid', 'name', 'salary', 'position', 'contact', 'address']] 
]
retail = [
        ['customer', ['customerid', 'name', 'contact' , 'storeid' , 'productid' , 'price']], 
        ['manager', ['managerid', 'name', 'contact', 'address', 'storeid']],
        ['product', ['productid', 'name', 'price' , 'storeid' , 'wholesalerid']],
        ['store', ['storeid', 'location', 'number of workers']],
        ['wholesaler', ['wholesalerid', 'name', 'location']]
]
restaurant = [
        ['customer', ['customerid', 'name', 'contact' , 'table number' , 'bill amount' , 'branchid']], 
        ['branch', ['branchid', 'location', 'number of workers', 'capacity']],
        ['manager', ['managerid', 'name', 'contact', 'branchid']],
        ['staff', ['staffid', 'name', 'position', 'salary', 'branchid']] 
]
hospital = [
        ['department', ['departmentid', 'name', 'number of doctors' , 'number of rooms', 'HOD(Head Of Department)']], 
        ['doctor', ['doctorid', 'name', 'age', 'speciality', 'departmentid', 'visiting day']],
        ['patient', ['patientid', 'name', 'contact', 'age', 'disease', 'room number', 'doctorid', 'bill amount']],
        ['room', ['room number', 'floor', 'number of beds', 'number of staff']],
        ['staff', ['staffid', 'name', 'contact', 'age', 'position', 'salary', 'departmentid', 'room number']]  
]

UPLOAD_FOLDER = 'F:\\isql-python3\\uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
input_data =''


@app.route('/db', methods = [ 'GET', 'POST'])
def db():
    global school,retail,restaurant,hospital,user,data_user,sc1
    user = request.form['DB']
    if user == "School" :
        user = school
        data_user = 'school_query'
        sc1 = ques_fetch()
        return render_template("task.html", data=school, ques=sc1)
    if user == "Retail_Store" :
        user = retail
        data_user = 'retail_query'
        sc1 = ques_fetch()
        return render_template("task.html", data=retail)
    if user == "Restaurant" :
        user = restaurant
        data_user = 'restaurant_query'
        sc1 = ques_fetch()
        return render_template("task.html", data=restaurant)
    if user == "Hospital" :
        user = hospital
        data_user = 'hospital'
        sc1 = ques_fetch()
        return render_template("task.html", data=hospital)
    if user == "Custom" :
        return render_template("custom.html", "")


@app.route('/next_ques')
def next_ques():
    global count, user, level,sc1
    count+=1
    if count == 4 :
        level+=1
        count = 1
    sc1 = ques_fetch()
    return render_template("task.html", data = user, ques=sc1)


@app.route('/answer')
def content():
    global user,sc1
    text = open('textfile.txt', 'r+')
    content = text.read()
    text.close()
    return render_template('task.html', data = user, ques=sc1, text=content)


def ques_fetch():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="question"
    )
    global count, data_user, level
    cursor = mydb.cursor ()
    # number_row = cursor.execute ("select count(*) from "+ data_user +" where level= %s ",(level,))
    cursor.execute ("select user_ques from "+ data_user +" where level= %s ",(level,))
    sc = cursor.fetchmany(count)
    return sc[count-1]

def allowed_file(filename):
    return '.' in filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print("upload_found")
    global input_data
    thesaurus_path = None
    json_output_path = None
    stopwords_path = None
    input_ques = request.form['question']
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file1']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_data = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            isql(input_data, str("F:\isql-python3\lang\english.csv"), input_ques , str("F:\isql-python3\output.json"), thesaurus_path, stopwords_path)
        text = open('output.txt', 'r+')
        content = text.read()
        text.close()
    return render_template('custom.html', text=content)



@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template("index.html")

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")

@app.route('/custom', methods=['GET', 'POST'])
def custom():
    return render_template("custom.html")

@app.route('/task', methods=['GET', 'POST'])
def task():
    return render_template("task.html")



if __name__ == '__main__':
    app.run(debug=True)
