
from flask import Flask
from flask import render_template
import os
from flask import safe_join, send_from_directory


PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__,
    template_folder=os.path.join(PROJECT_PATH, 'templates'),
    static_folder=PROJECT_PATH)


@app.route('/assets/<any(css, i, js, sound,fonts):folder>/<path:filename>')
def toplevel_static(folder, filename):
    folder = safe_join('assets/'+folder)
    filename = safe_join(folder, filename)
    cache_timeout = app.get_send_file_max_age(filename)
    return send_from_directory(app.static_folder, filename,
                               cache_timeout=cache_timeout)


@app.route('/')
def index():
    return render_template("mainpage.html")


@app.route('/Yieldcurve')
def yieldcurve():
    return render_template("yieldCurvePage.html")


@app.route('/calculator')
def calculator():
    return render_template("calculatorPage.html")


if __name__ == "__main__":
    app.debug = True
    app.run(port=31540, host='0.0.0.0')