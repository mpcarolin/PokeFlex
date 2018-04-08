from api import FlexApp
from sample_mapper import mapper

app = FlexApp(mapper)

if __name__ == '__main__':
   app.run(debug=True)
