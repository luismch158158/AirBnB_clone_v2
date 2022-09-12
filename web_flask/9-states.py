#!/usr/bin/python3
"""Script to starts a Flask web application and use storage
for fetching data from the storage engine"""
from flask import Flask, render_template
from markupsafe import escape
from models.state import State
from models.city import City
from models import storage
app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<string:id>", strict_slashes=False)
def cities_states(id=''):
    """This method display list of all State present in DBStorage
    sorted by name"""
    exist = 1
    escaped_id = escape(id)

    if (escaped_id == ''):
        values = list(storage.all(State).values())
        return (render_template('/9-states.html', states=values,
                                exist=exist, id=escaped_id))
    else:
        values = [storage.all(State).get('State.{:s}'.format(escaped_id))]

    if (values[0] is None):
        exist = 0

    return (render_template('/9-states.html', states=values,
                            exist=exist, id=escaped_id))


@app.teardown_appcontext
def close_session(self):
    """This method remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
