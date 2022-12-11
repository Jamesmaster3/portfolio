from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)


# def write_contact_to_file(data):
#     try:
#         email = data['email']
#         subject = data['subject']
#         message = data['message']
#         # now i can easily create an Excel database if i want
#         with open('database.txt', 'a') as f:
#             f.write(f'\n {email}, {subject}, {message}')
#             f.close()
#             return 'done'
#     except:
#         return 'error'

def write_to_CSV(data):
    email = data['email']
    subject = data['subject']
    message = data['message']
    with open('database.csv', mode='a', newline='') as f2:
        writer = csv.writer(f2, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        writer.writerow([email, subject, message])


@app.route("/")
def my_home():
    return render_template('index.html')


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_CSV(data)
            return redirect('thankyou.html')
        except:
            return 'did not save to database'
    else:
        return 'Something went wrong, try again'


# write to txt file

# with open('database.txt', 'a') as f:
#     for k, v in data.items():
#         f.write(str((k, v)))
#     f.close()
