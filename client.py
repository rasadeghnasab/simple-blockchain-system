#client.py

import pickle
import socket

import signature
import socketUtils
from txBlock import TxBlock as TxBlock
from transaction import Transaction as Tx

TCP_PORT = 5005
IP_ADDR = 'localhost'

if __name__ == "__main__":
    print("client.py test start here")
    pr1, pu1 = signature.generate_keys()
    pr2, pu2 = signature.generate_keys()
    pr3, pu3 = signature.generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 2.3)
    Tx1.add_output(pu2, 1.0)
    Tx1.add_output(pu3, 1.1)
    Tx1.sign(pr1)

    Tx2 = Tx()
    Tx2.add_input(pu3, 2.3)
    Tx2.add_input(pu2, 1.0)
    Tx2.add_output(pu1, 3.1)
    Tx2.sign(pr2)
    Tx2.sign(pr3)

    B1 = TxBlock(None)
    B1.addTx(Tx1)
    B1.addTx(Tx2)

    socketUtils.sendObj(IP_ADDR, B1)

    socketUtils.sendObj(IP_ADDR, Tx2)



