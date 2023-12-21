from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ShipPositions(db.Model):
    __tablename__ = 'ship_positions'

    id = db.Column(db.Integer, primary_key=True)
    IMO_number = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, IMO_number, timestamp, latitude, longitude):
        self.IMO_number = IMO_number
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"<Ship {self.IMO_number}>"
    
    def to_dict(self):
        return {
            "IMO_number": self.IMO_number,
            "timestamp": self.timestamp,
            "latitude": self.latitude,
            "longitude": self.longitude
        }


