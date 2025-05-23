from flask import Flask, render_template, request, redirect, url_for, session,make_response
from flask_cors import CORS
from flask_mysqldb import MySQL
from pytz import timezone
from datetime import datetime
import pytz
import json 
from json import JSONEncoder
from werkzeug.utils import secure_filename
import hashlib

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mcq_management_system'
CORS(app)

app.secret_key = 'your secret key'
mysql = MySQL(app)
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))

import re
def validate_email(email):
    # Regular expression for validating email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)
def validate_password(password):
    if len(password) < 6:
        return False
    return True

@app.route('/',methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/user-login', methods=['GET','POST'])
def login():
    return render_template('student-login.html')

@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    gmail=request.form.get('gmail')
    pwd=request.form.get('pwd')
    cursor=mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM user WHERE Email=%s and UPassword=MD5(%s)''',(gmail,pwd))
    row=cursor.fetchone()
    cursor.close()
    if row:
            uid=str(row[0])
            response = make_response("successfully logged") 
            response.set_cookie('uid',uid)
            return response
    else:
        return "Failed to login"

@app.route('/signup', methods=['GET','POST'])
def signup():
    uname = request.form.get('uname')
    pwd = request.form.get('pwd')
    email = request.form.get('email')

    if not uname:
        return "Username cannot be empty"
    if not validate_email(email):
        return "Invalid Email format"
    if not validate_password(pwd):
        return "Password should be at least 6 characters long"

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE Email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        return "Email already exists"


    cursor.execute(''' INSERT INTO user(Username,UPassword,Email) VALUES(%s,MD5(%s),%s)''',(uname,pwd,email))
    mysql.connection.commit()
    cursor.close()
    return "success"

# admin-login
@app.route('/admin-login',methods=['GET', 'POST'])
def admin_login():
    return render_template('admin-login.html')

@app.route('/admin', methods =['GET', 'POST'])
def admin():
    gmail = request.form.get('gmail')
    password = request.form.get('psw')
    print(gmail, password)
    if gmail == 'admin@gmail.com' and password == 'admin':
        #return redirect(url_for('adminlogin', username=username))
        return ('success')
    else:
        return ('Login failed')
    
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    button_id = request.form['id']
    # You can perform any processing with the button_id here
    return "Button clicked with ID: {}".format(button_id)

@app.route('/forget-password')
def forget_password():
    return render_template('forget-password.html')

@app.route('/nav')
def Nav():
    return render_template('nav.html')

  




@app.route('/qzinsert', methods=['GET', 'POST'])
def qzinsert():
    if request.method == 'POST':
        qname = request.form.get('qname')
        if qname:  
            cursor = mysql.connection.cursor()
            try:
                cursor.execute('''INSERT INTO quiz(QuizTitle) VALUES(%s)''', (qname,))
                mysql.connection.commit()
                cursor.close()
                return "Quiz Name Created Successfully"
            except Exception as e:
                error_message = "Quiz Title Already exist"
                return error_message
        else:
            return "Enter Quiz Name "




@app.route('/qzshow', methods =['GET', 'POST'])
def qzshow():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM quiz")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            elif cnt==3:
                rstr=rstr+"<td>"+"<input type=date id=QZ"+str(ll[cnt])+str(did)+" value="+str(row)+"></td>"  
            else:
                rstr=rstr+"<td>"+"<input type=text id=QZ"+str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=qzupdate("+str(did)+")></i></a></td>"
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=qzdel("+str(did)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function qzupdate(did)
    {
       qtitle=$("#QZB"+did).val();
       
       $.ajax({
        url: \"/qzupdate\",
        type: \"POST\",
        data: {did:did,qtitle:qtitle},
        success: function(data){    
        alert(data);
        loadquizzes();
       }
       });
    }
   
    function qzdel(did)
    {
    $.ajax({
        url: \"/qzdelete\",
        type: \"POST\",
        data: {did:did},
        success: function(data){
            alert(data);
            loadquizzes();
        }
        });
    }
    function loadquizzes(){

       $.ajax({
        url: 'http://127.0.0.1:5000/qzshow',
        type: 'POST',
        success: function(data){
          $('#qzshow').html(data);
        }
      });
    }
    </script>

'''
    return rstr

@app.route('/qnshow', methods =['GET', 'POST'])
def qnshow():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM question")
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr="<table border><tr>"
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Update</th><th>Delete</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
            
            else:
                rstr=rstr+"<td>"+"<input type=text id=QN"+str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"     
            cnt+=1
            
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=qnupdate("+str(did)+")></i></a></td>"
        rstr+="<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=qndel("+str(did)+")></i></a></td>"
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function qnupdate(did)
    {
       qntitle=$("#QNB"+did).val();
       oa=$("#QNC"+did).val();
       ob=$("#QND"+did).val();
       oc=$("#QNE"+did).val();
       od=$("#QNF"+did).val();
       cans=$("#QNG"+did).val();
       
       $.ajax({
        url: \"/qnupdate\",
        type: \"POST\",
        data: {did:did,qntitle:qntitle,oa:oa,oc:oc,od:od,cans:cans},
        success: function(data){    
        alert(data);
        loadquestions();
       }
       });
    }
   
    function qndel(did)
    {
    $.ajax({
        url: \"/qndelete\",
        type: \"POST\",
        data: {did:did},
        success: function(data){
            alert(data);
            loadquestions();
        }
        });
    }
    function loadquestions(){

       $.ajax({
        url: 'http://127.0.0.1:5000/qnshow',
        type: 'POST',
        success: function(data){
          $('#qnshow').html(data);
        }
      });
    }
    
    
    </script>

'''
    return rstr

import html
@app.route('/getallquestions', methods =['GET', 'POST'])
def getallquestions():
    cursor = mysql.connection.cursor()
    quiz_id=request.form.get('quiz_id')
    cursor.execute("SELECT QuestionID,QuestionTitle,OptionA,OptionB,OptionC,OptionD FROM question where QuizID=%s",(quiz_id,))
    row_headers=[x[0] for x in cursor.description] 
    DBData = cursor.fetchall() 
    cursor.close()
    json_data=[]
    rstr='''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"><table border><tr>'''
    for r in row_headers:
        rstr=rstr+"<th>"+r+"</th>"
    rstr=rstr+"<th>Answer</th><th>Update</th></tr>"
    cnt=0
    did=-1
    for result in DBData:
        cnt=0
        ll=['A','B','C','D','E','F','G','H','I','J','K']
        for row in result:
            if cnt==0:
                did=row
                rstr=rstr+"<td>"+str(row)+"</td>" 
        
            else:
                rstr=rstr+"<td>"+html.escape(str(row))+"</td>" 
            
            
            cnt+=1
        rstr+="<td><select id=QZN"+str(did)+"><option>A</option><option>B</option><option>C</option><option>D</option></select></td>"
        rstr+="<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=mqnupdate("+str(did)+")></i></a></td>"
       
        
        rstr=rstr+"</tr>"
    
    rstr=rstr+"</table>"
    rstr=rstr+'''
    <script type=\"text/javascript\">
    function mqnupdate(did)
    {
       ans=$("#QZN"+did).val();
      
       $.ajax({
        url: \"/mqnupdate\",
        type: \"POST\",
        data: {did:did,ans:ans},
        success: function(data){    
        alert(data);
        $("#shBtn").click();
       }
       });
    }
   
        
    </script>

'''
    return rstr


@app.route('/qzupdate', methods =['GET', 'POST'])
def qzupdate():
    
    did=request.form.get('did')
    qtitle = request.form.get('qtitle')
    
    
    cursor = mysql.connection.cursor()
    cursor.execute(''' UPDATE quiz SET QuizTitle=%s WHERE QuizID=%s''',(qtitle,did))
    mysql.connection.commit()
    cursor.close()
    return "Updated successfully"

@app.route('/qnupdate', methods =['GET', 'POST'])
def qnupdate():
    
    did=request.form.get('did')
    qntitle = request.form.get('qntitle')
    oa=request.form.get('oa')
    ob=request.form.get('ob')
    oc=request.form.get('oc')
    od=request.form.get('od')
    cans=request.form.get('cans')
    
    
    cursor = mysql.connection.cursor()
    print(''' UPDATE question SET QuestionTitle=%s,OptionA=%s,OptionB=%s,OptionC=%s,OptionD=%s,Answer=%s WHERE QuestionID=%s''',(qntitle,oa,ob,oc,od,cans,did))
    cursor.execute(''' UPDATE question SET QuestionTitle=%s,OptionA=%s,OptionB=%s,OptionC=%s,OptionD=%s,Answer=%s WHERE QuestionID=%s''',(qntitle,oa,ob,oc,od,cans,did))
    mysql.connection.commit()
    cursor.close()
    return "Updated successfully"

@app.route('/mqnupdate', methods =['GET', 'POST'])
def mqnupdate():
    
    did=request.form.get('did')
    ans = request.form.get('ans')
    uid=request.cookies.get('uid')
    
   
    
    cursor = mysql.connection.cursor()
    #print(''' UPDATE question SET QuestionTitle=%s,OptionA=%s,OptionB=%s,OptionC=%s,OptionD=%s,Answer=%s WHERE QuestionID=%s''',(qntitle,oa,ob,oc,od,cans,did))
    cursor.execute(''' DELETE FROM answer where uid=%s and QuestionID=%s''',(uid,did))
    cursor.execute(''' INSERT INTO answer values (%s,%s,%s)''',(uid,did,ans))
    mysql.connection.commit()
    cursor.close()
    return "Updated successfully"



@app.route('/qzdelete', methods =['GET', 'POST'])
def qzdelete():
    
    did=request.form.get('did')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM quiz WHERE QuizID=%s''',(did,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"

@app.route('/qndelete', methods =['GET', 'POST'])
def qndelete():
    
    did=request.form.get('did')
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM question WHERE QuestionID=%s''',(did,))
    mysql.connection.commit()
    cursor.close()
    return "Deleted successfully"

@app.route('/getquiznames', methods =['GET', 'POST'])

def getquiznames():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM quiz")
    DBData = cursor.fetchall() 
    cursor.close()
    
    rtnames=''
    for result in DBData:
        rtnames+="<option value="+str(result[0])+">"+result[1]+"</option>"
    return rtnames    

@app.route('/questioninsert', methods =['GET', 'POST'])
def questioninsert():
    
    qtitle = request.form.get('qtitle')
    oa = request.form.get('oa')
    ob = request.form.get('ob')
    oc = request.form.get('oc')
    od = request.form.get('od')
    cans = request.form.get('cans')
    qntitle=request.form.get('qntitle')
    cursor = mysql.connection.cursor()
    try:
        cursor.execute(''' INSERT INTO question(QuestionTitle,OptionA,OptionB,OptionC,OptionD,Answer,QuizID) VALUES(%s,%s,%s,%s,%s,%s,%s)''',(qtitle,oa,ob,oc,od,cans,qntitle))
        mysql.connection.commit()
        cursor.close()
        return "Inserted successfully"
    except Exception as e:
        return str(e)







@app.route('/qzshowatn', methods=['GET', 'POST'])
def qzshowatn():

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM quiz")
    row_headers = [x[0] for x in cursor.description]
    DBData = cursor.fetchall()
    cursor.close()
    json_data = []
    "<h1>welcome to the quiz platform</h1>"
    rstr = "<table border><tr>"
    for r in row_headers:
        rstr = rstr+"<th>"+r+"</th>"
    rstr = rstr+"</tr>"
    cnt = 0
    did = -1
    for result in DBData:
        cnt = 0
        ll = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
        for row in result:
            if cnt == 0:
                did = row
                rstr = rstr+"<td>"+str(row)+"</td>"
            elif cnt == 3:
                rstr = rstr+"<td>"+"<input type=date id=QZ" + \
                    str(ll[cnt])+str(did)+" value="+str(row)+"></td>"
            else:
                rstr = rstr+"<td>"+"<input type=text id=QZ" + \
                    str(ll[cnt])+str(did)+" value=\""+str(row)+"\"></td>"
            cnt += 1

        rstr += "<td><a ><i class=\"fa fa-edit\" aria-hidden=\"true\" onclick=qzupdate("+str(
            did)+")></i></a></td>"
        rstr += "<td><a ><i class=\"fa fa-trash\" aria-hidden=\"true\" onclick=qzdel("+str(
            did)+")></i></a></td>"

        rstr = rstr+"</tr>"

    rstr = rstr+"</table>"
    rstr = rstr+'''
    <script type=\"text/javascript\">
    function qzupdate(did)
    {
       qtitle=$("#QZB"+did).val();

       $.ajax({
        url: \"/qzupdate\",
        type: \"POST\",
        data: {did:did,qtitle:qtitle},
        success: function(data){
        alert(data);
        loadquizzes();
       }
       });
    }

    function qzdel(did)
    {
    $.ajax({
        url: \"/qzdelete\",
        type: \"POST\",
        data: {did:did},
        success: function(data){
            alert(data);
            loadquizzes();
        }
        });
    }
    function loadquizzes(){

       $.ajax({
        url: 'http://127.0.0.1:5000/qzshow',
        type: 'POST',
        success: function(data){
          $('#qzshow').html(data);
        }
      });
    }


    </script>

'''
    return rstr

@app.route('/getquizids', methods =['GET', 'POST'])

def getquizids():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM quiz")
    DBData = cursor.fetchall() 
    cursor.close()
    
    rtnames=''
    for result in DBData:
        rtnames+="<option value="+str(result[0])+">"+result[1]+"</option>"
    return rtnames 
  
@app.route('/qnshowatn', methods=['GET', 'POST'])
def qnshowatn():
    if request.method == 'POST':
        quiz_id = request.form.get('quiz_id')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM question WHERE QuizID = %s", (quiz_id,))
        rows = cursor.fetchall()

        # Fetch user details
        cursor.execute("SELECT UserID, Username FROM user")
        users = cursor.fetchall()

        cursor.close()
        return render_template('qn_show.html', rows=rows, users=users)
    else:
        return render_template('qn_show.html', rows=None, users=None)


@app.route('/insert_selected_value', methods=['POST'])
def insert_selected_value():
    question_id = request.form.get('question_id')
    selected_option = request.form.get('selected_option')
    user_id = request.form.get('user_id')  # Get the selected User ID

    # Here you can insert the selected question ID, option, and User ID into the database
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO answer (uid, QuestionID, ans) VALUES (%s, %s, %s)", (user_id, question_id, selected_option))
    mysql.connection.commit()
    cursor.close()
    return "Inserted selected value successfully"



import traceback
@app.route('/scorebord', methods=['GET', 'POST'])
def score():
    if request.method == 'POST':
        quiz_id = request.form.get('quiz_id')
        print("Received quiz ID:", quiz_id) 
        
        try:
            cursor = mysql.connection.cursor()
           
            cursor.execute("SELECT COUNT(*) AS num_questions FROM question WHERE QuizID = %s", (quiz_id,))
            num_questions_result = cursor.fetchone()
            num_questions = str(num_questions_result[0])
            
            cursor.execute("SELECT u.UserID, u.Username, a.QuestionID, a.ans FROM user u JOIN answer a ON u.UserID = a.uid JOIN question q ON a.QuestionID = q.QuestionID WHERE q.QuizID = %s", (quiz_id,))
            user_answers = cursor.fetchall()
            
            scores = {}
            for user in user_answers:
                user_id = str(user[0])
                username = user[1]
                question_id = user[2]
                selected_option = user[3]
                
                cursor.execute("SELECT Answer FROM question WHERE QuestionID = %s", (question_id,))
                correct_answer = cursor.fetchone()[0]
                

                if selected_option == correct_answer:
                    if user_id not in scores:
                        scores[user_id] = {'username': username, 'score': 0}
                    scores[user_id]['score'] += 1
            

            return render_template('score2.html', scores=scores, num_questions=num_questions)
        except Exception as e:
            print("An error occurred:", e)
            print(traceback.format_exc())
            return "An error occurred"
        finally:
            cursor.close()
    else:
        return "nothing"




@app.route('/scorebordid', methods=['GET', 'POST'])
def scoreid():
    return render_template('score3.html')

if __name__ == '__main__':
    app.run(debug=True)
