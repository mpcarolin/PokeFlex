from flask_api import FlaskAPI

app = FlaskAPI(__name__)

@app.route("/pokemon", methods=['GET'])
def get_pokemon():
    return {
        'name': 'Pikachu',
        'color': 'Yellow',
        'type': 'Lightning'
    }

if __name__ == '__main__':
    app.run(debug=True)
