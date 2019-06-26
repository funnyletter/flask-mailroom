import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donor, Donation

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/add', methods=['GET', 'POST'])
def add():
    # there are too many return statements up in here and I need to
    # clean that ish up.
    # By default we return the main page with all donations.
    output = redirect(url_for('all'))
    if request.method == 'POST':
        # Let's make sure the donation amount is a positive integer...
        less_than_0_error = "Please enter a donation amount greater than 0."
        try:
            amount = int(request.form['amount'])
        except ValueError:
            output = render_template('add.jinja2', error=less_than_0_error)
        if amount <= 0:
            output = render_template('add.jinja2', error=less_than_0_error)
        else:
            name = request.form['name']
            if name:
                try:
                    donor = Donor.select().where(Donor.name == name).get()
                except Donor.DoesNotExist:
                    donor = Donor(name)
                    donor.save()
                donation = Donation(donor=donor, value=amount)
                donation.save()
                output = redirect(url_for('all'))
            else:
                output = render_template(
                    'add.jinja2',
                    error='Please enter a donor name.'
                    )
    else:
        output = render_template('add.jinja2')

    return output

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

