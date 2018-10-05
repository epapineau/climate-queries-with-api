# Import dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, and_, distinct
import datetime as dt

# Build and connect to ORM
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Establish flask app
app = Flask(__name__)

# Routes
@app.route("/")
def home():
    return (
        f"Welcome to an API!<br/>"
        f"Available Routes <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end> <br/>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Set start and end dates    
    date_start = dt.date.today() - dt.timedelta(days = 365)
    date_end = dt.date.today() - dt.timedelta(days = (365 * 2))
    
    # Query for date and precipitation values
    q = session.query(Measurement.prcp, Measurement.date).filter(and_(Measurement.date <= date_start, Measurement.date >= date_end))

    # Build dictionary
    precip_dict = {}
    for row in q:
        precip_dict[row[1]] = row[0]

    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Query for unique station list
    q = session.query(distinct(Measurement.station))
    stations = [row[0] for row in q]

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_observations():
    # Set start and end dates    
    date_start = dt.date.today() - dt.timedelta(days = 365)
    date_end = dt.date.today() - dt.timedelta(days = (365 * 2))

    # Query for temperature observations
    q = session.query(Measurement.tobs).filter(and_(Measurement.date <= date_start, Measurement.date >= date_end))
    temp_obs = [row[0] for row in q]

    return jsonify(temp_obs)

@app.route("/api/v1.0/<start>")
def start(start):
    # Query for minimum, average, and maximum temperature observations
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    q = session.query(*sel).filter(Measurement.date <= start)
    temp = [row for row in q]

    return jsonify(temp)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Query for minimum, average, and maximum temperature observations
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    q = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end)
    temp = [row for row in q]

    return jsonify(temp)

if __name__ == "__main__":
    app.run(debug=True)