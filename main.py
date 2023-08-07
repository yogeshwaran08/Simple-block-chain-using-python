import datetime
import hashlib
import json
from numba import jit,cuda
from pprint import pprint
import pandas
from blockchain import Blockchain
import pandas as pd
import os

chain = Blockchain()
while True:
    print("1. Create block chain\n2. Search Data Block Chain")
    choice = int(input("Enter your choice : "))

    if choice == 1:
        df = pd.read_csv(os.path.join("input","data.csv"))
        df = df.to_dict("records")
        for i in range(0,len(df),10):
            try:
                print("Creating ",i,"Block")
                previous_block = chain.print_previous_block()
                previous_proof = previous_block['proof']
                proof = chain.proof_of_work(previous_proof)
                previous_hash = chain.hash(previous_block)
                block = chain.create_block(proof, previous_hash,df[i],df[i+1],
                                        df[i+2],df[i+3],df[i+4],df[i+5],df[i+6],
                                        df[i+9],df[i+8],df[i+9])
                print("Block ",i,"created")
            except IndexError:
                print("Broken at ",i)
                #pprint(chain.chain[1])
                chain.save_chain(os.path.join("output","chain.json"))
                print("Data saved")
                break
        print(chain.chain_valid(chain.chain))
        chain.save_chain(os.path.join("output","chain.json"))

    elif choice == 2:
        print("[+] Loading file in memory")
        file = open(os.path.join("Output","chain.json"),'r')
        content = file.read()
        content = json.loads(content)
        chain.chain = content
        print("[+] Chain Loaded")
        vin = input("Enter the VIN number : ")
        result = []
        for block in chain.get_chain():
            for i in range(1,11):
                if block["data"+str(i)]['VIN'] == vin:
                    result.append(block["data"+str(i)])
        pprint(result)
        print("No of Records found : ",len(result))

        