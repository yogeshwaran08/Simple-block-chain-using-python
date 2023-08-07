from flask import Flask, jsonify, request, render_template
from utils import Blockchain
from os.path import join

app = Flask(__name__)
chain = Blockchain()
chain.load_chain(join("output", "chains.json"))
print("[+] Chain loaded successfully")

@app.route('/create-chain', methods=['POST'])
def create_chain():
    previous_block = chain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = chain.proof_of_work(previous_proof)
    previous_hash = chain.hash(previous_block)
    data = request.get_json()
    chain.create_block(proof,previous_hash,data["VIN"],data["Model"],
                       data["Version"],data["color"],data['country'],data['dealer_code'],
                    data["dealer"],data['RO'],data['Odometer'],data['Part_number'],data['Part_name'],
                    data['Technician_Description'])
    #chain.save_chain("data/blockchain_db.json")
    return render_template("success.html", val=proof)

@app.route('/search', methods=['GET'])
def search_value():
    vin = request.args.get('VIN')
    data = chain.search_vechile_data(vin)
    return render_template("result.html",dicti=data)
    #return data

if __name__ == '__main__':
    app.run(debug=True,port=8000)
