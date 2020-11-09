# This script creates a Flask API to store and retrieve climate data from Hawaii.

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route('/')
def home():
    print("Requesting home page...")
    return(
        f'Available Routes<br/>'
        f'<hr/>'
        f'Precipitation measured by day: /api/v1.0/precipitation<br/>'
        f'List of stations: /api/v1.0/stations<br/>'
        f'Dates and temperature observations of most active station: /api/v1.0/tobs<br/>'
        f'Min, avg and max temperatures on or after given date: /api/v1.0/<start><br/>'
        f'Min, avg and max temperatures for date range: /api/v1.0/<start>/<end><br/>'
    )
#TODO Figure out what to do about multiple dates/dict keys are dates
#TODO group by date and determine avg. temp for each date
@app.route('/api/v1.0/precipitation')
def precipitation():
    print('Requesting precipitation data...')
    # Connect to database
    session = Session(engine)

    # Determine date that is one year from latest date in dataset
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_date_dt = dt.datetime.strptime(last_date, '%Y-%m-%d')
    year_ago = last_date_dt - dt.timedelta(days=366)

    # Pull data from database
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    session.close()

    # Store data in list of dictionaries
    precipitation_data = []
    for date, prcp in results:
        date_dict = {}
        date_dict[date] = prcp
        precipitation_data.append(date_dict)

    # Return data in JSON format
    return jsonify(precipitation_data)

# Call all data from station table
@app.route('/api/v1.0/stations')
def stations():
    print('Requesting station data')
    # Pull data from database
    session = Session(engine)
    results = session.query(Station.name).all()
    session.close()

    # Store data in list
    all_stations = list(np.ravel(results))

    # Return data in JSON format
    return jsonify(all_stations)

@app.route('/api/v1.0/tobs')
def tobs():
    print('Requestion tobs data')

    # Connect to database
    session = Session(engine)

    # Determine date that is one year from latest date in dataset
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_date_dt = dt.datetime.strptime(last_date, '%Y-%m-%d')
    year_ago = last_date_dt - dt.timedelta(days=366)

    # Determine most active station
    most_active = session.query(Measurement.station, func.count(Measurement.id)\
        .label('frqcy'))\
        .group_by(Measurement.station)\
        .order_by(desc('frqcy')).all()

    # Pull data from database
    results = session.query(Measurement.date, Measurement.tobs)\
                    .filter(Measurement.date >= year_ago)\
                    .filter(Measurement.station == most_active[0][0])\
                    .all()
    session.close()

    # Store data in list of dictionaries
    temp_data = []
    for date, tobs in results:
        date_tuple = (date, tobs)
        temp_data.append(date_table)
    
    # Return data in JSON format
    return jsonify(temp_data)

@app.route('/api/v1.0/<start>')
def by_date(start):
    start_date = start.replace("<", "").replace(">", "")
    # Pull data from database
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()

    # Store data in list of dictionaries
    temp_data = {}
    temp_data['Min Temp'] = results[0][0]
    temp_data['Avg Temp'] = results[0][1]
    temp_data['Max Temp'] = results[0][2]

    # Return data in JSON format
    return jsonify(temp_data)
    
@app.route('/api/v1.0/<start>/<end>')
def by_date_range(start, end):
    start_date = start.replace("<", "").replace(">", "")
    end_date = end.replace("<", "").replace(">", "")
    # Pull data from database
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()

    # Store data in list of dictionaries
    temp_data = {}
    temp_data['Min Temp'] = results[0][0]
    temp_data['Avg Temp'] = results[0][1]
    temp_data['Max Temp'] = results[0][2]

    # Return data in JSON format
    return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True)