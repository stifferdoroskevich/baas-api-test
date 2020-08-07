from api import app


@app.route('/')
def start():
    return "Dock is Here"


@app.route('/bee')
def bee():
    return "Dock is bee"
