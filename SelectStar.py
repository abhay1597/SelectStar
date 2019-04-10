import os
from flask import Flask, flash, request, redirect, url_for,render_template, g, session
from werkzeug.utils import secure_filename
from isql import isql
import unicodedata
import mysql.connector

count=1
level=1
user=''
data_user=''
sc1=''
data_base1=''
data_base =['C:\\wamp64\\www\\SelectStar\\database\\SchoolDB.sql','C:\\wamp64\\www\\SelectStar\\database\\Retail_StoreDB.sql','C:\\wamp64\\www\\SelectStar\\database\\HospitalDB.sql','C:\\wamp64\\www\\SelectStar\\database\\RestaurantDB.sql','C:\\wamp64\\www\\SelectStar\\database\\TaxiBookingDB.sql','C:\\wamp64\\www\\SelectStar\\database\\BookSupplyDB.sql']
thesaurus_path = None
stopwords_path = None
content = ''
username=''

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
taxibooking = [
        ['cab', ['regNo', 'capacity', 'company', 'driverid', 'insuranceNo']],
        ['driver', ['driverid', 'name', 'age', 'regNo', 'licenceNo']],
        ['passenger', ['passengerid', 'name', 'contact', 'source', 'destination', 'driverid']],
        ['route', ['routeid', 'passengerid', 'distance', 'fare']],
        ['transaction', ['transactionid', 'routeid', 'cardDetails', 'eWalletName']] 
]
booksupply = [
        ['author', ['authorid', 'name', 'age', 'language']],
        ['book', ['bookid', 'name', 'year', 'noOfPages', 'authorid', 'price']],
        ['printingpress', ['bookid', 'noOfCopies', 'warehouseLocation']],
        ['store', ['location', 'bookid', 'shelfNo']]
]

UPLOAD_FOLDER = '.\\uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
input_data =''


@app.route('/db', methods = [ 'GET', 'POST'])
def db():
    global school,retail,restaurant,hospital,user,data_user,sc1,data_base,data_base1,thesaurus_path,stopwords_path,count
    user = request.form['DB']
    if user == "School" :
        user = school
        data_user = 'school_query'
        sc1 = ques_fetch()
        data_base1 = data_base[0]
        isql(data_base1, str(".\lang\english.csv"), sc1[0] , str(".\output.json"), thesaurus_path, stopwords_path)
        return render_template("task.html", data=school, ques=sc1[1], username = username)
    if user == "Retail Store" :
        user = retail
        count = 1
        data_user = 'retailstore_query'
        sc1 = ques_fetch()
        data_base1 = data_base[1]
        isql(data_base1, str(".\lang\english.csv"), sc1[0] , str(".\output.json"), thesaurus_path, stopwords_path)
        return render_template("task.html", data=retail, ques=sc1[1], username = username)
    if user == "Restaurant" :
        user = restaurant
        count = 1
        data_user = 'restaurant_query'
        sc1 = ques_fetch()
        data_base1 = data_base[3]
        isql(data_base1, str(".\lang\english.csv"), sc1[0] , str(".\output.json"), thesaurus_path, stopwords_path)
        return render_template("task.html", data=restaurant, ques=sc1[1], username = username)
    if user == "Hospital" :
        user = hospital
        count = 1
        data_user = 'hospital_query'
        sc1 = ques_fetch()
        data_base1 = data_base[2]
        isql(data_base1, str(".\lang\english.csv"), sc1[0] , str(".\output.json"), thesaurus_path, stopwords_path)
        return render_template("task.html", data=hospital, ques=sc1[1], username = username)
    if user == "Taxi Booking" :
        user = taxibooking
        count = 1
        data_user = 'taxibooking_query'
        sc1 = ques_fetch()
        data_base1 = data_base[4]
        isql(data_base1, str(".\lang\english.csv"), sc1[0] , str(".\output.json"), thesaurus_path, stopwords_path)
        return render_template("task.html", data=taxibooking, ques=sc1[1], username = username)
    if user == "Book Supply" :
        user = booksupply
        count = 1
        data_user = 'booksupply_query'
        sc1 = ques_fetch()
        data_base1 = data_base[5]
        isql(data_base1, str(".\lang\english.csv"), sc1[0] , str(".\output.json"), thesaurus_path, stopwords_path)
        return render_template("task.html", data=booksupply, ques=sc1[1], username = username)      
    if user == "Feed In" :
        return render_template("custom1.html", username=username)


@app.route('/next_ques')
def next_ques():
    global count, user, level,sc1,data_base1,thesaurus_path,stopwords_path
    count+=1
    count1 = ques_num()
    print(count1)
    if count > count1 :
        level+=1
        count = 1
    if level > 3 :
        level = 1
    sc1 = ques_fetch()
    isql(data_base1, str(".\lang\english.csv"), sc1[0] , str(".\output.json"), thesaurus_path, stopwords_path)
    return render_template("task.html", data = user, ques=sc1[1], username = username)


@app.route('/answer')
def content():
    global user,sc1,content
    text = open('output.txt', 'r+')
    content = text.read().replace('\n','<br>')
    text.close()
    return render_template('task.html', data = user, ques=sc1[1], text=content, username = username)


def ques_num():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="question"
    )
    global data_user, level
    cursor1 = mydb.cursor ()
    cursor1.execute ("select count(*) from "+ data_user +" where level= %s",(level,))
    (number_row,) = cursor1.fetchone()
    return number_row


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
    cursor.execute ("select system_ques,user_ques from "+ data_user +" where level= %s ",(level,))
    sc = cursor.fetchmany(count)
    return sc[count-1]

def allowed_file(filename):
    return '.' in filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    global input_data,thesaurus_path,stopwords_path
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
            isql(input_data, str(".\lang\english.csv"), input_ques , str(".\output.json"), thesaurus_path, stopwords_path)
        text = open('output.txt', 'r+')
        content = text.read().replace('\n','<br>')
        text.close()
    return render_template('custom.html', text=content)



@app.route('/submit', methods=['GET', 'POST'])
def submit():
    global content
    input1 = request.form['answer']
    ans = request.form['ans']
    input1=input1.lower()
    inputList = input1.split()
    if 'inner' in inputList:
        inputList.remove('inner')
    f = open("output.txt","r")
    fileInput=f.read()
    fileInput=fileInput.lower()
    fileInput = fileInput.split()
    if 'inner' in fileInput:
        fileInput.remove('inner')
    tempFile=fileInput
    tempInput=inputList

    if ans == "Submit" :
        if fileInput == inputList:
            content = 'Congrats!!! your answer is correct.'
            return render_template('task.html', data = user, ques=sc1[1], text=content, username = username)
        else:
            content = 'Sorry Wrong Answer.'
            return render_template('task.html', data = user, ques=sc1[1], text=content, username = username)


    if ans == "Hint" :
        if fileInput == inputList:
            content = 'Congrats!!! your answer is correct.'
            return render_template('task.html', data = user, ques=sc1[1], text=content, username = username)
        if fileInput != inputList:
            if 'select' in fileInput:
                a = fileInput.index('select')
            #print(a,"\n")
            if 'from' in fileInput:
                b=fileInput.index('from')
            #print(b,"\n")
            if 'join' in fileInput:
                c=fileInput.index('join')
            #print(c,"\n")
            if 'where' in fileInput:
                d=fileInput.index('where')

            try:
                for x in range(0,len(fileInput)):
                    if fileInput[x] == inputList[x]:
                        continue
                    elif fileInput[x] !=inputList[x] and x<fileInput.index('from'):
                        content = 'wrong attribute names are selected'
                        break
                    elif fileInput[x]!=inputList[x] and x>fileInput.index('from'):
                        if ("join" and "where" not in inputList) and ("join" and "where"  in fileInput):
                            content = 'Wrong Table name or incomplete query'
                            break
                        if "where" in fileInput and x<fileInput.index('where'):
                            content = 'wrong table is selected'
                            break
                        if ("join" in fileInput and x<fileInput.index('join')) and ("where" not in fileInput):
                            content = 'wrong table is selected'
                            break
                        elif "join" in fileInput and x>fileInput.index('join'):
                            content = 'Join Conditions or where conditions are wrong'
                            break
                        elif "where" in fileInput and x>fileInput.index('where'):
                            content = 'Join Conditions or where conditions are wrong'
                            break
            except:
                content = 'Too few or more keywords or clauses'
            return render_template('task.html', data = user, ques = sc1[1], text =content, username = username)




@app.route('/signin1', methods=['GET', 'POST'])
def signin1():
    global username
    if request.method == 'POST':
        session.pop('user', None)
        email = request.form['email']
        password = request.form['pass']
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="userdata"
            )
        cursor3 = mydb.cursor()
        cursor4 = mydb.cursor()
        cursor3.execute ("select password from signup where emailid= %s",(email,))
        (password1,) = cursor3.fetchone()
        if password == password1:
            cursor4.execute("select name from signup where emailid = %s",(email,))
            (username,)= cursor4.fetchone()
            session['user'] = username
            flash('You were successfully logged in')
            return redirect(url_for('protected'))
        else:
            flash('Invalid username or password. please try again')
            return render_template('sign_in.html')


@app.route('/signup1', methods=['GET', 'POST'])
def signup1():
    global username
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['pass']
        password1 = request.form['re_pass']

        if password != password1:
            flash('Passwords Do Not Match')
            return render_template('sign_up.html')
        else:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="userdata"
            )
            cursor2 = mydb.cursor ()
            cursor2.execute ("insert into signup values (%s,%s,%s)",(username,email,password,))
            return render_template('task.html', username=username)


@app.route('/protected')
def protected():
    if g.user:
        return render_template('task.html',username=username)

    return redirect(url_for('signin1'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']

    return 'Not logged in!'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')


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
    return render_template("task.html", username = username)

@app.route('/course', methods=['GET', 'POST'])
def course():
    return render_template("course.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    return render_template("sign_in.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("sign_up.html")

@app.route('/index1', methods=['GET', 'POST'])
def index1():
    return render_template("index1.html", username=username)

@app.route('/about1', methods=['GET', 'POST'])
def about1():
    return render_template("about1.html", username=username)

@app.route('/custom1', methods=['GET', 'POST'])
def custom1():
    return render_template("custom1.html", username=username)

@app.route('/course1', methods=['GET', 'POST'])
def course1():
    return render_template("course1.html", username=username)

if __name__ == '__main__':
    app.run(debug=True)
