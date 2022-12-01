from datetime import datetime, timedelta, timezone

from config import db


def datetime_with_corrected_timezone():
    """Returns a datetime with timezone GMT-3."""
    delta = timedelta(hours=-3)
    tz = timezone(delta, name="GMT-3")
    return datetime.now(tz)


class Message(db.Model):
    """
    Models how messages are saved to the database, adds classmethods to make
    specific queries easier, and encapsulates operations.
    """

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False, unique=False)
    receiver = db.Column(db.String(80), nullable=False, unique=False)
    message = db.Column(
        db.String(288), nullable=False, unique=False, default=''
    )
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime_with_corrected_timezone
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime_with_corrected_timezone,
        onupdate=datetime_with_corrected_timezone
    )

    def __init__(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        self.message = message

    def create(self):
        """Creates an entry on the database."""
        db.session.add(self)
        db.session.commit()

    def commit(self):
        """Commits changes to the database."""
        db.session.commit()

    @classmethod
    def get_last(cls):
        return cls.query.order_by(cls.id.desc()).first()

    @classmethod
    def get_valid_messages_for_receiver(cls, receiver):
        """
        Gets all valid messages for a given receiver.
        A valid message is any unread message that was sent in the past 24 hours.
        """

        limit = datetime.now() - timedelta(days=1)

        return db.session.query(cls).filter(
            cls.receiver == receiver,
            cls.created_at >= limit,
            cls.read == False
        ).order_by(cls.id.desc()).all()
