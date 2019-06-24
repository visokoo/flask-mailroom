import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)
 
    
@app.route('/create/', methods=['GET','POST'])
def create():
    error = None
    if request.method == 'POST':
        name, amount = request.form['name'], int(request.form['amount'])
        existing_donor = Donor.select().where(Donor.name == name.capitalize()).first()
        if existing_donor:
            Donation(donor=existing_donor, value=amount).save()
        else:
            # create new donor if existing one cannot be found
            new_donor = Donor(name=name).save()
            Donation(donor=new_donor, value=amount).save()
        return redirect(url_for('home'))
    return render_template('create.jinja2')


@app.route('/donations/filter', methods=['GET','POST'])
def donation_by_donor():
    filter, error = None, None
    if request.method == 'POST':
        try:
            name = request.form['name']
            donor = Donor.select().where(Donor.name == name.capitalize()).first()
            filter = Donation.select().where(Donation.donor == donor.id)
            return render_template('donations.jinja2', donations=filter)
        except AttributeError as e:
            error = f"User {name} cannot be found, please verify entry"
    return render_template('donations_by_donor.jinja2', donations=filter, error=error)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

