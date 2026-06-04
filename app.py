import os
from flask import Flask
from classes.gclass import Gclass

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
Gclass.path = os.path.join(BASE_DIR, 'data', 'dados_finais.db')

app = Flask(__name__, template_folder='classes/templates')
app.secret_key = 'chave_secreta_para_o_trabalho'

from classes.model import Model
from classes.suplier import Suplier
from classes.manufacturer import Manufacturer
from classes.transaction import Transaction

def carregar_dados_da_bd():
    try:
        Model.reset()
        Suplier.reset()
        Manufacturer.reset()
        Transaction.reset()
        Model.read(Gclass.path)
        Suplier.read(Gclass.path)
        Manufacturer.read(Gclass.path)
        Transaction.read(Gclass.path)
    except Exception as e:
        print(f"Erro ao ler base de dados: {e}")

from routes.dashboard_routes import dashboard_bp
from routes.model_routes import model_bp
from routes.suplier_routes import suplier_bp
from routes.manufacturer_routes import manufacturer_bp
from routes.transaction_routes import transaction_bp


app.register_blueprint(dashboard_bp)
app.register_blueprint(model_bp)
app.register_blueprint(suplier_bp)
app.register_blueprint(manufacturer_bp)
app.register_blueprint(transaction_bp)


carregar_dados_da_bd()

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)