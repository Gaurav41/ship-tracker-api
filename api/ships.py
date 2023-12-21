from flask import Blueprint, request, jsonify
from models.ship_models import db, ShipPositions
from datetime import datetime
import pandas as pd
from scripts.load_csv import load_csv_to_database
from sqlalchemy import desc


ships = Blueprint("ships",__name__)


@ships.route("/ships", methods=['GET'])
def get_ships():
    data = ShipPositions.query.all()
    if data:
        return jsonify({"message":f"{len(data)} records found", "data":[ship.to_dict() for ship in ShipPositions.query.all()]})
    return jsonify({"message":"No data","data":None})


@ships.route("/positions/<imo>", methods=['GET'])
def get_positions(imo):
    data = ShipPositions.query.filter_by(IMO_number=imo).order_by(desc(ShipPositions.timestamp)).all()
    if data:
        return jsonify({"message":f"{len(data)} records found", "data":[ship.to_dict() for ship in ShipPositions.query.all()]})
    return jsonify({f"message":"No data for Imo {imo}","data":None})


@ships.route("/load_data", methods=['POST'])
def uplaod_csv():
    if request.files and 'file' in request.files:
        try:
            load_csv_to_database(request.files['file'], db.engine)
            return jsonify({"message": "Data inserted Succesfully"}),200
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
