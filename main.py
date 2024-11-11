from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/store", methods=["POST"])
def store():
    with open("details.txt", "a+") as file:
        for dictionary in request.json:
            file.write(f"X: {dictionary['x']}, Y: {dictionary['y']}, Time: {dictionary['t']}s\n")
    return "200"


@app.route('/calibration')
def calibration():
    return render_template("calibration.html")


@app.route("/test_code")
def test_code():
    return render_template("test_code.html")


if __name__ == "__main__":
    app.run(debug=True)
