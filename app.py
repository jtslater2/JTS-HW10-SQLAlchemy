import numpy as np

import sqlalchemy
import pandas as pd
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
        f"/api/v1.0/start<start><br/>"
        f"/api/v1.0/start/end/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def prec():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > '2016-08-23')\
        .filter(Measurement.prcp >= 0)\
        .order_by(Measurement.date).all()

    session.close()

    #n_date = [result[0] for result in results]
    #n_prcp = [int(result[1]) for result in results]

    #df = pd.DataFrame(results, columns=['n_date','n_prcp'])

    #df.set_index('n_date', inplace=True, )
    #df2 = df.groupby(['n_date']).mean().reset_index()

    #Create a dictionary from the row data and append to a list of all_passengers
    all_prec = []
    for date, prcp in results:
        prec_dict = {}
        prec_dict["date"] = date
        prec_dict["prcp"] = prcp
        all_prec.append(prec_dict)

    return jsonify(all_prec)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of staions"""
    # Query all 
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    most = "USC00519281"
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date > '2016-08-23')\
        .filter(Measurement.station == most)\
        .order_by(Measurement.date).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/start/<start>")
def fdate(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)\
            .filter(Measurement.date >= start)).first()
        
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    #all_st = []
    #for min, max, avg in results:
    #    all_dict = {}
    #    all_dict["min"] = min
    #    all_dict["max"] = max
    #    all_dict["avg"] = avg
    #    all_st.append(all_dict)

    return jsonify(results)

@app.route("/api/v1.0/start/end/<start>/<end>")
def fldate(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)\
            .filter(Measurement.date >= start)\
            .filter(Measurement.date <= start)).first()
        
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    #all_st = []
    #for min, max, avg in results:
    #    all_dict = {}
    #    all_dict["min"] = min
    #    all_dict["max"] = max
    #    all_dict["avg"] = avg
    #    all_st.append(all_dict)

    return jsonify(results)















if __name__ == '__main__':
    app.run(debug=True)
