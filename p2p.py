 
from random import randint
from numpy import random
from event_classes import Event,Node
import time

#Simulation Parameters:
#Interarrival time between transactions
Ttx=10
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



def latency(sender_node,receiver_node,message_bits):
    if sender_node.speed=='Fast' and receiver_node.speed=='Fast':
        link_speed=100
    else:
        link_speed=5
    light_delay=randint(10,500)
    queue_delay=random.exponential(scale=96/link_speed)
    overall_delay=light_delay+(message_bits/link_speed)+queue_delay
    return overall_delay




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

class TxnEvent:
    def __init__(self,id):
        self.id=id
        self.type=""
        self.timestamp=0
        self.triggered_by=""
        self.details=""

class ReceiveEvent:
    def __init__(self,id):
        self.id=id
        self.type=""
        self.timestamp=0
        self.sender_node=""
        self.receiver_node=""
        self.details=""



def gen_first_txn():
    #event_id=global variable with inital value =0
    txn=Single_Transaction(event_id)
    payer_node_id=randint(1,total_nodes)
    recipient_node_id=randint(1,total_nodes)
    while (recipient_node_id==payer_node_id):
        recipient_node_id=randint(1,total_nodes)
    amount=randint(0,100)
    txn.gen_txn_details(payer_node_id,recipient_node_id,amount)    
    print("Txnid",0,"Node ",payer_node_id," pays","Node ",recipient_node_id," ",amount," BTC$ at 0",)
    event=TxnEvent(0)
    event.type="GenerateTxn"
    event.timestamp=0
    event.triggered_by=all_nodes_dict[payer_node_id]
    event.details=txn
    #Global list containing list of events
    event_list.append(event)




def gen_txn(event):
    event_id=event_id+1
    next_event_id=event_id
    txn=Single_Transaction(next_event_id)
    payer_node_id=randint(1,total_nodes)
    recipient_node_id=randint(1,total_nodes)
    while (recipient_node_id==payer_node_id):
        recipient_node_id=randint(1,total_nodes)
    amount=randint(1,100)
    txn.gen_txn_details(payer_node_id,recipient_node_id,amount)
    next_event=TxnEvent(next_event_id)
    next_event.type="GenerateTxn"
    next_event.timestamp=event.timestamp+random.exponential(scale=Ttx)
    next_event.triggered_by=all_nodes_dict[payer_node_id]
    next_event.details=txn
    print("Txnid",next_event_id,"Node ",payer_node_id," pays","Node ",recipient_node_id," ",amount," BTC$"," at ",next_event.timestamp)
    #Global list containing list of events
    event_list.append(next_event)

def gen_receive_txn(event,sender_node,receiver_node,message_size):
    event_id=event_id+1
    next_event_id=event_id
    next_event=ReceiveEvent(next_event_id)
    next_event.type="ReceiveTxn"
    next_event.timestamp=event.timestamp+latency(sender_node,receiver_node,message_size)
    next_event.sender_node=sender_node
    next_event.receiver_node=receiver_node
    next_event.details=event.details
    event_list.append(next_event)





#Periodically Generate Transactions
#To DO: Time Delay should be an exponenetial Distribution
#Check balance does not go negative upon txn generation




#Testing working of Latency Calculations
# def generate_latency_graph(node_graph):
#     for i in range(len(node_graph)):
#         for peer_node in node_graph[i+1]:
#             overall_delay=latency(Node(i+1),Node(peer_node),1000)
#             print("Sender=",i+1,"Receiver=",peer_node,"Latency",overall_delay)

#generate_latency_graph(node_graph)


#!!!!!!!!!!! MAIN!!!!!!!!!!!!!!!!!!!!!!!! 
node_graph,node_speed,node_hash,total_nodes,init_node_bal = network_topology()
#A Global Dictionary to Store node_num as key mapped to its node object
all_nodes_dict={}
#Initialzing Nodes:
for i in range(total_nodes):
    all_nodes_dict[i+1]=Node(i+1)
#def gen_receive(sender_node,receiver_node,message_details):

#Event Ids
event_id=0
event_list = []
gen_first_txn()
#Event Handler:
for event in event_list:
    if event.type=="GenerateTxn":
        #Generate Txn triggers another Generate Txn
        gen_txn(event)
        print("Initiator is",event.triggered_by.id)
        for peer in event.triggered_by.peers:
            message_delay=latency(event.triggered_by,all_nodes_dict[peer],1000)
            print("Latency is",message_delay)
            sender_node=event.triggered_by
            receiver_node=all_nodes_dict[peer]
            message_size=1024
            gen_receive_txn(event,sender_node,receiver_node,message_size)


            
        

        


#Function for latency
#Fucntion for slow and fast CPU/ fast and slow nodes
#Loopless Transaction Forward
#Define a transaction

#Event Scheduler
#What are the possible events?

#Pressing:
#Resolution of forks: Trigger an event periodically at each node to check for forks
#Initiate a transaction
