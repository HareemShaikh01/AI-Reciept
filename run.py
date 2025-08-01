from flask import Flask
from app.routes.workspace import workspace_bp

app = Flask(__name__)

app.register_blueprint(workspace_bp)

@app.route("/")
def runApp():
    return "APP running Successfully"

app.run(debug=True)
