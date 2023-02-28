import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
## WORK NEEDED HERE ##
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route('/')
def welcome():
    return (
        f'<h1><center>Welcome to the Climate App!</center></h1>'
        f'<h2><center>Available Routes:</center><h2>'
        f'<ol><ul><a href=http://127.0.0.1:5000/api/v1.0/precipitation>'
        f'http://127.0.0.1:5000/api/v1.0/precipitation</a></ul><br/>'
        f'<ul><a href=http://127.0.0.1:5000/api/v1.0/stations>'
        f'http://127.0.0.1:5000/api/v1.0/stations</a></ul><br/>'
        f'<ul><a href=http://127.0.0.1:5000/api/v1.0/tobs>'
        f'http://127.0.0.1:5000/api/v1.0/tobs</a></ul><br/>'
        f'<ul><a href=http://127.0.0.1:5000/api/v1.0/temp/<start>'
        f'http://127.0.0.1:5000/api/v1.0/temp/<start></a></ul><br/>'
        f'<ul><a href=http://127.0.0.1:5000/api/v1.0/temp/<start>/<end>'
        f'http://127.0.0.1:5000/api/v1.0/temp/<start>/<end></a></ul><br/>'

)



@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    session.close()

    prec_dict = {}
    for i in precipitation:
        prec_dict[i[0]] = i[1]
    
    
    # Dict with date as the key and prcp as the value
    ## WORK NEEDED HERE ##
    return jsonify(prec_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    results = session.query(Station.station).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    stations = list(np.ravel(results))
    print(stations)
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperature observations (tobs) for previous year."""
    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the primary station for all tobs from the last year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()

    session.close()
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))

    # Return the results
    return jsonify(temps=temps)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

     # calculate TMIN, TAVG, TMAX with start and stop
    if end != None:
        temps = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        session.close()
        # # Unravel results into a 1D array and convert to a list
        temps = list(np.ravel(temps))
        return jsonify(temps)
    
     # calculate TMIN, TAVG, TMAX with just start
    else:
    
        temps = session.query(*sel).\
            filter(Measurement.date >= start).all()

        session.close()

        temps = list(np.ravel(temps))
        return jsonify(temps)

    
if __name__ == '__main__':
    app.run(debug=True)
