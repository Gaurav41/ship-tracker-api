from flask import Flask
from api.ships import ships
from models.ship_models import db,Ship
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ships.db'


app.register_blueprint(ships, url_prefix="/api")

db.init_app(app)

with app.app_context():
    db.create_all()
    print("database created")
    if not Ship.query.all():
        ship1 = Ship(IMO_number=9632179,name="Mathilde Maersk")
        ship2 = Ship(IMO_number=9247455,name="Australian Spirit")
        ship3 = Ship(IMO_number=9595321,name="MSC Preziosa")
        db.session.bulk_save_objects([ship1,ship2,ship3])
        db.session.commit()
        print("add some entries to ship table")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)