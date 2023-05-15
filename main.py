from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import URLField, TimeField, DateField
from wtforms.validators import DataRequired, URL
import csv
import os
import pandas as pd

#API imports
import requests
import smtplib

FLIGHT_API_KEY='w_B_iJfs9eehraYvVX8QyS7flHSPO7YR'
FLIGHT_API_ENDPOINT='https://api.tequila.kiwi.com/search'
headers = {'apikey': FLIGHT_API_KEY}
# params = {'fly_from': 'DUS'
#     , 'fly_to': destination['iataCode']
#     , 'date_from': '19/04/2023'
#     , 'date_to': '26/05/2023'
#     , 'price_to': destination['lowestPrice']
#           }

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class FlightForm(FlaskForm):
    from_city = StringField(label='From', validators=[DataRequired()])
    to_city = StringField(label='To', validators=[DataRequired()])
    departure_time = DateField(label='Departure', validators=[DataRequired()])
    return_time = DateField(label='Return', validators=[DataRequired()])
    price = StringField(label='Your Price', validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_flight():
    global travel_link
    form = FlightForm()
    if form.validate_on_submit():

        new_city_info = [form.from_city.data, form.to_city.data, form.departure_time.data,
                         form.return_time.data,form.price.data]
        df = pd.read_csv('3-letter-city.csv')
        row_from = df.loc[df['city name'] == form.from_city.data]
        value_from = row_from['city code'].to_string()
        iata_code_from=value_from.split(' ')[4]
        row_to = df.loc[df['city name'] == form.to_city.data]
        value_to = row_to['city code'].to_string()
        iata_code_to=value_to.split(' ')[4]


        #etelaat e tooye new_city_info bayad formatash mese paeen beshe
        params = {'fly_from':iata_code_from  # 'DUS'
        , 'fly_to':iata_code_to #destination['iataCode']
        , 'date_from':form.departure_time.data.strftime('%d/%m/%Y') #'19/04/2023'
        , 'date_to':form.return_time.data.strftime('%d/%m/%Y') #'26/05/2023'
        , 'price_to': form.price.data#destination['lowestPrice']
        }
        print(new_city_info)
        print(params)

        print(f"########### CITY: {form.from_city.data} ##########")
        flight_response=requests.get(url=FLIGHT_API_ENDPOINT,params=params,headers=headers)
        flight_response.raise_for_status()
        flight_content=flight_response.text
        flight_data=flight_response.json()
        if not flight_data['data'] :
            print("Sorry,no flight with this budget for {destination['city']}")
        else:
            print('congratulation we find you a flight')
            print(flight_data['data'][0]['deep_link'])
            travel_link=flight_data['data'][0]['deep_link']
            # inform user via email
            connection=smtplib.SMTP('smtp.gmail.com',port=587)
            connection.starttls()
            connection.login(user='trytestpython2023@gmail.com',password='pfslkpnaeseetlkx')
            TEXT=f"we found you a flight from {form.from_city.data} to {form.to_city.data} with {flight_data['data'][0]['price']} $"

            message = 'Subject: {}\n\n{}'.format('AFFORDABLE FLIGHT', TEXT)
            connection.sendmail(from_addr='trytestpython2023@gmail.com',to_addrs='rezaee.parvin89@gmail.com',
                                msg=message)
            connection.close()
        new_city_api_info=[iata_code_from,iata_code_to,form.departure_time.data.strftime('%d/%m/%Y')
                           ,form.return_time.data.strftime('%d/%m/%Y'),
                           form.price.data,travel_link]
        with open('flight-data.csv', 'a',newline='') as flight_data:
            writer = csv.writer(flight_data)
            writer.writerow(new_city_api_info)
        print("True")
    # Make the form write a new row into flight-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/flights')
def flights():
    with open('flight-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
            # params = {'fly_from': row[0]  # 'DUS'
            #     , 'fly_to': row[1]  # destination['iataCode']
            #     , 'date_from': row[2]  # '19/04/2023'
            #     , 'date_to': row[3]  # '26/05/2023'
            #     , 'price_to': row[4]  # destination['lowestPrice']
            #           }
    return render_template('flights.html', flights=list_of_rows)


if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), debug=True,
            port=int(os.getenv('PORT', 5002)))
