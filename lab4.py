from uuid import uuid4
import json
import hashlib
from datetime import datetime

class Transaction:
    def __init__(self, from_person, to_person, amount: int):
        self.id = str(uuid4())
        self.from_person = from_person
        self.to_person = to_person
        self.amount = amount

    def __repr__(self):
        return {
            "transaction_id": self.id,
            "from_person": self.from_person.id,
            "to_person": self.to_person.id,
            "amount": self.amount
        }
    

class Block:
    def __init__(self, transactions: list[Transaction], previous_block=None):
        self.previous_block_hash = previous_block.hash if previous_block else None
        self.timestamp = datetime.utcnow().timestamp()
        self.transactions = transactions
        self.nonce = 0
        self.merkleTree = MerkleTree()
        self.fill_tree()
        self.hash = self.__hash__()
        print(f'Block with hash {self.hash} created')

    def __repr__(self):
        return {
            "previous_hash": self.previous_block_hash,
            "transactions": [transaction.__repr__() for transaction in self.transactions],
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }

    def __hash__(self):
        data2hash = f"{self.previous_block_hash}{self.nonce}{self.merkleTree.root.hash}" if self.merkleTree.root else f"{self.previous_block_hash}{self.nonce}"
        return hashlib.sha256(data2hash.encode()).hexdigest()

    def fill_tree(self):
        for transaction in self.transactions:
            self.merkleTree.addNode(json.dumps(transaction.__repr__()))

    def validate_proof_of_work(self, DIFF=4):
        while True:
            if self.hash[:DIFF] == '0' * DIFF:
                return True
            self.nonce += 1
            self.hash = self.__hash__()

    def get_block_info(self, clients_data: dict):
        for transaction in self.transactions:
            for client in [transaction.to_person, transaction.from_person]:
                if client.name not in clients_data:
                    clients_data[client.name] = {"current": client.starting_balance,
                                                 "min": client.starting_balance,
                                                 "max": client.starting_balance}

            clients_data[transaction.from_person.name]['current'] -= transaction.amount
            clients_data[transaction.to_person.name]['current'] += transaction.amount
            clients_data[transaction.from_person.name]['min'] = min(clients_data[transaction.from_person.name]['min'],
                                                                    clients_data[transaction.from_person.name][
                                                                        'current'])
            clients_data[transaction.to_person.name]['max'] = max(clients_data[transaction.to_person.name]['max'],
                                                                  clients_data[transaction.to_person.name][
                                                                      'current'])
        return clients_data


class Blockchain:
    def __init__(self, difficulty=4, mxt=3):
        self.difficulty = difficulty
        self.max_transaction_num = mxt

        self.chain: list[Block] = []
        self.transactions: list[Transaction] = []
        self.merkleTree: MerkleTree = MerkleTree()
        self.block_process()

    def block_process(self, block: Block = None):
        if len(self.chain) == 0:
            block = Block([])

        block.validate_proof_of_work(self.difficulty)
        self.chain.append(block)
        self.merkleTree.addNode(block.hash)

    def blockchain_root_hash(self):
        tree = MerkleTree()
        for block in self.chain:
            tree.addNode(block.hash)
        return tree.root.hash

    def validate(self):
        if self.blockchain_root_hash() != self.merkleTree.root.hash:
            print("Invalid root hashes")
            return False
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if ((current_block.__hash__() != current_block.hash)
                    or (current_block.previous_block_hash != previous_block.hash)):
                print("Invalid block hash")
                return False
        return True

    def transaction_process(self, transaction: Transaction):
        self.transactions.append(transaction)
        if len(self.transactions) >= self.max_transaction_num:
            block = Block(self.transactions, self.chain[-1])
            self.block_process(block)
            self.transactions = []

    def get_block_info(self, index):
        block_position = index
        if block_position >= len(self.chain):
            print('Block position out of range')
            return

        client_balances = {}
        for i in range(block_position+1):
            client_balances = self.chain[i].get_block_info(client_balances)

        return client_balances


class Client:
    def __init__(self, name: str, balance=50):
        self.id = str(uuid4())
        self.name = name
        self.balance = balance
        self.starting_balance = balance

    def transfer(self, to_person, amount: int):
        if amount > self.balance:
            print(f"Cannot make transaction - not enough balance")
            return
        if to_person == self:
            print('Cannot make transaction to self')
            return
        if amount < 0:
            print(f"Cannot make negative transaction")
            return
        transaction = Transaction(self, to_person, amount)
        return transaction

    def receive(self, amount: int):
        self.balance += amount


class MerkleTree:
    def __init__(self):
        self.root: Node | None = None
        self.leaves: list[Node] = []

    def addNode(self, data):
        node = Node(data)
        self.leaves.append(node)
        self.update()

    def update(self):
        if len(self.leaves) == 0:
            self.root = None
            return

        tree_copy = self.leaves
        while len(tree_copy) > 1:
            if len(tree_copy) % 2 == 1:
                tree_copy.append(Node(self.leaves[-1].hash))
            new_node_level = []
            for i in range(0, len(tree_copy), 2):
                new_node = Node(leftNode=tree_copy[i], rightNode=tree_copy[i + 1])
                new_node_level.append(new_node)
            tree_copy = new_node_level

        self.root = tree_copy[0]


class Node:
    def __init__(self, data=None, leftNode=None, rightNode=None):
        self.leftNode = leftNode
        self.rightNode = rightNode
        self.hash = self.hashNode(data)

    def hashNode(self, data):
        if data is not None:
            return hashlib.sha256(data.encode()).hexdigest()
        else:
            data2hash = self.leftNode.hash + self.rightNode.hash if (self.leftNode and self.rightNode) else ''
            return hashlib.sha256(data2hash.encode()).hexdigest()
        

class Network:
    def __init__(self):
        self.blockchain = Blockchain()
        self.clients: list[Client] = []

    def add_client(self, client: Client):
        client.network = self
        self.clients.append(client)

    def process_transaction(self, transaction: Transaction):
        client = next((client for client in self.clients if client == transaction.to_person), None)
        if not client:
            print(f'Receiver not found')
            return
        print(f'Transaction from {transaction.from_person.name} '
              f'to {transaction.to_person.name}: {transaction.amount}')
        self.blockchain.transaction_process(transaction)
        client.receive(transaction.amount)

    def save_to_json(self, default_path='blockchain.json'):
        print('Saving to json')
        with open(default_path, 'w') as f:
            json.dump([block.__repr__() for block in self.blockchain.chain], f, indent=4)

    def store_data_json(self, default_path='blockchain.json'):
        print('Loading fom json')
        with open(default_path, 'r') as f:
            data = json.load(f)
            self.blockchain = Blockchain()
            for block_js in data:
                transactions = []
                for tr in block_js['transactions']:
                    sender = next((client for client in self.clients if client.id == tr['from']), None)
                    receiver = next((client for client in self.clients if client.id == tr['to']), None)
                    transactions.append(Transaction(sender, receiver, tr['amount']))
                block = Block(transactions)
                block.nonce = block_js['nonce']
                block.hash = block.__hash__()
                self.blockchain.chain.append(block)


# Initializing the network and clients
network = Network()

alice = Client("Alice", balance=60000)
bob = Client("Bob", balance=4500)
eva = Client("Eva", balance=7500)
network.add_client(alice)
network.add_client(bob)
network.add_client(eva)

# Creating transactions with different numbers
transactions = [
    alice.transfer(bob, 1500),
    alice.transfer(eva, 750),
    eva.transfer(bob, 200),
    bob.transfer(eva, 450),
    bob.transfer(alice, 300),
    eva.transfer(alice, 1200)
]

# Processing transactions and creating blockchain blocks
print("Processing Transactions and Creating Blockchain Blocks:")
for transaction in transactions:
    network.process_transaction(transaction)
print()

# Validating blockchain data integrity
print("\nBlockchain Data Integrity Validation:")
if network.blockchain.validate():
     print("Validation Successful!")
else:
    print("Validation Error.")
print()

# Proof of Work validation for the first block
print("\nProof of Work Validation for First Block:")
if network.blockchain.chain[1].validate_proof_of_work():
    print("Proof of Work is Valid!")
else:
    print("Proof of Work Error.")
print()

# Details of the first block in the blockchain
print("\nDetails of First Block in Blockchain:")
block_info = network.blockchain.get_block_info(index=1)
for client, info in block_info.items():
    print(f"Client: {client}, Current Balance: {info['current']}, Min Balance: {info['min']}, Max Balance: {info['max']}")
print()

# Saving blockchain data to JSON
print("\nSaving Blockchain Data to JSON:")
network.save_to_json()
print()

# Validating data in reloaded blockchain
print("\nValidating Data in Reloaded Blockchain:")
print("Validation Successful!") if network.blockchain.validate() else print("Validation Error.")