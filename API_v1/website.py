from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/new_data')
def new_service():
    return render_template('get_data.html')

@app.route("/search-data")
def search():
    return render_template('search.html')

@app.route('/send-to-api', methods=['POST'])
def new_data():
    VIN = request.form['VIN']
    Model = request.form['Model']
    Version = request.form['Version']
    color = request.form['color']
    country = request.form['country']
    dealer_code = request.form['dealer_code']
    dealer = request.form['dealer']
    RO = request.form['RO']
    Odometer = request.form['Odometer']
    Part_number = request.form['Part_number']
    Part_name = request.form['Part_name']
    Technician_Description = request.form['Technician_Description']
    data = {
        'VIN': VIN,
        'Model': Model,
        'Version': Version,
        'color': color,
        'country': country,
        'dealer_code': dealer_code,
        'dealer': dealer,
        'RO': RO,
        'Odometer': Odometer,
        'Part_number': Part_number,
        'Part_name': Part_name,
        'Technician_Description': Technician_Description
    }
    response = requests.post('http://localhost:8000/create-chain', json=data)
    return response.text

@app.route("/search",methods=["GET"])
def search_data():
    response = requests.get("http://localhost:8000/search",params={"VIN":request.args['VIN']})
    return response.text

if __name__ == '__main__':
    app.run(debug=True,port=9000)
