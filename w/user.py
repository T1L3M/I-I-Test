"""---------หน้า Login, Regis--------------"""

import formatter
from flask import Blueprint,render_template,request,redirect,session,flash, sessions
from flask import url_for
import pymysql
from config import *
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField
from flask_uploads import configure_uploads, IMAGES, UploadSet

app = Flask(__name__)

con = pymysql.connect(host=HOST,
                      user=USER,
                      password=PASS,
                      database=DATABASE)

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

class MyForm(FlaskForm):
    image = FileField('image')

user = Blueprint('user',__name__)


@user.route("/login")
def Loginpage():
    if "username" not in session:
        return render_template("login.html")
    else:
        return redirect(url_for('dash.Showusermanage'))



@user.route("/checklogin",methods=["POST"])
def Checklogin():
    username = request.form['username']
    password = request.form['password']
    with con:
        cur = con.cursor()
        sql = "SELECT * FROM tb_user WHERE usr_username = %s AND usr_userpassword = %s and usr_status=1"
        cur.execute(sql,(username,password))
        rows = cur.fetchall()
        cur.close()
        if len(rows) > 0:
            session['username'] = username
            session['fname'] = rows[0][1]
            session['lname'] = rows[0][2]
            session.permanent = True
            return redirect(url_for('dash.Showusermanage'))
        else:
            flash("ไม่พบผู้ใช้นี้ในระบบ โปรดกรอกข้อมูลอีกครั้ง")
            return render_template('login.html')


@user.route("/logoff")
def Logoff():
    session.clear()
    print(session)
    return redirect(url_for('user.Loginpage'))


        
@user.route("/regis")
def Regisuser():
    return render_template("/regis.html")



@user.route("/adduser",methods=['GET', 'POST'])
def Adduser():
    if request.method == "POST":
     fname=request.form["fname"]
     lname=request.form["lname"]
     username=request.form["username"]
     password=request.form["password"]
     repassword=request.form["repassword"]
     if password != repassword:
        flash("Password ไม่ตรงกับ Re-password")
    def index():
     form = MyForm()
     if form.validate_on_submit():
        imgfile = images.save(form.image.data)
        imgfile=request.form["imgfile"]
        return f'Filename: {imgfile}'
     return render_template('regis.html')
  
    
        
    with con:
        cur = con.cursor()
        sql = "insert into tb_user(usr_fname,usr_lname,usr_username,usr_userpassword,) VALUES (%s,%s,%s,%s)"
        cur.execute(sql,(fname, lname, username, password, ))
        con.commit()
        flash(fname+" สมัครสมาชิกแล้ว")
    return redirect(url_for('user.Loginpage'))
    



@user.route("/addnewuser",methods=["POST"])
def Addnewuser():
    if request.method == "POST":
     fname=request.form["fname"]
     lname=request.form["lname"]
     username=request.form["username"]
     password=request.form["password"]
     def index():
      form = MyForm()
      if form.validate_on_submit():
        imgfile = images.save(form.image.data)
        imgfile=request.form["imgfile"]
        return f'Filename: {imgfile}'
    with con:
        cur = con.cursor()
        sql = "insert into tb_user(usr_fname,usr_lname,usr_username,usr_userpassword) VALUES (%s,%s,%s,%s)"
        cur.execute(sql,(fname, lname, username, password))
        con.commit()
        return redirect(url_for('dash.Showusermanage'))




"""---------------------หน้า user edit--------------------"""

@user.route("/useredit")
def Showusermanage():
    if "username" not in session:
        return render_template('login.html')
    with con:
        cur = con.cursor()
        sql = "SELECT * FROM tb_user"
        cur.execute(sql)
        rows = cur.fetchall()
        print(rows)
        # return "ok"
        return render_template("useredit.html", datas=rows)


@user.route("/edituser", methods=["POST"])
def Edituser():
    if request.method == "POST":
        id = request.form["id"]
        status = request.form["status"]

        with con:
            cur = con.cursor()
            sql = "update tb_user set usr_status = %s WHERE usr_id = %s"
            cur.execute(sql, (status,id))
            con.commit()
            #rows = cur.fetchall()
            # print(rows)
            return redirect(url_for("user.Edituser"))