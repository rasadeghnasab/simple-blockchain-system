#server.py
import txBlock
import socketUtils

import socket
import pickle

TCP_PORT = 5005
IP_ADDR = 'localhost'

if __name__ == '__main__':
    s = socketUtils.newServerConnection(IP_ADDR)
    newB = socketUtils.recvObj(s)

    print(newB.data[0])
    print(newB.data[1])

    if newB.is_valid():
        print("Success. Tx is valid")
    else:
        print("Error. Tx is invalid.")

    if newB.data[0].inputs[0][1] == 2.3:
        print("Success. Input value matches")
    else:
        print("Error! Wrong input value for block 1, tx1")

    if newB.data[0].outputs[1][1] == 1.1:
        print("Success. Output value matches")
    else:
        print("Error! Wrong output value for block 1, tx1")

    if newB.data[1].inputs[0][1] == 2.3:
        print("Success. Input value matches")
    else:
        print("Error! Wrong input value for block 1, tx1")

    if newB.data[1].inputs[1][1] == 1.0:
        print("Success. Input value matches")
    else:
        print("Error! Wrong input value for block 1, tx1")

    if newB.data[1].outputs[0][1] == 3.1:
        print("Success. Output value matches")
    else:
        print("Error! Wrong output value for block 1, tx1")

    newTx = socketUtils.recvObj(s)
    print(newTx)
