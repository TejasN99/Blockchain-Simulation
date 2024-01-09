# BlockChain_Simulation
Simulation of a P2P Decentralized following high level Bitcoin Protocol

## Tasks pending:
- [x] Loopless forwarding
- [x] Add txns_in_blockchain to each block
- [x] Add seen_txns and leaf_blocks to each node
- [ ] Add initial generate_event for each block
- [ ] Handle events:
    - [x] Generate_txn:
        - add receive_events to all peers
    - [x] Receive_txn:
        - if txn not in seen_txns:
            - add txn to seen_txns
            - forward txn according to loopless forwarding
    - [ ] Generate_block:
        - modify leaf_nodes of the block appropriately        
        - add receive_events to all peers
        - start generating new block
            - Check if txn_pool of block has atleast 50 txns
                - If no, schedule generate_block with event_packet = None after 100 ms
                - If yes: select a subset of txns from txn_pool, add coinbase txn, calculate size of block and add
    - [ ] Receive block:
        - Check length from new block
            - if longer than current, remove current mining block
            - Update txn_pool of node by traversing back in blockchain, adding back transactions in the current chain and removing txns from new chain
            - start mining on new block
        - modify leaf_nodes appropriately
        - forward block according to loopless forwarding
