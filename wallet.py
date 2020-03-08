#wallet.py

import socketUtils
from transaction import Transaction as Tx
import signature

Tx1 = Tx()
Tx2 = Tx()

pr1, pu1 = signature.generate_keys()
pr2, pu2 = signature.generate_keys()
pr3, pu3 = signature.generate_keys()

Tx1.add_input(pu1, 4.0)
Tx1.add_input(pu2, 1.0)
Tx1.add_output(pu3, 4.8)
Tx2.add_input(pu3, 4.0)
Tx2.add_output(pu2, 4.0)
Tx2.add_required(pu1)

Tx1.sign(pr1)
Tx1.sign(pr2)
Tx2.sign(pr3)
Tx2.sign(pr1)

try:
    socketUtils.sendObj('localhost', Tx1)
    socketUtils.sendObj('localhost', Tx2)
except:
    print("Error! Connection unsuccessfull.")

server = socketUtils.newServerConnection('localhost')
for i in range(30):
    newBlock = socketUtils.recvObj(server)
    if newBlock:
        break
server.close()

if newBlock.is_valid():
    print("Success! Block is valid")
else:
    print("Error! Block is invalid")

if newBlock.good_nonce():
    print("Success! Nonce is valid")
else:
    print("Error! Nonce is not valid")

for tx in newBlock.data:
    if tx == Tx1:
        print("Tx1 is present")
    if tx == Tx2:
        print("Tx2 is present")

