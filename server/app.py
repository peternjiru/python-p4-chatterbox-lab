from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():

    if request.method == 'GET':
            
        messages = []
        for message in Message.query.order_by(Message.created_at.asc()).all():
            message_dict = message.to_dict()
            messages.append(message_dict)

        response = make_response(
            messages,
            200
        )

        return response
    
    elif request.method == 'POST':

        request_data = request.json

        new_message = Message(
            body=request_data['body'],
            username=request_data['username'],
        )

        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()

        response = make_response(
            jsonify(new_message_dict),
            201
        )

        return response

@app.route('/messages/<int:id>', methods=['PATCH','DELETE'])
def messages_by_id(id):
    if request.method == 'PATCH':
            message = Message.query.filter(Message.id == id).first()

            # for attr in request.form:
            #     setattr(message, attr, request.form.get(attr))

            # Extracts JSON data from the request body
            request_data = request.json

            message.body=request_data['body']

            db.session.add(message)
            db.session.commit()

            message_dict = message.to_dict()

            response = make_response(
                jsonify(message_dict),
                200
            )

            return response
     
    elif request.method == 'DELETE':
            message = Message.query.filter(Message.id == id).first()

            db.session.delete(message)
            db.session.commit()

            response_body = {
            "delete_successful": True,
            "message": "Message deleted."    
            }

            response = make_response(
             response_body,
             200
            )

            return response

if __name__ == '__main__':
    app.run(port=4000)
