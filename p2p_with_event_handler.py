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
    def __init__(self, id, speed, hash_power, genesis_block, avg_mining_time):
        self.id = id
        self.speed = speed
        self.hash_power = hash_power
        self.unspent_txn_pool = []
        self.seen_txn_id=[]
        self.leaf_blocks = [genesis_block]
        self.mining_on = genesis_block
        self.avg_mining_time = avg_mining_time
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

    def add_block_to_leaf_blocks(self, new_block):
        fork_flag = 1
        for leaf_block in self.leaf_blocks:
            if leaf_block.id == new_block.parent.id:
                fork_flag = 0
                self.leaf_blocks.remove(leaf_block)
                self.leaf_blocks.append(new_block)
        
        if fork_flag == 1:
            self.leaf_blocks.append(new_block)




class Single_Transaction:
    def __init__(self, payer_node, recipient_node, amount):
        global txn_count
        self.id=txn_count
        self.payer=payer_node
        self.recipient=recipient_node
        self.amount=amount
        txn_count += 1


class Block:
    def __init__(self, creator_node, parent, txn_list, balance_sheet):
        global block_count
        self.id = block_count
        self.creator_node = creator_node
        self.parent = parent
        self.balance_sheet = balance_sheet   

        # block_count = 0 means Genesis block             
        if block_count == 0:
            self.chain_length = 0
            self.txn_list = [] 
            self.txns_in_blockchain = []
        else:
            self.chain_length = parent.chain_length + 1
            self.txn_list = txn_list
            self.txns_in_blockchain = parent.txns_in_blockchain + txn_list
        self.block_size = (1024*8) + (1024*8*len(txn_list))
        block_count += 1
            #Upon Block Mining:
            #1. Miner Node Assigned
            #2. A random list of transactions picked from miner node's pool and added to block transaction list
            #3. Mining Time is pre-computed and another mine_block event is scheduled when mining duration is elasped            
            #% of transactions randomly picked from trasnsaction pool of creator_node
            #Num Transactions
            


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
    def __init__(self, execution_time, event_type, event_packet, src_node, tgt_node = None):
        global event_count
        self.id = event_count
        self.execution_time = execution_time
        self.event_type = event_type
        self.event_packet = event_packet
        self.src_node = src_node
        self.tgt_node = tgt_node
        event_count += 1

#Returns 
# 1) A list of valid  txns 
# 2) Balance sheet of the new block that will be generated
def generate_valid_txn_list(node):
    print("generate_valid_txn_list for node ",node.id)
    print("Length of unspent_txn_pool of node:",len(node.unspent_txn_pool))
    if len(node.unspent_txn_pool) < 1:  ## UNDO
        print("Stuck at 144")
        print(event_count)
        # print("Length of txn_pool too small, returning None")
        return None, None

    txns_valid_flag = 0
    no_of_attempts = 0
    max_no_of_attempts = 50 #UNDO
    while txns_valid_flag == 0 and no_of_attempts != max_no_of_attempts:
        num_txns=min(10, len(node.unspent_txn_pool))
        #num_txns = randint(1, min(3, len(node.unspent_txn_pool)))     ## UNDO
        # num_txns = randint(1,min(1023, len(node.unspent_txn_pool)))
        txn_list = [node.unspent_txn_pool[i] for i in sorted(random_sample.sample(range(len(node.unspent_txn_pool)), num_txns))]
        balance_sheet = node.mining_on.balance_sheet.copy()
        txns_valid_flag = 1
        for txn in txn_list:
            if balance_sheet[txn.payer.id] < txn.amount:
                txns_valid_flag = 0
                break
            else:
                balance_sheet[txn.payer.id] -= txn.amount
                balance_sheet[txn.recipient.id] += txn.amount

        no_of_attempts += 1

    if txns_valid_flag == 0 and no_of_attempts == max_no_of_attempts:
        return None, None
    else:

        f1.write("Node:" + str(node.id) + "\n")
        f1.write("Transactions in unspent_txn_pool:" + "\n")
        for txn in node.unspent_txn_pool:
            f1.write(str(txn.id) + " ")
        f1.write("\n")
        f1.write("Transactions in block\'s txn_pool:" + "\n")
        for txn in txn_list:
            f1.write(str(txn.id) + " ")
        f1.write("\n\n")
        

        coinbase_txn = Single_Transaction(None, node, 50)
        print("Coinbase generated with ID", coinbase_txn.id)
        txn_list.append(coinbase_txn)
        balance_sheet[node.id] += 50    # Coinbase txn
        return txn_list, balance_sheet

    #     # Max no of txns allowed in a block is 1023
    #     # num_txns = randint(10,min(1023, len(node.unspent_txn_pool)))
    #     num_txns = randint(1,min(1023, len(node.unspent_txn_pool)))
    #     print("Total ", len(node.unspent_txn_pool),"txns")
    #     print("Picked ",num_txns," txns")
    #     txn_list = random_sample.sample(node.unspent_txn_pool, num_txns)
    #     balance_sheet = node.mining_on.balance_sheet.copy()
    #     txns_valid_flag = 1
    #     invalid_txns = []
    #     print(balance_sheet)
    #     for txn in txn_list:
    #         if balance_sheet[txn.payer.id] < txn.amount:
    #             invalid_txns.append(txn)
    #         else:
    #             balance_sheet[txn.payer.id] -= txn.amount
    #             balance_sheet[txn.recipient.id] += txn.amount
        
    #     for txn in invalid_txns:
    #         print("Payer:", txn.payer.id)
    #         print("Recipient:", txn.recipient.id)
    #         print("Amount:", txn.amount)

    #     for txn in invalid_txns:
    #         if balance_sheet[txn.payer.id] < txn.amount:
    #             txns_valid_flag = 0
    #             break
    #         else:
    #             balance_sheet[txn.payer.id] -= txn.amount
    #             balance_sheet[txn.recipient.id] -= txn.amount
    #     no_of_attempts += 1
    
    # if no_of_attempts == max_no_of_attempts:
    #     return None, None
    # else:
    #     coinbase_txn = Single_Transaction(None, node, 50)
    #     txn_list.append(coinbase_txn)
    #     balance_sheet[node.id] += 50    # Coinbase txn
    #     return txn_list, balance_sheet

def network_topology():
    # total_nodes=randint(10,20)
    total_nodes = randint(3,4)      ## UNDO
    #print("Total Nodes are",total_nodes)
    #Creating a random network of nodes and checking if it connected or not 
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
            # node_connections[i+1]=randint(4,8)
            node_connections[i+1]=randint(1,2) ## UNDO
            # node_connections[i+1]=randint(2,3)
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
        init_node_bal[i+1]=randint(1000,10000)

    return node_graph,node_speed,node_hash,total_nodes,init_node_bal  


#Periodically Generate Transactions
#To DO: Time Delay should be an exponenetial Distribution
#Check balance does not go negative upon txn generation
def gen_initial_txns():
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

    global nodes
    global txn_count
    global event_count

    event_list = []

    # Minimal execution_time difference to sort event_list
    c = 0
    for node in nodes.values():     
        payer_node_id = node.id
        recipient_node_id = randint(1,total_nodes)
        while (recipient_node_id == payer_node_id):
            recipient_node_id = randint(1,total_nodes)
        amount = randint(1,20)
        txn = Single_Transaction(nodes[payer_node_id], nodes[recipient_node_id], amount)
        print("Txnid",txn_count,"Node ", payer_node_id," pays","Node ",recipient_node_id," ",amount," BTC$")

        #print("txn execution time",txn_execution_time)
        txn_event = Event(c, "generate_txn", txn, nodes[payer_node_id])
        print("Event Count",event_count)
        
        #Global list containing list of events
        #Add time-stamp concept and event listed to be always sorted by time stamp
        hq.heappush(event_list,(c,txn_event))
        c += 1
    return event_list


def start_mining(event_list, ttx):
    """
    The function adds a mining event for each node in the network

    Parameters
    ----------
    event_list : list
        List of events that has already been generated. The generate_block events are appended to this list.
    """
    c = 0
    for node in nodes.values():
        # mining_time = random.exponential(scale = node.avg_mining_time)
        # execution_time = cur_time + mining_time
        # txn_list, new_balance_sheet = generate_valid_txn_list(node)
        # if txn_list == None:
        #     retry_mining_event = Event(cur_time + 50, "retry_mining", None, node)
        #     # hq.heappush(event_list,(cur_time + 50, retry_mining_event))
        # else:
        #     new_block = Block(node, node.mining_on, txn_list, new_balance_sheet)
        #     mining_event = Event(execution_time, "generate_block", new_block, node)
        #     hq.heappush(event_list,(execution_time, mining_event))
        retry_mining_event = Event(ttx + c, "retry_mining", None, node)
        hq.heappush(event_list, (ttx + c, retry_mining_event))
        c += 1    

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


# #Testing working of Latency Calculations
# def generate_latency_graph(node_graph):
#     for i in range(len(node_graph)):
#         for peer_node in node_graph[i+1]:
#             overall_delay=latency(Node(i+1),Node(peer_node), 8 * 2**20)
#             print("Sender=",i+1,"Receiver=",peer_node,"Latency",overall_delay)


def restart_mining(node, event_list, new_block, cur_execution_time):
    for event in event_list:
        if event[1].src_node == node and event[1].event_type == "generate_block":
            event_list.remove(event)
            hq.heapify(event_list)
            break
    node.mining_on = new_block
    txn_list, new_balance_sheet = generate_valid_txn_list(node)
    if txn_list == None:
        retry_mining_event = Event(cur_execution_time + 5*ttx, "retry_mining", None, node)
        hq.heappush(event_list, (cur_execution_time + 5*ttx, retry_mining_event))
    else:
        mining_time = random.exponential(scale = node.avg_mining_time)
        execution_time = cur_execution_time + mining_time
        new_block = Block(node, node.mining_on, txn_list, new_balance_sheet)
        mining_event = Event(execution_time, "generate_block", new_block, node)
        hq.heappush(event_list,(execution_time, mining_event))


def event_handler(event_list, event, ttx):
    if event.event_type=="generate_txn":
        global txn_count        
        print("Detected Generate_txn")
        # print("Execution_time is",event.execution_time)
        src_node=event.src_node
        src_node.seen_txn_id.append(event.event_packet.id)
        src_node.unspent_txn_pool.append(event.event_packet)
        print("Generate Txn: Appended to UTXO of source node ",src_node.id)
        print("Length of UTXO is",len(src_node.unspent_txn_pool))
        for peer_node in node_graph[src_node]:
            #message size of single trasaction is 1024*8 bits
            prev_execution_time=event.execution_time
            # print("Previous exec time of event is",prev_execution_time)
            latency_delay=latency(src_node,peer_node,1024*8)
            execution_time=prev_execution_time+latency_delay
            # print("New exec time of event is",execution_time)
            event_packet=event.event_packet
            # print("Latency between",src_node.id," ",peer_node.id,"is ",latency_delay)
            # print("Event Count",event_count)
            receive_event=Event(execution_time,"receive_txn",event_packet,src_node,peer_node)
            hq.heappush(event_list,(execution_time,receive_event))
        
        if txn_count > 500:
            print("Shashank")
            return

        # One generate_txn event spawns the next generate_txn event from the same node
        payer_node_id = src_node.id
        recipient_node_id = randint(1,total_nodes)
        while (recipient_node_id == payer_node_id):
            recipient_node_id = randint(1,total_nodes)
        amount = randint(1,20)
        txn = Single_Transaction(nodes[payer_node_id], nodes[recipient_node_id], amount) 
        # print("Txnid",txn_count,"Node ", payer_node_id," pays","Node ",recipient_node_id," ",amount," BTC$")
        new_txn_duration = random.exponential(scale = ttx)
        new_txn_event = Event(event.execution_time + new_txn_duration, "generate_txn", txn, nodes[payer_node_id])
        hq.heappush(event_list,(event.execution_time + new_txn_duration,new_txn_event))

    elif event.event_type=="generate_block":        
        #print("Execution_time is",event.execution_time)
        src_node = event.src_node
        new_block = event.event_packet
        print("Detected Generate_block",new_block.id, "from node",event.src_node.id)
        # print("Mining on:", src_node.mining_on.id)
        # print("Leaf Nodes:")
        # for node in src_node.leaf_blocks:
        #     print(node.id)
        src_node.leaf_blocks.remove(src_node.mining_on)
        src_node.leaf_blocks.append(new_block)
        src_node.mining_on = new_block
        print("UTXO Length b4 block generation",len(src_node.unspent_txn_pool))

        # Removing the txns in new block from the node's unspent_txn_pool
        for txn in new_block.txn_list:
            try:
                if txn in src_node.unspent_txn_pool:
                    src_node.unspent_txn_pool.remove(txn)
                    print("Removed from UTXO Txn id",txn.id)
            except Exception as err:
                print("Encountered error:", err)
                print("Node:" + str(src_node.id))
                print("Transactions in block:")
                for txn in new_block.txn_list:
                    print(txn.id, end = " ")
                print()
                print("Transactions in unspent_txn_pool:")
                for txn in src_node.unspent_txn_pool:
                    print(txn.id, end = " ")
                print()
                print("Seen txns:")
                
                for txn_id in src_node.seen_txn_id:
                    print(txn_id,end = " ")
                print("txn_count:", txn_count)
                write_logs(event_list)
                exit()


        print("UTXO Length after block generation",len(src_node.unspent_txn_pool))
        for peer_node in node_graph[src_node]:
            prev_execution_time=event.execution_time
            print("Previous exec time of event is",prev_execution_time)
            latency_delay=latency(src_node, peer_node, new_block.block_size)
            execution_time=prev_execution_time+latency_delay
            print("New exec time of event is",execution_time)
            print("Latency between",src_node.id," ",peer_node.id,"is ",latency_delay)
            print("Event Count",event_count)
            receive_event=Event(execution_time,"receive_block",new_block,src_node,peer_node)
            hq.heappush(event_list,(execution_time,receive_event))
        

        new_txn_list, balance_sheet = generate_valid_txn_list(src_node)
        if new_txn_list == None:
            retry_mining_event = Event(5*ttx + event.execution_time, "retry_mining", None, src_node)
            hq.heappush(event_list, (5*ttx + event.execution_time, retry_mining_event))
        else:
            next_block = Block(src_node, src_node.mining_on, new_txn_list, balance_sheet)
            print("Node", src_node.id,"started mining new block")
            mining_duration = random.exponential(scale = src_node.avg_mining_time)
            new_mining_event = Event(event.execution_time + mining_duration, "generate_block", next_block, src_node)
            hq.heappush(event_list,(event.execution_time + mining_duration, new_mining_event))

    elif event.event_type=="receive_txn":
        #the target node of previous event is the source node for the next receive event triggered
        src_node=event.tgt_node
        prev_src_node=event.src_node
        print("Detected Receive_txn from node",prev_src_node.id,"to node ",src_node.id)
        # print("Execution_time is",event.execution_time)
        if (event.event_packet.id not in src_node.seen_txn_id):
            # print("Sendin Txn id",event.event_packet.id,"from node",src_node.id,"to its peers")
            src_node.seen_txn_id.append(event.event_packet.id)
            # print("unspent_txn_pool",src_node.unspent_txn_pool)
            if event.event_packet not in src_node.unspent_txn_pool:
                print("Inside receive_txn, appending txn to unspent_txn_pool")
                src_node.unspent_txn_pool.append(event.event_packet)
                print("Receive Txn: Appended to UTXO of source node ",src_node.id)
                print("Length of UTXO is",len(src_node.unspent_txn_pool))
            else:
                print("Receive Txn: Txn already in UTXO")
            for peer_node in node_graph[src_node]:
                if (peer_node.id != prev_src_node.id):
                    # print("Generating receive txn from node ",src_node.id,"to peer node ",peer_node.id)
                    #message size of single trasaction is 1024*8 bits
                    prev_execution_time=event.execution_time
                    # print("Previous exec time of event is",prev_execution_time)
                    latency_delay=latency(src_node,peer_node,1024*8)
                    execution_time=prev_execution_time+latency_delay
                    # print("New exec time of event is",execution_time)
                    event_packet=event.event_packet
                    # print("Latency between",src_node.id," ",peer_node.id,"is ",latency_delay)
                    # print("Event Count",event_count)
                    receive_event=Event(execution_time,"receive_txn",event_packet,src_node,peer_node)
                    hq.heappush(event_list,(execution_time,receive_event))
                else:
                    pass
                    # print("Not sending receive txn from node ",src_node.id,"to peer node ",peer_node.id,"since packet came from there!")

        else:
            pass
            # print("Discarding Txn id",event.event_packet.id,"as it already sent from node",src_node.id)



    elif event.event_type=="receive_block":
        # Checking if the block received is already in blockchain of the node
        prev_src_node = event.src_node
        src_node = event.tgt_node
        new_block = event.event_packet
        cur_time = event.execution_time

        print("Detected Receive block",new_block.id, "from node",prev_src_node.id,"to node ",src_node.id)
        #print("Previous exec time of event is",cur_time)
        already_seen_flag = 0
        for leaf_block in src_node.leaf_blocks:
            block = leaf_block
            while block.id != 0:
                if block == new_block:
                    already_seen_flag = 1
                    break
                block = block.parent
            if already_seen_flag == 1:
                break
        
        # If block is already in blockchain, we do not forward it again
        if already_seen_flag == 0:
            if new_block.parent in src_node.leaf_blocks:
                src_node.leaf_blocks.remove(new_block.parent)
            src_node.leaf_blocks.append(new_block)
            for peer_node in node_graph[src_node]:
                if (peer_node.id != prev_src_node.id):
                    print("Generating receive block from node ",src_node.id,"to peer node ",peer_node.id)
                    #message size of single trasaction is 1024*8 bits                    
                    latency_delay=latency(src_node,peer_node,new_block.block_size)
                    execution_time = cur_time + latency_delay
                    print("New exec time of event is",execution_time)
                    print("Latency between",src_node.id," ",peer_node.id,"is ",latency_delay)
                    print("Event Count",event_count)
                    receive_event = Event(execution_time,"receive_block", new_block, src_node, peer_node)
                    hq.heappush(event_list,(execution_time,receive_event))
                else:
                    print("Not sending receive block from node ",src_node.id,"to peer node ",peer_node.id,"since packet came from there!")

            if new_block.parent == src_node.mining_on:
                restart_mining(src_node, event_list, new_block, event.execution_time)

            elif new_block.chain_length > src_node.mining_on.chain_length:
                current_mining_chain = []
                block = src_node.mining_on
                while(block.id != 0):
                    current_mining_chain.append(block)
                    block = block.parent

                new_block_chain = []
                block = new_block
                while(block.id != 0):
                    new_block_chain.append(block)
                    block = block.parent

                print("current_mining_chain:", current_mining_chain)
                print("new_block_chain:", new_block_chain)
                if current_mining_chain != []:
                    print("len of current_mining_chain:", len(current_mining_chain))
                    print("len of new_block_chain:", len(new_block_chain))
                    while(current_mining_chain[-1] == new_block_chain[-1]):
                        del current_mining_chain[-1]
                        del new_block_chain[-1]
                        
                        # If new block came earlier than parent and both nodes are in the same chain
                        if current_mining_chain == []:
                            break

                    
                for block in current_mining_chain:
                    for txn in block.txn_list:
                        if txn in src_node.seen_txn_id:
                            src_node.unspent_txn_pool.append(txn)
                for block in new_block_chain:
                    for txn in block.txn_list:
                        if txn in src_node.unspent_txn_pool:
                            src_node.unspent_txn_pool.remove(txn)
                
                # Killing the current mining of the node since longer chain was found
                restart_mining(src_node, event_list, new_block, event.execution_time)
             
    
    elif event.event_type == "retry_mining":
        src_node = event.src_node
        cur_time = event.execution_time        
        txn_list, new_balance_sheet = generate_valid_txn_list(src_node)
        if txn_list == None:
            retry_mining_event = Event(cur_time + 5*ttx, "retry_mining", None, src_node)
            hq.heappush(event_list, (cur_time + 5*ttx, retry_mining_event))
        else:
            mining_time = random.exponential(scale = src_node.avg_mining_time)
            execution_time = cur_time + mining_time
            new_block = Block(src_node, src_node.mining_on, txn_list, new_balance_sheet)
            mining_event = Event(execution_time, "generate_block", new_block, src_node)
            hq.heappush(event_list,(execution_time, mining_event))


def write_logs(event_list):
    global nodes
    f = open("log_" + str(cur_time) + ".txt", "w")
    f.write("Number of nodes: " + str(total_nodes) +"\n")
    for node in nodes.values():
        f.write("\nNode ID: " + str(node.id) + "\n")
        f.write("Number of txns in unspent_txn_pool: " + str(len(node.unspent_txn_pool)) + "\n")
        f.write("Currently mining on: " + str(node.mining_on.id) + "\n")
        f.write("Number of leaf blocks: " + str(len(node.leaf_blocks)))

    f.write("\nCurrent Time: " + str(cur_time))
    f.write("\n\nCurrent state of event_list:\n")
    for event in event_list:
        f.write(event[1].event_type + " at " + str(event[0]) + "\n")
        f.write("src_node: " + str(event[1].src_node.id) + "\n")
        if event[1].event_type != "retry_mining":
            f.write("Event Packet ID: " + str(event[1].event_packet.id) + "\n")
        
    f.close()

z0 = int(sys.argv[1])
z1 = int(sys.argv[2])
ttx = int(sys.argv[3])

# Inter-arrival time between blocks is set to 10 mins
I = 60
txn_count = 1
block_count = 0
event_count = 1


node_graph = None
node_graph,node_speed,node_hash,total_nodes,init_node_bal = network_topology()


f = open("log.txt", "w")
f1 = open("txn_pools.txt", "w")


for node in node_graph:
    f.write(str(node) + ": " +  str(node_graph[node]) + "\n")

genesis_block = Block(None, None, [], init_node_bal)
no_of_lowCPU_nodes = total_nodes * z1 // 100
no_of_highCPU_nodes = total_nodes - no_of_lowCPU_nodes
lowCPU_hashing_power = 1/(no_of_lowCPU_nodes + 10*no_of_highCPU_nodes)
highCPU_hashing_power = 10/(no_of_lowCPU_nodes + 10*no_of_highCPU_nodes)

nodes={}
#Initialzing Nodes:
for i in range(total_nodes):
    if node_hash[i+1] == "Low":
        nodes[i+1] = Node(i+1, node_speed[i+1], node_hash[i+1], genesis_block, I/lowCPU_hashing_power)
    else:
        nodes[i+1] = Node(i+1, node_speed[i+1], node_hash[i+1], genesis_block, I/highCPU_hashing_power)

print("Total no. of nodes:", total_nodes)

# Replacing node IDs in node_graph with the node objects
for id in range(1, total_nodes+1):
    peer_nodes = []
    for peer_id in node_graph[id]:
        peer_nodes.append(nodes[peer_id])
    node_graph[nodes[id]] = peer_nodes
    del node_graph[id]


# # printing node graph
# for node in node_graph:
#     print(node.id, node.speed, node.hash_power)
#     # print()
#     # print()
#     peers = []
#     for peer in node_graph[node]:
#         peers.append(peer.id)
#     print(" ".join(str(peer_id) for peer_id in peers))



if __name__ == "__main__":    
    # generate_latency_graph(node_graph)
    event_list = gen_initial_txns()
    start_mining(event_list, ttx)
    #Event Handler
    print("Event list length is",len(event_list))
    print("Events in event_list:")
    for event in event_list:
        print(event[1].event_type,"at", event[0])

    cur_time = 1    # Represents each ms
    while (len(event_list)!=0):

        # if len(event_list) > 100:
        #     break
        try:        ## UNDO
            event  = hq.heappop(event_list)[1]
        except Exception as e:
            print("Exception:",e)
            conflict_event1 = event_list[0]
            for c_event in event_list[1:]:
                if conflict_event1[0] == event[0]:
                    print(conflict_event1[1].event_type)
                    print(c_event[1].event_type)
        f.write("Type of Event:" + event.event_type + "\n")
        f.write("Source Node:" + str(event.src_node.id) + "\n")
        if event.tgt_node != None:
            f.write("Target Node:" + str(event.tgt_node.id) + "\n")
        f.write("Execution Time:" + str(event.execution_time) + "\n")
        if event.event_packet != None:
            f.write("Packet ID:" + str(event.event_packet.id) + "\n")
        event_handler(event_list, event, ttx)
        # print("Event list length is",len(event_list))

    print("Initial txns done!")    
    print(cur_time)
    
    # while (len(event_list)!=0):

    #     # if len(event_list) > 100:
    #     #     break

    #     if event_list[0][0] <= cur_time:
    #         event = hq.heappop(event_list)[1]
    #         event_handler(event_list, event, ttx)
    #     if total_nodes == len(event_list):
    #         print("Event list length is",len(event_list))
    #     cur_time += 1

    # print(len(event_list))
    # print(total_nodes)
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