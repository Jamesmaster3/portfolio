from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from scrape_hackernews import run_hackernews
import csv

# flask --app server.py --debug run

def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    return app


app = create_app()


def write_to_CSV(data):
    name = data['name']
    email = data['email']
    message = data['message']
    with open('portofolio/database.csv', mode='a', newline='') as f2:
        writer = csv.writer(f2, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        writer.writerow([name, email, message])


@app.route("/")
def my_home():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_CSV(data)
            return redirect('index.html')
        except:
            return 'did not save to database'
    else:
        return 'Something went wrong, try again'


@app.route('/hackernews', methods=['POST', 'GET'])
def request_hackernews():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            pages = data['pages']
            top_posts = run_hackernews(int(pages))
            #return str(top_posts)
            return render_template('hackernews_pages.html', result=top_posts, pages=pages)
        except:
            return 'Couldn\'t get latest posts'
    else:
        return 'Something went wrong, try again'
