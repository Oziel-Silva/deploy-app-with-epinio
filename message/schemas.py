from marshmallow import fields, validate
from marshmallow_sqlalchemy import auto_field

from config import ma
from message.models import Message


class MessageSchema(ma.SQLAlchemySchema):
    """
    A serializer to map message fields from the database. Also adds
    display fields.
    """

    id = auto_field()
    sender = auto_field()
    receiver = auto_field()
    message = auto_field()
    created_at = auto_field()
    created_at_display_long = fields.Function(
        lambda obj: obj.created_at.strftime("%d/%m/%Y às %H:%M")
    )
    created_at_display = fields.Function(
        lambda obj: obj.created_at.strftime("%H:%M")
    )

    class Meta:
        model = Message
        load_instance = True


class MultipleReceiversSchema(ma.SQLAlchemySchema):
    """Serializer to take multiple receivers for a single message and sender."""

    sender = fields.String(required=True)
    receivers = fields.List(fields.String, required=True)
    message = fields.String(
        required=True,
        validate=[validate.Length(min=1,max=288)]
    )
