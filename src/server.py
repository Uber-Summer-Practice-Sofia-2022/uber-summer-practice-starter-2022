import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

server = Flask(__name__)

server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    os.getenv('DB_USER', 'admin'),
    os.getenv('DB_PASSWORD', 'mysql'),
    os.getenv('DB_HOST', 'localhost'),
    os.getenv('DB_PORT', '3307'),
    os.getenv('DB_NAME', 'db')
)
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print(server.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(server)


@dataclass
class Log(db.Model):
    id: int
    log: str

    id = db.Column(db.Integer, primary_key=True)
    log = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return '<Log %r>' % self.log

    def __init__(self, message):
        self.log = message


# create the DB on demand
@server.before_first_request
def create_tables():
    db.create_all()


@server.route("/")
def hello():
    return "Hello World!"


@server.route("/hello")
def personalised_hello():
    username = request.args.get('user')
    return f'Hello {username}!'


@server.route('/logs', methods=['POST'])
def insert_log():
    request_data = request.get_json()

    log_message = request_data['log_message']
    log = Log(log_message)

    db.session.add(log)
    db.session.commit()
    return 'success!'


@server.route('/logs', methods=['GET'])
def get_all_logs():
    logs = Log.query.all()
    return jsonify(logs)


if __name__ == "__main__":
    server_port = os.environ['FLASK_PORT']
    server.run(host='0.0.0.0', port=server_port, debug=True)
