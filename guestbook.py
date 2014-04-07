import datetime

from flask import Flask, flash, redirect, render_template, request, session


app = Flask(__name__)
entries = []
entry_names = []
entry_dates = []


@app.route('/')
def index():
    return render_template(
        'index.html', entries=zip(entry_names, entry_dates, entries))

@app.route('/submit', methods=['POST'])
def submit():
    entries.append(request.form['entry'] or '<blank>')
    if not request.form['name']:
        flash("you must provide a name!")
        return redirect('/')
    entry_names.append(request.form['name'])
    entry_dates.append(datetime.datetime.now())
    return redirect('/')

@app.route('/admin')
def admin_login():
    return render_template('login.html')

@app.route('/admin', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return admin_login()

@app.route('/moderate', methods=['POST'])
def moderate_posts():
    for key in request.form:
        if not key.startswith('delete_'):
            continue
        index = int(key.partition('_')[2])
        del entries[index]
        del entry_names[index]
    return redirect('/')


if __name__ == '__main__':
    import os
    app.secret_key = os.urandom(12)
    app.run(debug=True)
