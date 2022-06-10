import imp
from flask import Flask, render_template
import datetime
# ===============================================

# TEMPLATE FLASK & Flask Login With Firebase
# By otysimanov

# ================================================

from backend.config import configapp


app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'iNiAdalahsecrEtKey'
app.permanent_session_lifetime = datetime.timedelta(days=7)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(configapp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8008, debug=True)
