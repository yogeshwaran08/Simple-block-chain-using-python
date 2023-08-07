import datetime
import hashlib
import json
from numba import jit,cuda
from pprint import pprint
import pandas

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash="0",d0={},d1={},d2={},d3={},d4={},d5={},d6={},d7={},d8={},d9={})

    def create_block(self, proof, previous_hash,d0,d1,d2,d3,d4,d5,d6,d7,d8,d9):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
            "data1": d0,"data2": d1,"data3": d2,"data4": d3,"data5": d4,"data6": d5,"data7": d6,"data8": d7,"data9": d8,"data10": d9
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