from flask import request
from flask_restx import fields, Resource
from marshmallow.exceptions import ValidationError

from config import server
from message.models import Message
from message.schemas import MessageSchema, MultipleReceiversSchema
from utils import send_message

message_schema = MessageSchema()
multiple_receivers_schema = MultipleReceiversSchema()


class MessageReceiver(Resource):
    """
    Creates resource to receive, save to database, and pass through
    messages via socket.
    """

    post_model = server.api.model(
        'Post Messages',
        {
            'sender': fields.String(
                required=True,
                nullable=False,
                example="sys_admin"
            ),
            'receivers': fields.List(
                fields.String,
                required=True,
                nullable=False,
                example=["hostname_01", "hostname_02"]
            ),
            'message': fields.String(
                required=True,
                nullable=False,
                example="This is a message example."
            )
        },
    )

    @server.api.doc(responses={201: 'Created', 400: 'Bad request'})
    @server.api.expect(post_model)
    def post(self):
        """Receives messages to be passed on via socket."""

        # Validating data before all.
        message_json = request.get_json()
        try:
            message_data = multiple_receivers_schema.load(message_json)
        except ValidationError as e:
            return e.messages, 400

        # The previous block guarantees it will contain all needed fields.
        sender = message_data['sender']
        message = message_data['message']
        for receiver in message_data.get('receivers', []):

            # Creating instance and saving to db.
            instance = Message(sender, receiver, message)
            instance.create()

            # Now, all valid messages (last 24h) are retrieved, serialized,
            # and passed on.
            valid_messages_for_receiver = message_schema.dump(
                Message.get_valid_messages_for_receiver(receiver),
                many=True
            )
            send_message(receiver, valid_messages_for_receiver)

        # For now, it echoes back what was sent with its created status.
        return message_json, 201


class MessageResender(Resource):
    """
    Creates the resource to resend all valid for a given receiver without a 
    socket.
    """

    @server.api.doc(
        params={'receiver': 'Hostname that was used when the message was sent.'},
        responses={200: 'Success', 404: 'Not found'}
    )
    def get(self, receiver=None):
        """Returns all valid messages for a given receiver."""

        valid_messages_for_receiver = message_schema.dump(
            Message.get_valid_messages_for_receiver(receiver),
            many=True
        )

        if len(valid_messages_for_receiver) == 0:
            return {'detail': f"receiver '{receiver}' not found"}, 404

        return valid_messages_for_receiver, 200


class MessageReadMarker(Resource):
    """Adds the resource that sets a message as read."""

    @server.api.doc(
        params={'id': 'The ID of the message to be set as read.'},
        responses={204: 'No content', 404: 'Not found'}
    )
    def put(self, id=None):
        """Sets message as read from its id."""

        message = Message.query.get(id)
        if message is not None and (not message.read):
            message.read = True
            message.commit()

            return None, 204

        return {'detail': f"id '{id}' not found"}, 404
