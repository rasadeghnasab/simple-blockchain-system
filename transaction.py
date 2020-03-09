#Transaction.py
import signature
#signature.sign
#signature.verify

class Transaction:
    inputs = None
    outputs =None
    sigs = None
    requireds = None
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.requireds = []
        self.total_in = 0
        self.total_out = 0

    def add_input(self, from_addr, amount):
        self.total_in += amount
        self.inputs.append((from_addr, amount))

    def add_output(self, to_addr, amount):
        self.total_out += amount
        self.outputs.append((to_addr, amount))

    def add_required(self, addr):
        self.requireds.append(addr)

    def sign(self, private):
        message = self.__gather()
        newsig = signature.sign(message, private)
        self.sigs.append(newsig)

    def is_valid(self):
        total_in = 0
        total_out = 0
        message = self.__gather()
        for addr,amount in self.inputs:
            found = False
            for s in self.sigs:
                if signature.verify(message, s, addr) :
                    found = True
            if not found:
                #print ("No good sig found for " + str(message))
                return False
            if amount < 0:
                return False
            total_in = total_in + amount
        for addr in self.requireds:
            found = False
            for s in self.sigs:
                if signature.verify(message, s, addr) :
                    found = True
            if not found:
                return False
        for addr,amount in self.outputs:
            if amount < 0:
                return False
            total_out = total_out + amount

        #if total_out > total_in:
            #print("Outputs exceed inputs")
        #    return False

        return True
    def __gather(self):
        data=[]
        data.append(self.inputs)
        data.append(self.outputs)
        data.append(self.requireds)
        return data
    def __repr__(self):
        reprstr = "INPUTS:\n"
        for addr, amt in self.inputs:
            reprstr = reprstr + str(amt) + " from " + str(addr) + "\n"
        reprstr = reprstr + "OUTPUTS:\n"
        for addr, amt in self.outputs:
            reprstr = reprstr + str(amt) + " to " + str(addr) + "\n"
        reprstr = reprstr + "requireds:\n"
        for r in self.requireds:
            reprstr = reprstr + str(r) + "\n"
        reprstr = reprstr + "SIGS:\n"
        for s in self.sigs:
            reprstr = reprstr + str(s) + "\n"
        reprstr = reprstr + "END\n"
        return reprstr



if __name__ == "__main__":
    pr1, pu1 = signature.generate_keys()
    pr2, pu2 = signature.generate_keys()
    pr3, pu3 = signature.generate_keys()
    pr4, pu4 = signature.generate_keys()

    Tx1 = Transaction()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)
    if Tx1.is_valid():
        print("Success! Tx is valid")
    else:
        print("ERROR! Tx is invalid")

    Tx2 = Transaction()
    Tx2.add_input(pu1, 2)
    Tx2.add_output(pu2, 1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr1)

    Tx3 = Transaction()
    Tx3.add_input(pu3, 1.2)
    Tx3.add_output(pu1, 1.1)
    Tx3.add_required(pu4)
    Tx3.sign(pr3)
    Tx3.sign(pr4)

    for t in [Tx1, Tx2, Tx3]:
        if t.is_valid():
            print("Success! Tx is valid")
        else:
            print("ERROR! Tx is invalid")

    # Wrong signature
    Tx4 = Transaction()
    Tx4.add_input(pu1, 1)
    Tx4.add_output(pu2, 1)
    Tx4.sign(pr2)

    # Escrow Tx not signed by the arbiter
    Tx5 = Transaction()
    Tx5.add_input(pu3, 1.2)
    Tx5.add_output(pu1, 1.1)
    Tx5.add_required(pu4)
    Tx5.sign(pr3)

    # Two input addrs, signed by one
    Tx6 = Transaction()
    Tx6.add_input(pu3, 1)
    Tx6.add_input(pu4, 0.1)
    Tx6.add_output(pu1, 1.1)
    Tx6.sign(pr3)

    # Negative values
    Tx8 = Transaction()
    Tx8.add_input(pu2, -1)
    Tx8.add_output(pu1, -1)
    Tx8.sign(pr2)

    # Modified Tx
    Tx9 = Transaction()
    Tx9.add_input(pu1, 1)
    Tx9.add_output(pu2, 1)
    Tx9.sign(pr1)
    # outputs = [(pu2,1)]
    # change to [(pu3,1)]
    Tx9.outputs[0] = (pu3,1)


    for t in [Tx4, Tx5, Tx6, Tx8, Tx9]:
        if t.is_valid():
            print("ERROR! Bad Tx is valid")
        else:
            print("Success! Bad Tx is invalid")









