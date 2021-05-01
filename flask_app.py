
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for
import model
app = Flask(__name__)
comments = []
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=comments)


    recom = model.newRecommendations_50(request.form["contents"])
    comments.append(recom)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()

