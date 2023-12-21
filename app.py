from flask import Flask
from api.ships import ships
from models.ship_models import db

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ships.db'


app.register_blueprint(ships, url_prefix="/api")

db.init_app(app)

with app.app_context():
    print("Created db")
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)