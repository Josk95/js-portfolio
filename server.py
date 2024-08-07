from flask import Flask, render_template, send_from_directory, request, redirect,url_for, session
import  csv

app = Flask(__name__)
app.secret_key = 'ThisIsMyVerySecretKey'  # Replace with a strong secret key


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/<page_name>")
def html_page(page_name):
    name = session.get('name')
    # Optionally clear the name from the session after use
    session.pop('name', None)
    return render_template(f'{page_name}.html', name=name)

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        name = data['name']
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\nName: {name}, Email: {email}, Subject: {subject}, Message {message}')



def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as csv_database:
        name = data['name']
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(csv_database,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name,email, subject, message])



@app.route('/submit_contact_form', methods=['POST', 'GET'])
def submit_contact_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            session['name'] = data.get('name', '')
            write_to_csv(data)
            return redirect(url_for('html_page', page_name='/thankyou'))
        except:
            return 'did not save to database'
    else:
        return 'something went wrong'




