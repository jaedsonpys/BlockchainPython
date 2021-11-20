from hashlib import sha256
from datetime import datetime
import json

class Block:
    def __init__(self, transitions, previous_hash) -> None:
        self.transitions = transitions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.timestamp = datetime.now()

        self.hash = self.generate_hash()

    def generate_hash(self) -> str:
        block_content = str(self.transitions) + str(self.timestamp) + str(self.previous_hash) + str(self.nonce)
        block_hash = sha256(block_content.encode())

        return block_hash.hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.all_transitions = []
        self.genesis_block()

    def genesis_block(self):
        transitions = []
        previous_hash = 0
        self.chain.append(Block(transitions,previous_hash))

    def add_block(self, transitions):
        previous_hash = self.chain[-1].hash
        new_block = Block(transitions, previous_hash)

        self.chain.append(new_block)

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            if current.hash != current.generate_hash():
                print('\033[31mO bloco foi alterado. Hashes não são compatíveis\033[m')
                return False

            if previous.hash != previous.generate_hash():
                print('\033[31mO bloco foi alterado. Hashes não são compatíveis\033[m')
                return False

        return True


mycrypto = Blockchain()
fake = {"sender": "Pedro", "receiver": "Gabriela", "value": "340"}

with open('blocks.json', 'r') as file:
    blocks = json.load(file)

for t in blocks:
    mycrypto.add_block(t)

for c, i in enumerate(mycrypto.chain):
    print(f'Block {c}')
    print(f'Nonce: {i.nonce}')
    print(f'Hash: {i.hash}')
    print(f'Previous Hash: {i.previous_hash}')
    print(f'Timestamp: {i.timestamp}')
    print()

mycrypto.chain[2].transitions = fake
print(mycrypto.verify_chain())