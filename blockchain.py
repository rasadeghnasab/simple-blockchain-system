# Blockchain.py
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

class SomeClass:
        string = None
        num = 123456789

        def __init__(self, mystring):
                self.string = mystring

        def __repr__(self):
                return str(self.string) + " ^^^ " + str(self.num)

class CBlock:
        data = None
        previousHash = None
        previousBlock = None
        is_genesis = False

        def __init__(self, data, previousBlock):
                self.is_genesis = previousBlock is None
                self.data = data
                self.previousBlock = previousBlock
                if not self.is_genesis:
                        self.previousHash = previousBlock.computeHash()


        def computeHash(self):
                digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
                digest.update(bytes(str(self.data), 'utf8'))
                digest.update(bytes(str(self.previousHash), 'utf8'))

                return digest.finalize()

        def is_valid(self):
                if self.is_genesis:
                        return True

                return self.previousBlock.computeHash() == self.previousHash and self.previousBlock.is_valid()

if __name__ == '__main__':
        print("blockchain.py tests start here")

        root = CBlock('I am root', None)
        B1   = CBlock('I am a child', root)
        B2   = CBlock('I am B1s brother, B2', root)
        B3   = CBlock(12345, B2)
        B4   = CBlock(SomeClass('Hi there'), B3)
        B5   = CBlock(SomeClass('Hi there'), B4)
        B6   = CBlock("Top block", B5)

        # All blocks should be fine
        for block in [B1, B2, B3, B4, B5]:
                if block.is_valid():
                        print("Success! Hash is good.")
                else:
                        print("Error! Hash is not good.")

        # Tempered blocks
        # Change in B3 should be detect in B4
        # Note: Any change in a block should be detected into other blocks after that
        B3.data = 'tempered data'
        B4.data.num = '99999'

        # All blocks below should be detected as the tempered blocks
        for tempered_block in [B4, B5, B6]:
                if tempered_block.is_valid():
                        print("Error! Hash is good by mistake.")
                else:
                        print("Success! Hash is not good detected successfully.")













