from api import FlexApp

class TestMapper(object):
    def map(self, endpoint, json):
        json['added'] = 'added value'
        return json

app = FlexApp(TestMapper())

''' extensions '''
@app.route('/mark', methods=['GET'])
def mark():
    return app.map('/mark', {
        'mark': 'oh hai'
    })

if __name__ == '__main__':
   app.run(debug=True)
