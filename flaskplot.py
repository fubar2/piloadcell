#! /usr/bin/python3
# simple web server for data accumulated to date by loadcell.py writing
# to loadcell.xls
# Check Configuring Flask-Cache section for more details

from flask import Flask, send_file, make_response
from flask_cache import Cache
import loadcellplot
app = Flask(__name__)
NSD = 2.0

cache = Cache(app,config={'CACHE_TYPE': 'simple'})

@app.route('/', methods=['GET'])
@cache.cached(timeout=600)
def lcscatter():
    lc = loadcellplot.loadCellPlotter(nsd=NSD,infi='loadcell.xls')
    bytes_obj = lc.loadcellplotFlask()
    
    return send_file(bytes_obj,
                     attachment_filename='loadcellplot.png',
                     mimetype='image/png')
                     
@app.route('/raw', methods=['GET'])
@cache.cached(timeout=600)
def lcraw():
    lc = loadcellplot.loadCellPlotter(nsd=None,infi='loadcell.xls')
    bytes_obj = lc.loadcellplotFlask()
    
    return send_file(bytes_obj,
                     attachment_filename='loadcellplot.png',
                     mimetype='image/png')
    
if __name__ == '__main__':
    app.run(debug=False, port=80, host='0.0.0.0')
