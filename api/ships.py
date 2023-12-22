from flask import Blueprint, request, jsonify
import sqlalchemy
from models.ship_models import db, ShipPositions, Ship
from datetime import datetime
import pandas as pd
from scripts.load_csv import load_position_csv_to_database, load_ship_csv_to_database
from sqlalchemy import desc
from flask_cors import cross_origin

ships = Blueprint("ships",__name__)


@ships.route("/ships", methods=['GET'])
@cross_origin()
def get_ships():
    """ GET API 
        Return all rows in Ship table as a json data
    """
    data = Ship.query.all()
    if data:
        return jsonify([ship.to_dict() for ship in data])
        # return jsonify({"message":f"{len(data)} records found", "data":[ship.to_dict() for ship in data]})
    return jsonify({"message":"No data","data":None})


@ships.route("/positions/<imo>", methods=['GET'])
@cross_origin()
def get_positions(imo):
    """GET API 
    
    argument: imo -- IMO number of ship
    Return: Return all rows in ShipPosition table as a json data for given IMO number
    """    
    data = ShipPositions.query.filter_by(IMO_number=imo).order_by(desc(ShipPositions.timestamp)).all()
    if data:
        # return jsonify({"message":f"{len(data)} records found", "data":[ship.to_dict() for ship in data]})
        return jsonify([ship.to_dict() for ship in data])
    return jsonify({f"message":"No data for Imo {imo}","data":None}),404


@ships.route("/load-position-data", methods=['POST'])
def uplaod_position_csv():
    """POST API 
    Insert the data from csv file to database ShipPosition table
    Payload: form-data, csv file
    Return: Success/Error response
    """  
    if request.files and 'file' in request.files:
        try:
            load_position_csv_to_database(request.files['file'], db.engine)
            return jsonify({"message": "Data inserted Succesfully"}),200
        except Exception as e:
            print(f"error while data ingestion: {e}")
            return jsonify({"error":"Internal Server Error"}),500    
    else:
        return jsonify({"error":"File not received"}),400
    

@ships.route("/load-ship-data", methods=['POST'])
def uplaod_ship_csv():
    """POST API 
    Insert the data from csv file to database Ship table
    Payload: form-data, csv file
    Return: Success/Error response
    """ 
    if request.files and 'file' in request.files:
        try:
            load_ship_csv_to_database(request.files['file'], db.engine)
            return jsonify({"message": "Data inserted Succesfully"}),200
        except sqlalchemy.exc.IntegrityError as e:
            return jsonify({"error":f"Dublicate data {e}"}),500    
 
        except Exception as e:
            print(f"error while data ingestion: {e}")
            return jsonify({"error":"Internal Server Error"}),500    
    else:
        return jsonify({"error":"File not received"}),400


# def df_to_database(df):
#     for index, row in df.iterrows():
#         ship = Ship(
#             IMO_number=df.iloc[:,0],
#             timestamp=pd.to_datetime(df.iloc[:,1]),
#             longitude=df.iloc[:,2],
#             latitude=df.iloc[:,3]
#         )
#         db.session.add(ship)
#     db.session.commit()
