from flask import Blueprint, Flask
from flask_marshmallow import Marshmallow
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy


class Server():
    """
    Defines application server factory and configuration, database
    connection, namespace to be used and place for running as well.
    """

    def __init__(self):
        self.app = Flask(__name__)
        self.blueprint = Blueprint('api', __name__, url_prefix='/api')
        self.api = Api(self.blueprint,
                       doc='/doc',
                       title='Notification System API',
                       default_label='Messages',
                       default='Methods',
                       version='1.2.1'
                       )
        self.app.register_blueprint(self.blueprint)

        # port = os.environ['PORT']
        # database = os.environ['DATABASE']
        # uid = os.environ['UID']
        # pwd = os.environ['PASSWORD']

        # # This string is only used for Microsoft SQL-Server. Changing the
        # # connection string is necessary to use another database.
        # connect_string = (
        #     'Driver={ODBC Driver 17 for SQL Server};'
        #     f'Server=sql_server,{port};'
        #     f'Database={database};'
        #     f'uid={uid};'
        #     f'pwd={pwd}'
        # )
      
        self.app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:GZxcy0tt3U@xbeeb293a60cdd0d4f4dac2355c57-postgresql-hl.workspace.svc.cluster.local:5432/postgres"
        self.app.config['SQLALCHEMY_ECHO'] = True
        self.app.config['PROPAGATE_EXCEPTIONS'] = True
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def run(self):
        self.app.run(host='0.0.0.0', port=5000, debug=False)


db = SQLAlchemy()
ma = Marshmallow()
server = Server()
