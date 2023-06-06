from flask import Flask, request, render_template
#Flask is a Class
app = Flask(__name__)
#decorator
@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        #for debugging’s sake
        print("from submitted!")
        color = request.form.get("color")
        return render_template("color.html", color = color)