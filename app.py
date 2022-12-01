from flask import redirect, url_for

from config import db, ma, server
from message.views import (
    MessageReceiver,
    MessageResender,
    MessageReadMarker
)


app = server.app

# Adding messages resources.
server.api.add_resource(MessageReceiver, '/messages')
server.api.add_resource(MessageResender, '/messages/<string:receiver>')
server.api.add_resource(MessageReadMarker, '/messages/<int:id>')


@app.before_first_request
def create_table():
    db.create_all()


db.init_app(app)


@app.route("/")
def starting_url():
    """Redirects to the documentation."""

    url = url_for('api.doc')
    return redirect(url)


if __name__ == '__main__':

    ma.init_app(app)
    server.run()
