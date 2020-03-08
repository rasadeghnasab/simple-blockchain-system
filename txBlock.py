# Downloaded packages
import pickle
import time
import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# Personal packages
from blockchain import CBlock
from signature import generate_keys, sign, verify
from transaction import Transaction as Tx

leading_zeros=2
reward = 25.0
next_char_limit = 20

class TxBlock (CBlock):
        nonce = 'AAAAAAA'
        def __init__(self, previousBlock):
                super(TxBlock, self).__init__([], previousBlock)

        def addTx(self, Tx_in):
            self.data.append(Tx_in)

        def __count_totals(self):
            total_in = 0
            total_out = 0

            for transaction in self.data:
                total_in += transaction.in_amount
                total_out += transaction.out_amount

            return total_in, total_out

        def is_valid(self, show="False"):
                if not super(TxBlock, self).is_valid():
                        return False
                for transaction in self.data:
                        if not transaction.is_valid():
                                return False


                total_in, total_out = self.__count_totals()

                if total_out - total_in - reward > 0.000000000001:
                    return False

                return True

        def good_nonce(self):
            digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
            digest.update(bytes(str(self.data), 'utf8'))
            digest.update(bytes(str(self.previousHash), 'utf8'))
            digest.update(bytes(str(self.nonce), 'utf8'))

            this_hash = digest.finalize()
            if this_hash[:leading_zeros] != bytes(''.join(['\x4f' for i in range(leading_zeros)]),'utf8'):
                return False
            return int(this_hash[leading_zeros]) < next_char_limit

        def find_nonce(self):
            for i in range(1000000):
                self.nonce = "".join([
                    chr(random.randint(0,255)) for i in range(10*leading_zeros)])

                if self.good_nonce():
                    return self.nonce

            return None


if __name__ == '__main__':
        print("txBlock.py tests start here")

        private_key1, public_key1 = generate_keys()
        private_key2, public_key2 = generate_keys()
        private_key3, public_key3 = generate_keys()
        private_key4, public_key4 = generate_keys()

        Tx1 = Tx()
        Tx1.add_input(public_key1, 1)
        Tx1.add_output(public_key2, 1)
        Tx1.sign(private_key1)

        print('Tx{0} validation status before loading is: {1}'.format(1, Tx1.is_valid()))

        savefile = open("save.dat", "wb")
        pickle.dump(Tx1, savefile)
        savefile.close()

        loadfile = open("save.dat", "rb")
        loadedTx = pickle.load(loadfile)
        loadfile.close()

        print('Tx{0} validation status after loading is: {1}'.format(1, loadedTx.is_valid()))

        root = TxBlock(None)
        root.addTx(Tx1)

        Tx2 = Tx()
        Tx2.add_input(public_key2, 1.1)
        Tx2.add_output(public_key3, 1)
        Tx2.sign(private_key2)
        root.addTx(Tx2)

        B1 = TxBlock(root)

        Tx3 = Tx()
        Tx3.add_input(public_key3, 1.1)
        Tx3.add_output(public_key1, 1)
        Tx3.sign(private_key3)
        B1.addTx(Tx3)

        Tx4 = Tx()
        Tx4.add_input(public_key1, 1.1)
        Tx4.add_output(public_key2, 1)
        Tx4.add_required(public_key3)
        Tx4.sign(private_key1)
        Tx4.sign(private_key3)
        B1.addTx(Tx4)

        start = time.time()
        mynonce = B1.find_nonce()
        #print(mynonce)
        elapsed = time.time() - start
        print("elapsed time: " + str(elapsed) + " s.")

        if elapsed < 60:
            print("ERROR! Mining is too fast")


        if B1.good_nonce():
            print("Success! Nonce is good!")
        else:
            print("ERROR! Bad nonce")

        savefile = open('block.dat', "wb")
        pickle.dump(B1, savefile)
        savefile.close()

        loadfile = open('block.dat', "rb")
        load_B1  = pickle.load(loadfile)

        for name, block in [("root", root), ("B1", B1), ("load_B1", load_B1), ("load_B1.previousBlock", load_B1.previousBlock)]:
                if block.is_valid():
                        print('Success! {0} block is valid.'.format(name))
                else:
                        print('Error! {0} block is invalid.'.format(name))

        if B1.good_nonce():
            print("Success! Nonce is good after save and load!")
        else:
            print("ERROR! Bad nonce after load")

        BadB2 = TxBlock(B1)
        Tx5 = Tx()
        Tx5.add_input(public_key3, 1)
        Tx5.add_output(public_key1, 100)
        Tx5.sign(private_key3)
        BadB2.addTx(Tx5)

        load_B1.previousBlock.addTx(Tx4)

        for name, block in [("BadB2", BadB2), ("load_B1", load_B1)]:
                if block.is_valid():
                        print('Error! Bad {0} block verified.'.format(name))
                else:
                        print('Success! Bad {0} block detected.'.format(name))


        # Test mining reward and TX fees
        Tx6 = Tx()
        Tx6.add_output(public_key4, 25)

        B3 = TxBlock(B1)
        B3.addTx(Tx2)
        B3.addTx(Tx3)
        B3.addTx(Tx4)
        B3.addTx(Tx6)
        if B3.is_valid(show='True'):
            print('Success! Block reward succeeds.')
        else:
            print("Error! Block reward fail.")


        B4 = TxBlock(B3)
        B4.addTx(Tx2)
        B4.addTx(Tx3)
        B4.addTx(Tx4)
        Tx7 = Tx()
        Tx7.add_output(public_key4, 25.2)
        B4.addTx(Tx7)
        if B4.is_valid():
            print("Success! Tx fees succeeds")
        else:
            print("Error! Tx fees fail")

        #Greedy miner
        B5 = TxBlock(B4)
        B5.addTx(Tx2)
        B5.addTx(Tx3)
        B5.addTx(Tx4)
        Tx8 = Tx()
        Tx8.add_output(public_key4, 26.2)
        B5.addTx(Tx8)
        if not B5.is_valid():
            print("Success! Greedy miner detected.")
        else:
            print("Error! Greedy miner not detected.")

