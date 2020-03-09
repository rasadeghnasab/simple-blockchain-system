#miner.py

import socketUtils

import txBlock
import signature
from transaction import Transaction as Tx

head_blocks = [None]
wallet_list = ['localhost']
network_reward=25.0

def findLongestBlockchain():
    longest = -1
    long_head = None

    for b in head_blocks:
        current = b
        this_len = 0
        while current != None:
            this_len += 1
            current = current.previousBlock
        if this_len > longest:
            long_head = b
            longets = this_len

    return long_head


def minerServer(my_ip, wallet_list, my_public_key):
    tx_list = []
    #Receive data from wallet
    server = socketUtils.newServerConnection(my_ip)

    # Get 2 Txs from wallets
    for iteration in range(10):
        newTx = socketUtils.recvObj(server)
        if isinstance(newTx, Tx):
            print("Tx {0} received".format(len(tx_list)))
            tx_list.append(newTx)
        if len(tx_list) >= 2:
            break

    # Add Txs to a new block
    newBlock = txBlock.TxBlock(findLongestBlockchain())

    for transaction in tx_list:
        newBlock.addTx(transaction)


    # Compute and add mining reward to the block
    total_in, total_out = newBlock.count_totals()
    rewardTx = Tx()
    rewardTx.add_output(my_public_key, network_reward+total_in-total_out)
    newBlock.addTx(rewardTx)

    # Find nonce
    for i in range(10):
        print("Finding Nonce...")
        newBlock.find_nonce()
        if newBlock.good_nonce():
            break
    if not newBlock.good_nonce():
        print("Error. Couldn't find nonce")
        return False

    # Send new block to wallets
    for ip_addr in wallet_list:
        socketUtils.sendObj(ip_addr, newBlock, 5006)

    # Replace new block with previously longest block
    head_blocks.remove(newBlock.previousBlock)
    head_blocks.append(newBlock)

    print(head_blocks, "Everything done successfully in miner")
    # Open server connection
    # Rec'v 2 transactions
    # Collect them into block
    # Fine nonce
    # Send that block to wallet_list
    return False

my_private_key, my_public_key = signature.generate_keys()

minerServer('localhost', wallet_list, my_public_key)
