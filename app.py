from flask import Flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

last_date_qry = session.query(Measurement.date).\
    order_by(Measurement.date.desc()).first()
last_date = last_date_qry[0]
lastDate = dt.datetime.strptime(last_date, '%Y-%m-%d').date()
year_ago = lastDate - dt.timedelta(days = 365)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/name<br/>"
        f"/api/v1.0/prcp<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/datesearch/<startDate>"
        f"/api/v1.0/datesearch/<startDate>/<endDate>"
        
        
    )

    
@app.route("/api/v1.0/name")
def name():
    session = Session(engine)
    results = session.query(Station.name).all()
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/prcp")
def prcp():
    
    session = Session(engine)
    results = session.query(Measurement.prcp, Measurement.date, Measurement.station)\
              filter(Measurement.date > year_ago).order_by(Measurement.date).all()
    prcp_data = []
    for result in results:
        prcp_dict = {result.date: result.prcp, "Station": result.station}
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs, Measurement.station, Station.name)\
            .filter(Measurement.date > year_ago).\
            filter(Measurement.station == Station.station).\
                    order_by(Measurement.date).all()
    tobs_data = []
    for result in results:
        tobs_dict = {"Date":result.date, "Temperature (degree F)": result.tobs, "Station":result.station, "Station Name": result.name}
        tobs_data.append(tobs_dict)
    

    return jsonify(tobs_data)

 @app.route("/api/v1.0/datesearch/<startDate>")
def start(startDate):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)]
    results = session.query(*sel).\
        filter(func.strftime("%Y-%m-%d", Measurement.date)>= startDate).\
        group_by(Measurement.date).all()
    temp = []

    for result in results:
        temp_dict = {}
        temp_dict['Date'] = result[0]
        temp_dict['tmin'] = result[1]
        temp_dict['tavg'] = round(result[2],2)
        temp_dict['tmax']= result[3]
        temp.append(temp_dict)
    return jsonify(temp)


    @app.route("/api/v1.0/datesearch/<startDate>/<endDate>")
def start_end(startDate, endDate):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)]
    results = session.query(*sel).\
        filter(func.strftime("%Y-%m-%d", Measurement.date)>= startDate).\
        filter(func.strftime("%Y-%m-%d", Measurement.date)<= endDate).\
        group_by(Measurement.date).all()
    temp = []

    for result in results:
        temp_dict = {}
        temp_dict['Date'] = result[0]
        temp_dict['tmin'] = result[1]
        temp_dict['tavg'] = round(result[2],2)
        temp_dict['tmax']= result[3]
        temp.append(temp_dict)
    return jsonify(temp)



if __name__ == "__main__":
    app.run(debug=True)


