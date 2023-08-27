from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
from config import DB_HOST,DB_NAME,DB_USER,DB_PASS
from models.users import users
from models.expense_head import expense_head
from models.income_head import income_head
from models.record_expense import record_expense
from models.expense_report import expense_report

app = Flask(__name__)
app.secret_key = "expense_tracker"

obj_users=users()
obj_expense_head=expense_head()
obj_income_head=income_head()
obj_record_expense=record_expense()
obj_expense_report=expense_report()

@app.route("/")
def login():
    if 'userid' in session:
        return redirect(url_for("index"))
    else:
        return render_template("login.html")


@app.route("/login_authorize", methods=["POST"])
def login_authorize():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = validate_login_authorize(username,password)
        if error is None:
            try:
                user_id,user_name= obj_users.login_authorize(username,password)
                print(user_id)
                if not user_id:
                    flash("Username or Password is Incorrect")
                    return redirect(url_for("login"))
                else:
                    session['userid'] = user_id
                    # print(session['userid'])
                    session['username'] = user_name
                    # print(session['username'])
                    return redirect(url_for("index"))
            except Exception as error:
                print(error)
                return render_template("error_occured.html")
        else:
            flash(error)
            return redirect(url_for("login"))


@app.route('/logout')
def logout():
    if 'userid' in session:
        session.pop('userid',None)
        session.pop('username',None)
        flash("User Logged Out")
    return render_template('login.html');


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register_user", methods=["POST"])
def register_user():
    if request.method == "POST":
        fullname = request.form["fullname"]
        username = request.form["username"]
        password = request.form["password"]
        error = validate_register_user(fullname,username,password)
        if error is None:
            try:
                obj_users.register_user(fullname,username, password)
                flash("User Added Successflly. Please try logging in.")
                return redirect(url_for("login"))

            except Exception as error:
                print(error)
                return render_template("error_occured.html")
        else:
            flash(error)
            return redirect(url_for("register"))


@app.route("/home")
def index():
    if 'userid' in session:
        return render_template("index.html",res={"username":session['username']})
    else:
        return redirect(url_for("login"))


@app.route("/expense_head")
def expense_head():
    if 'userid' in session:
        try:
            data = obj_expense_head.expense_head(session['userid'])
            return render_template("expense_head.html", res={"username": session['username'],"expense_head":data})
        except Exception as error:
            # print(error)
            # import traceback
            # traceback.print_stack()
            raise error
            return render_template("error_occured.html")
    else:
        return redirect(url_for("login"))

@app.route("/insert_expense_head", methods=["POST"])
def insert_expense_head():
    if request.method == "POST":
        name = request.form["name"]
        error = validate_head(name)
        if error is None:
            try:
                obj_expense_head.insert_expense_head(name,session['userid'])
                flash("Data Inserted Successfully")
                return redirect(url_for("expense_head"))
            except Exception as error:
                print(error)
                print(name)
                return render_template("error_occured.html")
        else:
            flash(error)
            return redirect(url_for("expense_head"))


@app.route("/update_expense_head", methods=["POST", "GET"])
def update_expense_head():
    if request.method == "POST":
        id_data = request.form["id"]
        name = request.form["name"]
        error = validate_head(name)
        if error is None:
            try:
                obj_expense_head.update_expense_head(name, id_data)
                flash("Data Updated Successfully")
                return redirect(url_for("expense_head"))
            except Exception as error:
                print(error)
                return render_template("error_occured.html")
        else:
            flash(error)
            return redirect(url_for("expense_head"))


@app.route("/income_head")
def income_head():
    if 'userid' in session:
        try:
            data = obj_income_head.income_head(session['userid'])
            return render_template("income_head.html", res={"username": session['username'], "income_head": data})
        except Exception as error:
            print(error)
            return render_template("error_occured.html")
    else:
        return redirect(url_for("login"))

@app.route("/insert_income_head", methods=["POST"])
def insert_income_head():
    if request.method == "POST":
        name = request.form["name"]
        error = validate_head(name)
        if error is None:
            try:
                obj_income_head.insert_income_head(name,session['userid'])
                flash("Data Inserted Successfully")
                return redirect(url_for("income_head"))
            except Exception as error:
                print(error)
                print(name)
                return render_template("error_occured.html")
        else:
            flash(error)
            return redirect(url_for("income_head"))


@app.route("/update_income_head", methods=["POST", "GET"])
def update_income_head():
    if request.method == "POST":
        id_data = request.form["id"]
        name = request.form["name"]
        error = validate_head(name)
        if error is None:
            try:
                obj_income_head.update_income_head(name, id_data)
                flash("Data Updated Successfully")
                return redirect(url_for("income_head"))
            except Exception as error:
                print(error)
                return render_template("error_occured.html")
        else:
            flash(error)
            return redirect(url_for("income_head"))


@app.route("/record_expense")
def record_expense():
    if 'userid' in session:
        expense_head_list = obj_expense_head.expense_head(session['userid'])
        income_head_list = obj_income_head.income_head(session['userid'])
        return render_template("record_expense.html",res={"username":session['username'],"expense_head_list":expense_head_list,
                                                          "income_head_list":income_head_list})
    else:
        return redirect(url_for("login"))


@app.route("/insert_record_expense", methods=["POST"])
def insert_record_expense():
    if request.method == "POST":
        amount = request.form["amount"]
        comment = request.form["comment"]
        fromdate = request.form["fromdate"]
        income_head_id = request.form.get('income_head_id')
        expense_head_id = request.form.get('expense_head_id')
        error = validate_insert_record_expense(fromdate,amount,income_head_id,expense_head_id)
        if error is None:
            try:
                obj_record_expense.insert_record_expense(fromdate,amount,comment,income_head_id,expense_head_id,session['userid'])
                flash("Expense Recorded Successfully")
                return redirect(url_for("record_expense"))
            except Exception as error:
                print(error)
                raise error
                return render_template("error_occured.html")
        else:
            flash(error)
            return redirect(url_for("record_expense"))


@app.route("/expense_report", methods=["POST", "GET"])
def expense_report():
    if 'userid' in session:
        try:
            expense_head_list = obj_expense_head.expense_head(session['userid'])
            if request.method == "POST":
                fromdate = request.form["fromdate"]
                todate = request.form["todate"]
                expense_head_id = request.form.get('expense_head_id')
                trans_list = obj_expense_report.expense_report(session['userid'],expense_head_id,fromdate,todate)
                TotalAmt=sum([pair[4] for pair in trans_list])
                return render_template("expense_report.html",res={"username":session['username'],
                                                                  "expense_head_list":expense_head_list,
                                                                  "expense_head_id":expense_head_id,"trans_list":trans_list,
                                                                  "fromdate":fromdate,
                                                                  "todate":todate,"TotalAmt":TotalAmt})
            else:
                return render_template("expense_report.html",res={"username":session['username'],
                                                                  "expense_head_list":expense_head_list})
        except Exception as error:
            print(error)
            return render_template("error_occured.html")
    else:
        return redirect(url_for("login"))


def validate_login_authorize(username,password):
    error = None
    if not username:
        error = "username is required."
    elif not password:
        error = "password is required."
    print(error)
    return error


def validate_register_user(fullname,username,password):
    error = None
    if not fullname:
        error = "fullname is required."
    elif not username:
        error = "username is required."
    elif not password:
        error = "password is required."
    print(error)
    return error


def validate_head(name):
    error = None
    if not name:
        error = "name is required."
    print(error)
    return error


def validate_insert_record_expense(fromdate,amount,income_head_id,expense_head_id):
    error = None
    if not amount:
        error = "amount is required."
    elif not fromdate:
        error = "expense date is required."
    elif not income_head_id:
        error = "income head is required."
    elif not expense_head_id:
        error = "expense head is required."
    print(error)
    return error


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
