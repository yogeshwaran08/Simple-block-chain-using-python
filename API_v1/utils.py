import datetime
import hashlib
import json
from numba import jit,cuda
from pprint import pprint
import pandas as pd
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash="0",vin="",model_type="", version="",color="",country="",dealer_code="",dealer="",RO="", 
                     odometer="", part_number="", part_name="",desc="")

    def create_block(self, proof, previous_hash,vin,model_type, version,color,country,dealer_code,dealer,RO, 
                     odometer, part_number, part_name,desc):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
            "VIN" : vin,
            "model_type " : model_type,
            "version" : version,
            "color" : color,
            "country" : country, 
            "dealer_code" : dealer_code,
            "dealer" : dealer,
            "RO": RO,
            "odometer" : odometer,
            "part_number" : part_number,
            "part_name" : part_name,
            "tech_desc" : desc
        }
        self.chain.append(block)
        return block

    def print_previous_block(self):
        return self.chain[-1]
    
    def get_chain(self):
        return self.chain[1:]

    @jit(target_backend='cuda')
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()
            ).hexdigest()
            if hash_operation[:5] == "00000":
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False

            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()
            ).hexdigest()

            if hash_operation[:5] != "00000":
                return False
            previous_block = block
            block_index += 1
        return True
    def save_chain(self,filename):
        jsonString = json.dumps(self.chain)
        files = open(filename,'w')
        files.write(jsonString)
        files.close()

    def load_chain(self,filepath):
        file = open(filepath,'r')
        content = file.read()
        content = json.loads(content)
        self.chain = content
    
    def search_vechile_data(self,VIN):
        result = {}
        counter = 1
        for i in self.chain:
            temp = i.copy()
            if temp["VIN"] == VIN:
                del temp["index"]
                del temp["timestamp"]
                del temp["proof"]
                del temp["previous_hash"]
                result["d"+str(counter)] = temp
                counter += 1
        return result


def load_data_from_csv(obj,filepath):
    df = pd.read_csv(filepath)
    df = df.to_dict("records")
    counter =1
    for i in df: 
        print("Creating Block for VIN ",i['VIN']," at iter ",counter)
        previous_block = obj.print_previous_block()
        previous_proof = previous_block['proof']
        proof = obj.proof_of_work(previous_proof)
        previous_hash = obj.hash(previous_block)
        obj.create_block(proof,previous_hash,i['VIN'],i["MODEL TYPE"],
                                 i["VERSION"],i['COLOR'],i['COUNTRY'],i['DEALER CODE'],
                                 i['DEALER'],i['RO'],i['ODOMETER'],i['PART NUMBER'],
                                 i['PART NAME'],i['TECHNICIAN DESCRIPTION'])
        counter += 1
    else:
        print("Block Loading from csv success")

# chain = Blockchain()
# start = time.time()
# load_data_from_csv(chain,"../data/data.csv")
# print("Time taken : ",time.time()-start)
# print("Is chain is valid : ",chain.chain_valid(chain.chain))
# chain.save_chain("new_strct.json")

####search example
# chain = Blockchain()
# chain.load_chain("new_strct.json")
# vechicle  = chain.search_vechile_data("1FTNF1CG1GKF00539")
# print(vechicle)