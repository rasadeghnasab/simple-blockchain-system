#wallet.py

import socketUtils
from transaction import Transaction as Tx
import signature

head_blocks = [None]

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
    print("Sent Tx1")
    socketUtils.sendObj('localhost', Tx2)
    print("Sent Tx2")
except:
    print("Error! Connection unsuccessfull.")

server = socketUtils.newServerConnection('localhost', 5006)
for i in range(50):
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
    try:
        if tx.inputs[0][0] == pu1 and tx.inputs[0][1] == 4.0:
            print("Tx1 is present")
    except:
        print("expected exceptions happend in wallet.py line 58")
    try:
        if tx.inputs[0][0] == pu3 and tx.inputs[0][1] == 4.0:
            print("Tx2 is present")
    except:
        print("expected exceptions happend in wallet.py line 58")

# Add new block to blockchain
for b in head_blocks:
    if b == None or newBlock.previousHash == b.computeHash():
        newBlock.previousBlock = b
        head_blocks.remove(b)
        head_blocks.append(newBlock)

print(head_blocks, "Wallet receive the new block successfully")
