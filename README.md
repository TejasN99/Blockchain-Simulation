# BlockChain_Simulation
Simulation of a P2P Decentralized following high level Bitcoin Protocol

## Tasks pending:
- [ ] Loopless forwarding
- [ ] Add txns_in_blockchain and leaf_nodes to each block
- [ ] Add seen_txns to each event
- [ ] Add initial generate_event for each block
- [ ] Append 500 generate_txns after initial n generate_event
- [ ] Handle events:
    - [ ] Generate_txn:
        - add receive_events to all peers
    - [ ] Receive_txn:
        - if txn not in seen_txns:
            - add txn to seen_txns
            - forward txn according to loopless forwarding
    - [ ] Generate_block:
        - modify leaf_nodes of the block appropriately
        - add receive_events to all peers
    - [ ] Receive block:
        - Check length from new block
            - if longer than current, remove current mining block
            - Update txn_pool of node by traversing back in blockchain, adding back transactions in the current chain and removing txns from new chain
            - start mining on new block
        - modify leaf_nodes appropriately
        - forward block according to loopless forwarding
