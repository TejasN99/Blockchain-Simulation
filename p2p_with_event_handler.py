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

import random as random_sample
from random import randint
from numpy import random
import time
import sys
import heapq as hq


class Node:
    def __init__(self, id, speed, hash_power):
        self.id = id
        self.speed = speed
        self.hash_power = hash_power
        self.unspent_txn_pool = []
        self.seen_txn_id=[]
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


class Single_Transaction:
    def __init__(self, id, payer_node, recipient_node, amount):
        self.id=id
        self.payer=payer_node
        self.recipient=recipient_node
        self.amount=amount


class Block:
    def __init__(self, id, txn_list, creator_node, parent, balance_sheet):
        self.id = id
        self.txn_list = txn_list
        self.creator_node = creator_node
        self.parent = parent
        self.balance_sheet = balance_sheet
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
        block_txns=creator_node.unspent_txn_pool[:num_txns]
        for txn in block_txns:
            self.txn_list.append(txn)


class Event:
    """
    A class to represent each Event

    Attributes
    ----------
    execution_time : int
        The time in milliseconds from the starting of the program when the event should get executed

    event_type : str
        Denotes the type of event. Would contain one among the four values: generate_txn, generate_block, receive_txn, receive_block

    event_packet
        Stores the class object of the associated block or transaction
    """
    def __init__(self, id, execution_time, event_type, event_packet, src_node, tgt_node = None):
        self.id = id
        self.execution_time = execution_time
        self.event_type = event_type
        self.event_packet = event_packet
        self.src_node = src_node
        self.tgt_node = tgt_node



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
        # for key in node_graph.keys():
        #     print(key,node_graph[key])
        #Returns True or None 
        connected=check_connectedness([],node_graph,1,total_nodes)
    
    no_of_slow_nodes = total_nodes * z0 // 100
    slow_nodes = random_sample.sample(range(1,total_nodes+1), no_of_slow_nodes)

    node_speed={}
    for i in range(1, total_nodes+1):
            if i in slow_nodes:
                node_speed[i]='Slow'
            else:
                node_speed[i]='Fast'

    no_of_lowCPU_nodes = total_nodes * z1 // 100
    lowCPU_nodes = random_sample.sample(range(1,total_nodes+1), no_of_lowCPU_nodes)

    node_hash={}
    for i in range(1, total_nodes+1):
            if i in lowCPU_nodes:
                node_hash[i]='Low'
            else:
                node_hash[i]='High'                
    
    #Initial Node Balances
    init_node_bal={}
    for i in range(total_nodes):
        init_node_bal[i+1]=randint(0,100)

    return node_graph,node_speed,node_hash,total_nodes,init_node_bal  


#Periodically Generate Transactions
#To DO: Time Delay should be an exponenetial Distribution
#Check balance does not go negative upon txn generation
def gen_initial_txns(ttx, current_time = 0):
    """
    Generates the next 500 transactions, with the inter-arrival between transactions generated by any peer chosen from an exponential distribution whose mean time is Ttx

    Parameters
    ----------
    ttx : int
        Used to choose the inter-arrival time between transactions
    
    current_time : int
        The current time in milliseconds

    Returns
    -------
    event_list : list
        List of the initial 100 events with their time of exexcution
    """

    # global nodes
    global txn_count
    global event_count

    prev_txn_time = current_time
    event_list = []
    num_intial_txns=10
    for i in range(num_intial_txns):        
        payer_node_id = randint(1,total_nodes)
        recipient_node_id = randint(1,total_nodes)
        while (recipient_node_id == payer_node_id):
            recipient_node_id = randint(1,total_nodes)
        amount = randint(1,100)
        txn = Single_Transaction(txn_count, nodes[payer_node_id], nodes[recipient_node_id], amount) 
        print("Txnid",txn_count,"Node ", payer_node_id," pays","Node ",recipient_node_id," ",amount," BTC$")
        txn_count += 1   
        duration = random.exponential(scale = ttx)        

        txn_execution_time = prev_txn_time + duration
        #print("txn execution time",txn_execution_time)
        txn_event = Event(event_count, txn_execution_time, "generate_txn", txn, nodes[payer_node_id])
        print("Event Count",event_count)
        event_count += 1
        
        #Global list containing list of events
        #Add time-stamp concept and event listed to be always sorted by time stamp
        hq.heappush(event_list,(txn_execution_time,txn_event))
        prev_txn_time = txn_execution_time
    return event_list


def start_mining(event_list):
    """
    The function adds a mining event for each node in the network

    Parameters
    ----------
    event_list : list
        List of events that has already been generated. The generate_block events are appended to this list.
    """
    pass

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
    queue_delay=random.exponential(scale=96/(link_speed * (2**10)))

    # light_delay is in ms, converting link_speed to bits/sec, later converting resulting time from s to ms, similarly converting queue_delay from s to ms
    overall_delay=light_delay + (message_bits/(link_speed*(2**20))) * 1000 + queue_delay * 1000
    return overall_delay



#Testing working of Latency Calculations
def generate_latency_graph(node_graph):
    for i in range(len(node_graph)):
        for peer_node in node_graph[i+1]:
            overall_delay=latency(Node(i+1),Node(peer_node), 8 * 2**20)
            print("Sender=",i+1,"Receiver=",peer_node,"Latency",overall_delay)


z0 = int(sys.argv[1])
z1 = int(sys.argv[2])
ttx = int(sys.argv[3])

txn_count = 1
block_count = 1
event_count = 1


node_graph = None
node_graph,node_speed,node_hash,total_nodes,init_node_bal = network_topology()

nodes={}
#Initialzing Nodes:
for i in range(total_nodes):
    nodes[i+1] = Node(i+1, node_speed[i+1], node_hash[i+1])

print("Total no. of nodes:", total_nodes)

# Replacing node IDs in node_graph with the node objects
for id in range(1, total_nodes+1):
    peer_nodes = []
    for peer_id in node_graph[id]:
        peer_nodes.append(nodes[peer_id])
    node_graph[nodes[id]] = peer_nodes
    del node_graph[id]


# printing node graph
for node in node_graph:
    print(node.id, node.speed, node.hash_power)
    # print()
    # print()
    peers = []
    for peer in node_graph[node]:
        peers.append(peer.id)
    print(" ".join(str(peer_id) for peer_id in peers))



if __name__ == "__main__":    
    # generate_latency_graph(node_graph)
    event_list = gen_initial_txns(ttx)

    #Event Handler
    print("Event list length is",len(event_list))
    while (len(event_list)!=0):
        tuple=hq.heappop(event_list)
        event=tuple[1]
        if event.event_type=="generate_txn":
            print("Detected Generate_txn")
            print("Execution_time is",event.execution_time)
            src_node=event.src_node
            src_node.seen_txn_id.append(event.event_packet.id)
            for peer_node in node_graph[src_node]:
                #message size of single trasaction is 1024 bits
                prev_execution_time=event.execution_time
                print("Previous exec time of event is",prev_execution_time)
                latency_delay=latency(src_node,peer_node,1024)
                execution_time=prev_execution_time+latency_delay
                print("New exec time of event is",execution_time)
                event_packet=event.event_packet
                print("Latency between",src_node.id," ",peer_node.id,"is ",latency_delay)
                print("Event Count",event_count)
                event_count+=1
                receive_event=Event(event_count,execution_time,"receive_txn",event_packet,src_node,peer_node)
                hq.heappush(event_list,(execution_time,receive_event))

        elif event.event_type=="generate_block":
            pass
        elif event.event_type=="receive_txn":
            #the target node of previous event is the source node for the next receive event triggered
            src_node=event.tgt_node
            prev_src_node=event.src_node
            print("Detected Receive_txn!!")
            print("Execution_time is",event.execution_time)
            if (event.event_packet.id not in src_node.seen_txn_id):
                print("Sendin Txn id",event.event_packet.id,"from node",src_node.id,"to its peers")
                src_node.seen_txn_id.append(event.event_packet.id)
                for peer_node in node_graph[src_node]:
                    if (peer_node.id != prev_src_node.id):
                        print("Generating receive txn from node ",src_node.id,"to peer node ",peer_node.id)
                        #message size of single trasaction is 1024 bits
                        prev_execution_time=event.execution_time
                        print("Previous exec time of event is",prev_execution_time)
                        latency_delay=latency(src_node,peer_node,1024)
                        execution_time=prev_execution_time+latency_delay
                        print("New exec time of event is",execution_time)
                        event_packet=event.event_packet
                        print("Latency between",src_node.id," ",peer_node.id,"is ",latency_delay)
                        print("Event Count",event_count)
                        event_count+=1
                        receive_event=Event(event_count,execution_time,"receive_txn",event_packet,src_node,peer_node)
                        hq.heappush(event_list,(execution_time,receive_event))
                    else:
                        print("Not sending receive txn from node ",src_node.id,"to peer node ",peer_node.id,"since packet came from there!")

            else:
                print("Discarding Txn id",event.event_packet.id,"as it already sent from node",src_node.id)



        elif event.event_type=="receive_block":
            pass 
    print("Event list length is",len(event_list))
    # count=0
    # for id in nodes.keys():
    #     count+=1
    #     print("Length of seen_txn_id is",len(nodes[id].seen_txn_id))
    #     for seen_txn_id in nodes[id].seen_txn_id:
    #         print(seen_txn_id)
    # print(count)





#Function for latency
#Fucntion for slow and fast CPU/ fast and slow nodes
#Loopless Transaction Forward
#Define a transaction

#Event Scheduler
#What are the possible events?

#Pressing:
#Resolution of forks: Trigger an event periodically at each node to check for forks
#Initiate a transaction



# def handle_events(event_queue, cur_time):
#     while event_queue[0].execution_time <= cur_time:
#         if event_queue[0].event_type == "txn":



# starting_time