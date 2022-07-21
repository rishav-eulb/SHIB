#Miner
import SocketUtils
import Transactions
import TxBlock
import pickle


wallets = [('localhost',5006)]
tx_list = []
head_blocks=[None]
break_now = False
verbose = True

def StopAll():
    global break_now
    break_now = True
def minerServer(my_addr):
    global tx_list
    global break_now
    try:
        tx_list = loadTxList("Txs.dat")
        if verbose: print("Loaded tx_list has " + str(len(tx_list)) + " Txs.")
    except:
        print("No previous Txs. Starting fresh")
        tx_list = []
    head_blocks=[None]
    my_ip, my_port = my_addr
    server = SocketUtils.newServerConnection(my_ip,my_port)
    # Get Txs from wallets
    while not break_now:
        newTx = SocketUtils.recvObj(server)
        if isinstance(newTx,Transactions.Tx):
            tx_list.append(newTx)
            if verbose: print ("Recd tx")
    if verbose: print ("Saving " + str(len(tx_list)) + " txs to Txs.dat")
    saveTxList(tx_list,"Txs.dat")
    
    return False

def nonceFinder(wallet_list, miner_public):
    global break_now
    try:
        head_blocks = TxBlock.loadBlocks("AllBlocks.dat")
    except:
        print("No previous blocks found. Starting fresh.")
        head_blocks = TxBlock.loadBlocks("Genesis.dat")
    # add Txs to new block
    while not break_now:
        newBlock = TxBlock.TxBlock(TxBlock.findLongestBlockchain(head_blocks))
        placeholder = Transactions.Tx()
        placeholder.add_output(miner_public,25.0)
        newBlock.addTx(placeholder)
        #TODO sort tx_list by tx fee per byte
        for tx in tx_list:
            newBlock.addTx(tx)
            if not newBlock.check_size():
                newBlock.removeTx(tx)
                break
        newBlock.removeTx(placeholder)
        if verbose: print("new block has " + str(len(newBlock.data)) + " txs.")
        # Compute and add mining reward
        total_in,total_out = newBlock.count_totals()
        mine_reward = Transactions.Tx()
        mine_reward.add_output(miner_public,25.0+total_in-total_out)
        newBlock.addTx(mine_reward)
        # Find nonce
        if verbose: print ("Finding Nonce...")
        newBlock.find_nonce(10000)
        if newBlock.good_nonce():
            if verbose: print ("Good nonce found")
            head_blocks.remove(newBlock.previousBlock)
            head_blocks.append(newBlock)
            # Send new block
            savePrev = newBlock.previousBlock
            newBlock.previousBlock = None
            for ip_addr,port in wallet_list:
                if verbose: print ("Sending to " + ip_addr + ":" + str(port))
                SocketUtils.sendObj(ip_addr,newBlock,5006)
            newBlock.previousBlock = savePrev
            # Remove used txs from tx_list
            for tx in newBlock.data:
                if tx != mine_reward:
                    tx_list.remove(tx)
    TxBlock.saveBlocks(head_blocks,"AllBlocks.dat")                
    return True

def loadTxList(filename):
    fin = open(filename, "rb")
    ret = pickle.load(fin)
    fin.close()
    return ret

def saveTxList(the_list, filename):
    fp = open(filename, "wb")
    pickle.dump(the_list, fp)
    fp.close()
    return True

if __name__ == "__main__":
    
    import Signatures
    import threading
    import time
    my_pr, my_pu = Signatures.generate_keys()
    t1 = threading.Thread(target=minerServer, args=(('localhost',5005),))
    t2 = threading.Thread(target=nonceFinder, args=(wallets, my_pu))
    server = SocketUtils.newServerConnection('localhost',5006)
    t1.start()
    t2.start()
    pr1,pu1 = Signatures.generate_keys()
    pr2,pu2 = Signatures.generate_keys()
    pr3,pu3 = Signatures.generate_keys()

    Tx1 = Transactions.Tx()
    Tx2 = Transactions.Tx()

    Tx1.add_input(pu1, 4.0)
    Tx1.add_input(pu2, 1.0)
    Tx1.add_output(pu3, 4.8)
    Tx2.add_input(pu3, 4.0)
    Tx2.add_output(pu2, 4.0)
    Tx2.add_reqd(pu1)

    Tx1.sign(pr1)
    Tx1.sign(pr2)
    Tx2.sign(pr3)
    Tx2.sign(pr1)

    new_tx_list = [Tx1, Tx2]
    saveTxList(new_tx_list, "Txs.dat")
    new_new_tx_list = loadTxList("Txs.dat")
    

    for tx in new_new_tx_list:
        try:
            SocketUtils.sendObj('localhost',tx)
            print ("Sent Tx")
        except:
            print ("Error! Connection unsuccessful")

    for i in range(30):
        newBlock = SocketUtils.recvObj(server)
        if newBlock:
            break

    if newBlock.is_valid():
        print("Success! Block is valid")
    if newBlock.good_nonce():
        print("Success! Nonce is valid")
    for tx in newBlock.data:
        try:
            if tx.inputs[0][0] == pu1 and tx.inputs[0][1] == 4.0:
                print("Tx1 is present")
        except:
            pass
        try:
            if tx.inputs[0][0] == pu3 and tx.inputs[0][1] == 4.0:
                print("Tx2 is present")
        except:
            pass

    time.sleep(20)
    break_now=True
    time.sleep(2)
    server.close()




    t1.join()
    t2.join()

    print("Done!")
    










