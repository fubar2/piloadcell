from flask import Flask, send_file, make_response
from loadcellplotter import loadcellplot
app = Flask(__name__)

@app.route('/', methods=['GET'])
def lcscatter():
    bytes_obj = loadcellplot()
    
    return send_file(bytes_obj,
                     attachment_filename='loadcellplot.png',
                     mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=False, port=80, host='0.0.0.0')
