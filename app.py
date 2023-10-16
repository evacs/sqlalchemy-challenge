# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Global variables:
# Calculate the date one year from the last date in data set.
year_before = dt.date(2016, 8, 23)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    # Start at the homepage.
   # List all the available routes.
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) 
    # to a dictionary using date as the key and prcp as the value.
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_before).all()
    session.close()
    precip_dict = {date: prcp for date, prcp in results}
    # Return the JSON representation of your dictionary.
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    results = session.query(Station.station).all()
    session.close()
    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    max_station = 'USC00519281'
    results = session.query(Measurement.tobs).filter(Measurement.station == max_station).\
    filter(Measurement.date >= year_before).all()
    session.close()
    # Return a JSON list of temperature observations for the previous year.
    tobs = list(np.ravel(results))
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start_temp(start):
    # For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    start = dt.datetime.strptime(start, "%m%d%Y")
    results = session.query(*sel).filter(Measurement.date >= start).all()
    session.close()

    temps = list(np.ravel(results))
    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def range_temp(start,end):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date
    #  to the end date, inclusive.
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    temps = list(np.ravel(results))
    return jsonify(temps)







if __name__ == '__main__':
    app.run()