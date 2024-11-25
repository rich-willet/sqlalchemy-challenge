# Import the dependencies
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt

#################################################
# Database Setup
#################################################

# Set up the database engine
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database schema
Base = automap_base()
Base.prepare(autoload_with=engine)

# References to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Flask app
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"<h1>Welcome to the Climate API!</h1><br/>"
        f"<h3>Available Routes:</h3>"
        f"<ul>"
        f"<li><a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a> - Precipitation data for the past year.</li>"
        f"<li><a href='/api/v1.0/stations'>/api/v1.0/stations</a> - List of weather observation stations.</li>"
        f"<li><a href='/api/v1.0/tobs'>/api/v1.0/tobs</a> - Temperature observations of the most active station for the past year.</li>"
        f"<li><b>/api/v1.0/&lt;start&gt;</b> - Replace <i>&lt;start&gt;</i> with a start date in YYYY-MM-DD format to get min, avg, and max temperatures from that date onward.</li>"
        f"<li><b>/api/v1.0/&lt;start&gt;/&lt;end&gt;</b> - Replace <i>&lt;start&gt;</i> and <i>&lt;end&gt;</i> with a date range in YYYY-MM-DD format to get min, avg, and max temperatures for that range.</li>"
        f"</ul>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the last 12 months of precipitation data."""
    # Start a session
    session = Session(engine)

    # Find the most recent date in the dataset
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.datetime.strptime(recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    # Close the session
    session.close()

    # Create a dictionary with date as the key and precipitation as the value
    precipitation_dict = {date: prcp for date, prcp in results}

    # Return JSON
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all station IDs."""
    # Start a session
    session = Session(engine)

    # Query all station IDs
    results = session.query(Station.station).all()

    # Close the session
    session.close()

    # Convert to a list
    stations_list = [station[0] for station in results]

    # Return JSON
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations for the most active station."""
    # Start a session
    session = Session(engine)

    # Find the most recent date in the dataset
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.datetime.strptime(recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Find the most active station
    most_active_station = session.query(
        Measurement.station, func.count(Measurement.id)
    ).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).first()[0]

    # Query the temperature observations for the last 12 months
    results = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.date >= one_year_ago,
        Measurement.station == most_active_station
    ).all()

    # Close the session
    session.close()

    # Convert to a list
    tobs_list = [{date: tobs} for date, tobs in results]

    # Return JSON
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end=None):
    """Return temperature stats for a given start or start-end range."""
    # Start a session
    session = Session(engine)

    if end:
        # Query temperature stats for start to end range
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        # Query temperature stats for start to the last available date
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start).all()

    # Close the session
    session.close()

    # Create a dictionary for temperature statistics
    temp_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    # Return JSON
    return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True)
