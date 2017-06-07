

from flask import Flask


app = Flask(__name__)

ip_address = '192.168.43.87'

@app.route('/NDVI')
def NDVI():

    '''read sql table and stream everything through webpage'''


    end_data = ''

    return ('<p>' + str(end_data)+'</p>')



if __name__ == '__main__':

    app.run(host=ip_address , port=8500)