# Import dependencies
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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query precipitation
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    sel = [Measurement.date, Measurement.prcp]
    last_12_precip = session.query(*sel).filter(Measurement.date >= last_year).order_by(Measurement.date).all()


    session.close()

    precip_12 = dict(last_12_precip)

    return jsonify(precip_12)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query stations
    sel = [Station.station]
    station = session.query(*sel).all()


    session.close()

    station_list = list(np.ravel(station))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query tobs
    station_name = Measurement.station
    station_count = func.count(Measurement.station)
    most_active_station = session.query(station_name, station_count).group_by(station_name).order_by(station_count.desc()).first()
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    sel = [Measurement.date, Measurement.tobs]
    last_12_tobs = session.query(*sel).filter(Measurement.date >= last_year).filter(Measurement.station == most_active_station[0]).order_by(Measurement.date).all()


    session.close()

    tobs_list = dict(last_12_tobs)

    return jsonify(tobs_list)

@app.route("/api/v1.0/start")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query start
    start_date = dt.date(2017,6,27)
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    starts = session.query(*sel).filter(Measurement.date >= start_date).all()

    session.close()

    
    start_list = list(np.ravel(starts))

    return jsonify(start_list)
    
    
@app.route("/api/v1.0/start/end")
def end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query end
    start_date = dt.date(2017,6,27)
    end_date = dt.date(2017,7,7)
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    ends = session.query(*sel).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    end_list = list(np.ravel(ends))

    return jsonify(end_list)

if __name__ == "__main__":
    app.run(debug=True)