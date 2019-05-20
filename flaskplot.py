#! /usr/bin/python3
# simple web server for data accumulated to date by loadcell.py writing
# to loadcell.xls

from flask import Flask, send_file, make_response
import loadcellplot
app = Flask(__name__)
NSD = 2.0


@app.route('/', methods=['GET'])
def lcscatter():
    lc = loadcellplot.loadCellPlotter(nsd=NSD,infi='loadcell.xls')
    bytes_obj = lc.loadcellplotFlask()
    
    return send_file(bytes_obj,
                     attachment_filename='loadcellplot.png',
                     mimetype='image/png')
                     
@app.route('/raw', methods=['GET'])
def lcraw():
    lc = loadcellplot.loadCellPlotter(nsd=None,infi='loadcell.xls')
    bytes_obj = lc.loadcellplotFlask()
    
    return send_file(bytes_obj,
                     attachment_filename='loadcellplot.png',
                     mimetype='image/png')
    
if __name__ == '__main__':
    app.run(debug=False, port=80, host='0.0.0.0')
