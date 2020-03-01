import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect,desc
from flask import send_file
import json

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
postgresStr = ("postgresql://postgres:password@localhost:5432/climateanalysis")
engine = create_engine(postgresStr)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurement
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


    """List all routes that are available."""
    return (
        f"<b><u><center><h1> Hawaii Precipitation and Weather Data</h1><br/></br></br></</b></center></u>"
        "<h3>Pick from the available routes below:</h3>"
        f"Precipitation analysis from 2016-08-23 to 2017-08-23.&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;<body><i><u><a target='_blank' href ='http://localhost:5000/api/v1.0/precipitation'>Precipitation</a></i></u>&emsp;&emsp;</body></br></br>"
        f"Stations Names and Location&emsp;&emsp;&emsp;&nbsp;&nbsp;<i><u><a target='_blank' href='http://localhost:5000/api/v1.0/stations'>Stations</a><br/></i></u></br>"
        f"Temperature tobs for one date&emsp;&emsp;&emsp;<i><u><a target='_blank' href='http://localhost:5000/api/v1.0/tobs'>Temperature Observation</a><br/></i></u></br>"
        f"All Temperature observations&emsp;&emsp;&emsp;<i><u><a target='_blank' href='http://localhost:5000/api/v1.0/alltobs'>All Temperature Observation</a><br/></i></u></br>"
        f"Type in single date&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&emsp;<i><u>http://localhost:5000/api/v1.0/temp/startdate</i></u>&emsp;&emsp;<a target='_blank' href='http://localhost:5000/api/v1.0/temp/20160326'>Example_Temp_SingleDate</a></body></br></br>"
        f"Type in date range with start date and end date&emsp;&emsp;&emsp;&emsp;&emsp;<i><u>http://localhost:5000/api/v1.0/temp/<start>/<end></i></u>&emsp;&emsp;<a target='_blank' href='http://localhost:5000/api/v1.0/temp/20150326/20160826'>Example_Temperature_DateRange</a></br></br>"
        f"<img src='https://hawaii.kauai.com/images/hideaways-princeville.jpg'>"
        
        
    )


        


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all precipitation names"""
    # Query all precipitation
    results = session.query(Measurements.date,Measurements.prcp).filter(Measurements.date > '2017-03-20').order_by(Measurements.date).all()

    session.close()
    # Convert list of tuples into normal list
    all_precipitation = list(np.ravel(results))

    
# Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date,prcp in results:
        precipitation_dict = {}
        precipitation_dict["Date"] = date
        precipitation_dict["Precipitation"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

    
    
#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    

    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all Stations names"""
    # Query all station
    results = session.query(Station.station,Station.latitude,Station.longitude,Station.name).all()
    session.close()
    all_station =list(np.ravel(results))
# Create a dictionary from the row data and append to a list of all_precipitation
    all_stations = []
    for station,latitude,longitude,name in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Latitude"] = latitude
        station_dict["Longitude"]=longitude
        station_dict["Name"]=name
        
        all_stations.append(station_dict)    
    
    return jsonify(all_stations)
    


# `/api/v1.0/tobs`
  # query for the dates and temperature observations from a year from the last data point.
  # Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route("/api/v1.0/tobs")
def temp_observation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all date and temperature wthin a date range"""
    # Query all tobs based on the date range
    results = session.query(Measurements.date,Measurements.tobs).filter(Measurements.date > '2016-07-23').filter(Measurements.date <='2017-07-23').order_by(Measurements.date).all()

    session.close()
    # Convert list of tuples into normal list
    all_temp_observation = list(np.ravel(results))

    
# Create a dictionary from the row data and append to a list of all_precipitation
    all_temp_observation = []
    for date,tobs in results:
        temp_observation_dict = {}
        temp_observation_dict["Date"] = date
        temp_observation_dict["Temperature Observation"] = tobs
        all_temp_observation.append(temp_observation_dict)

    return jsonify(all_temp_observation)
    
#Return all tobs for the dates in the table

@app.route("/api/v1.0/alltobs")
def alltobs():

# Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all precipitation names"""
    # Query all tobs
    results = session.query(Measurements.date,Measurements.tobs).all()

    session.close()
    # Convert list of tuples into normal list
    alltobs = list(np.ravel(results))
    
# Create a dictionary from the row data and append to a list of all_precipitation
    all_tobs_data = []
    for date,tobs in results:
        all_tobs_dict = {}
        all_tobs_dict["Date"] = date
        all_tobs_dict["Temperature Observation"] = tobs
        all_tobs_data.append(all_tobs_dict)
    return jsonify(all_tobs_data)

#Return min(tobs),max(tobs),avg(tobs) for a start date

@app.route("/api/v1.0/temp/<start>")
def temp_stats_start(start):
    print("Server is trying to get startdate provide one in the url")
# Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(func.min(Measurements.tobs).label('min'),func.avg(Measurements.tobs).label('avg'),func.max(Measurements.tobs).label('max')).filter(Measurements.date >= start).all()
    

    start_stats_data = []
    for result in results:
        start_stats_dict = {}
        start_stats_dict['Start Date'] = start
        start_stats_dict['Min Temp'] = float(result[1])
        start_stats_dict['Avg Temp'] = float(result[0])
        start_stats_dict['Max Temp'] = result[2]
        start_stats_data.append(start_stats_dict)
    
    return jsonify(start_stats_data)
    
    
#Return min(tobs),max(tobs),avg(tobs) for a start date and end date
@app.route("/api/v1.0/temp/<start>/<end>")
def temp_stats_start_end(start,end):

# Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(func.min(Measurements.tobs).label('min'),func.avg(Measurements.tobs).label('avg'),func.max(Measurements.tobs).label('max')).filter(Measurements.date >= start).filter(Measurements.date <=end).all()
    

    start_end_stats_data = []
    for result in results:
        start_end_stats_dict = {}
        start_end_stats_dict['Min Temp'] = float(result[1])
        start_end_stats_dict['Avg Temp'] = float(result[0])
        start_end_stats_dict['Max Temp'] = result[2]
        start_end_stats_dict['Start Date'] = start
        start_end_stats_dict['End Date'] = end
        start_end_stats_data.append(start_end_stats_dict)
    
    return jsonify(start_end_stats_data)

if __name__ == '__main__':
    app.run(debug=True)