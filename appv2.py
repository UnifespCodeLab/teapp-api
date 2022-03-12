import os
from flask_cors import cross_origin
from api import app, PORTAL_NAME, VERSION
from api import controller


# TODO: Mover para controller
@app.route('/status')
def hello():
    return f'{PORTAL_NAME} API v{VERSION} Works! [{os.environ.get("ENV", "DEV")}]'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
