#We might need to initially broadcast the balances of each  node b4 starting the simulation

#events_list is a global list accessible to all the nodes in order to schedule their activities in a 
#timestamped manner

#To do:
#CoinBase : Txn Fomrat??
#Balance Sheet Maintenance?? Tricky for forks!

#What are the possbile events? List them down.
#Event 1. Generate Transaction: All nodes must generate traansactions periodically as it is an independent event
#Event 2. Mine Block: All nodes must kick-off mining once. 
                #Mining means colllecting a subset of txns from UTXO, verify if the block is valid by checking for negative balances and start mining
    #Upon Completion of "self-mined block":
                # a.Schedule another mining event when mining duration elapses (Duration can be pre-computed)
                # b.Add block  to miner's blockchain
                # c.Broadcast mined block amongst peers
                # d. Remove all these transactions from Unspent Transaction Pool of the Miner
                # e. Update the Balance Sheet of the Miner
                # f. Award itself the Mining Fee of 50 BTC$ (Think of logic when exactly when we want to award the fee?) 
                # g. ???? Anything else to be done????  
    #If someone's elses block wins, a node will verify the block. If verified: 
        #b,c,d,e remainds the same (We assume negigible delay in these steps as not mentioned in Assignment)
        #Additional actions:
        #f.Terminate the event of mining next block based on self-mined block (as it will be orphaned) and 
        #immediately start mining on a new block i.e. A Mine Block event will be genrated by the node
            # Think about resolution of forks here!! 

from random import randint
from numpy import random
import time
def network_topology():
    total_nodes=randint(10,20)
    #print("Total Nodes are",total_nodes)
    #Creating a random netowrk of nodes and checking if it connected or not 
    connected=False
    while not (connected):
        #Dictionary for number of nodes connected to each node
        node_connections={}
        node_graph={}
        #Initializing peer nodes to be empty for all nodes
        for i in range(total_nodes):
            node_graph[i+1]=[]
        for i in range(total_nodes):
            #Number of nodes connected to each node
            node_connections[i+1]=randint(4,8)
            count=len(node_graph[i+1])
            while count<node_connections[i+1]:
                node_num=randint(1,total_nodes)
                while node_num not in node_graph[i+1] and node_num!=(i+1):
                    #Add edges for both nodes since it is an undirected graph
                    node_graph[i+1].append(node_num)
                    node_graph[node_num].append(i+1)
                    count=count+1
        #Print num conecctions to each node
        # for key in node_connections.keys():
        #     print(key,node_connections[key])
        #Print list of peers for each node
        for key in node_graph.keys():
            print(key,node_graph[key])
        #Returns True or None 
        connected=check_connectedness([],node_graph,1,total_nodes)
    node_speed={}
    for i in range(total_nodes):
            if (i%2==0):
                node_speed[i+1]='Fast'
            else:
                node_speed[i+1]='Slow'
    node_hash={}
    for i in range(total_nodes):
            if (i%2==0):
                node_hash[i+1]='High'
            else:
                node_hash[i+1]='Low'                
    
    #Initial Node Balances
    init_node_bal={}
    for i in range(total_nodes):
        init_node_bal[i+1]=randint(0,100)

    return node_graph,node_speed,node_hash,total_nodes,init_node_bal  


#Periodically Generate Transactions
#To DO: Time Delay should be an exponenetial Distribution
#Check balance does not go negative upon txn generation
def gen_txns_periodically():
    txn_id=0
    t_end = time.time() + 1
    while time.time() < t_end:
        txn=Single_Transaction(txn_id)
        payer_node_id=randint(1,total_nodes)
        recipient_node_id=randint(1,total_nodes)
        while (recipient_node_id==payer_node_id):
            recipient_node_id=randint(1,total_nodes)
        amount=randint(0,100)
        txn.gen_txn_details(payer_node_id,recipient_node_id,amount)    
        txn_id=txn_id+1
        print("Txnid",txn_id,"Node ",payer_node_id," pays","Node ",recipient_node_id," ",amount," BTC$")
        #Global list containing list of events
        #Add time-stamp concept and event listed to be always sorted by time stamp
        event_list.append(["Single Transaction",txn])
        time.sleep(0.01)

#Check for connectedness
def check_connectedness(visited_nodes,node_graph,current_node,total_nodes):
    if current_node not in visited_nodes:
        visited_nodes.append(current_node)
        for peer_node in node_graph[current_node]:
            check_connectedness(visited_nodes,node_graph,peer_node,total_nodes)            
    
    if len(visited_nodes)==total_nodes:
        #print("Graph is connected!")
        #print(visited_nodes)
        return True
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
        #self.received_txn_ids=[]

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


def latency(sender_node,receiver_node,message_bits):
    if sender_node.speed=='Fast' and receiver_node.speed=='Fast':
        link_speed=100
    else:
        link_speed=5
    light_delay=randint(10,500)
    queue_delay=random.exponential(scale=96/link_speed)
    overall_delay=light_delay+(message_bits/link_speed)+queue_delay
    return overall_delay



#Testing working of Latency Calculations
def generate_latency_graph(node_graph):
    for i in range(len(node_graph)):
        for peer_node in node_graph[i+1]:
            overall_delay=latency(Node(i+1),Node(peer_node),1000)
            print("Sender=",i+1,"Receiver=",peer_node,"Latency",overall_delay)

node_graph,node_speed,node_hash,total_nodes,init_node_bal = network_topology()
generate_latency_graph(node_graph)
event_list = []
gen_txns_periodically()
for elem in event_list:
    print(elem)




#Function for latency
#Fucntion for slow and fast CPU/ fast and slow nodes
#Loopless Transaction Forward
#Define a transaction

#Event Scheduler
#What are the possible events?

#Pressing:
#Resolution of forks: Trigger an event periodically at each node to check for forks
#Initiate a transaction
