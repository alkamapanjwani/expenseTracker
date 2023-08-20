from flask import Flask, render_template

# from markupsafe import escape


# from

app = Flask(__name__)

app.secret_key = "flash_messages"


@app.route("/")
def index():
    return render_template("login.html")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
