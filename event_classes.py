class Node:
    def __init__(self,id):
        self.id=id
        self.peers=node_graph[id]
        self.speed=node_speed[id]
        self.hash_power=node_hash[id]
        self.unspent_txn_pool=[]
        #Bal_Sheet better at Block Level
        #self.bal_sheet={}
        #What will be the structire of the blockchain:
        #1. Should be linked to the previous block
        #2. Each should be an instance of the "Block" class
        #Structure should be probbly a tree???
        #self.blochchain
        self.received_txn_ids=[]

    #txn will be of Class "Single_Transaction"
    def add_to_txn_pool(self,txn):
        self.unspent_txn_pool.append(txn)


    def broadcast():
        pass

class Single_Transaction:
    def __init__(self,id):
        self.id=id
    def gen_txn_details(self,payer_node_id,recipient_node_id,amount):
        self.payer=payer_node_id
        self.recipient=recipient_node_id
        self.amount=amount 

def Broadcast(transaction):
    pass





class Block:
    def __init__(self,id):
        self.id=id
        self.txn_list=[]
        self.miner_node=None
        #self.parent??
        #self.balance_sheet?

    #txn will be of Class "Single_Transaction"
    def add_txn_to_block(self,txn):
        self.txn_list.append(txn)

    #creator_node will of class "Node"
    def mine_Block(self,creator_node):
    #Upon Block Mining:
    #1. Miner Node Assigned
    #2. A random list of transactions picked from miner node's pool and added to block transaction list
    #3. Mining Time is pre-computed and another mine_block event is scheduled when mining duration is elasped    
        self.miner_node=creator_node
        #% of transactions randomly picked from trasnsaction pool of creator_node
        #Num Transactions
        perct_txns=randint(10,50)
        num_txns=int(len(creator_node.unspent_txn_pool) *perct_txns/100)
        print("Total ", len(creator_node.unspent_txn_pool),"txns")
        print("Picked ",num_txns," txns")
        block_txns=creator_node.unspent_txn_pool[:-num_txns]
        for txn in block_txns:
            self.add_txn_to_block(txn)

class Event:
    def __init__(self,id):
        self.id=id
        self.type=""
        self.timestamp=0
        self.triggered_by=Node(1)
        self.details=""
