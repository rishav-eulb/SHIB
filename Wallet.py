#Wallet
import SocketUtils
import Transactions
import TxBlock
import pickle
import Signatures

head_blocks = [None]
wallets = [('localhost',5006)]
miners = [('localhost',5005)]
break_now = False
verbose = True
my_public,my_private = Signatures.generate_keys()

def StopAll():
    global break_now
    break_now = True
def walletServer(my_addr):
    global head_blocks
    try:
        head_blocks = TxBlock.loadBlocks("WalletBlocks.dat")
    except:
        print("WS:No previous blocks found. Starting fresh.")
        head_blocks = TxBlock.loadBlocks("Genesis.dat")
    server = SocketUtils.newServerConnection('localhost',5006)
    while not break_now:
        newBlock = SocketUtils.recvObj(server)
        if isinstance(newBlock,TxBlock.TxBlock):
            if verbose: print("Rec'd block")
            found = False
            for b in head_blocks:
                if b == None:
                    if newBlock.previousHash == None:
                        found = True
                        newBlock.previousBlock = b
                        if not newBlock.is_valid():
                            print("Error! newBlock is not valid")
                        else:
                            head_blocks.remove(b)
                            head_blocks.append(newBlock)
                            if verbose: print("Added to head_blocks")
                elif newBlock.previousHash == b.computeHash():
                    found = True
                    newBlock.previousBlock = b
                    if not newBlock.is_valid():
                        print("Error! newBlock is not valid")
                    else:
                        head_blocks.remove(b)
                        head_blocks.append(newBlock)
                        if verbose: print("Added to head_blocks")
                else:
                    this_block = b
                    while this_block != None:
                        if newBlock.previousHash == this_block.previousHash:
                            found = True
                            newBlock.previousBlock = this_block.previousBlock
                            if not newBlock in head_blocks:
                                head_blocks.append(newBlock)
                                if verbose: print("Added new sister block")

                        this_block = this_block.previousBlock
                if not found:
                    print ("Error! Couldn't find a parent for newBlock")
                    #TODO handle orphaned blocks 
    TxBlock.saveBlocks(head_blocks,"WalletBlocks.dat")
    server.close()
    return True
        
def getBalance(pu_key):
    long_chain = TxBlock.findLongestBlockchain(head_blocks)
    return TxBlock.getBalance(pu_key,long_chain)


def sendCoins(pu_send, amt_send, pr_send, pu_recv, amt_recv, miner_list):
    newTx = Transactions.Tx()
    newTx.add_input(pu_send, amt_send)
    newTx.add_output(pu_recv, amt_recv)
    newTx.sign(pr_send)
    for ip,port in miner_list:
        SocketUtils.sendObj(ip,newTx,port)
    return True

def loadKeys(pr_file, pu_file):
    return Signatures.loadPrivate(pr_file), Signatures.loadPublic(pu_file)


if __name__ == "__main__":
    
    import time
    import Miner
    import threading
    import Signatures
    miner_pr, miner_pu = Signatures.generate_keys()
    t1 = threading.Thread(target=Miner.minerServer, args=(('localhost',5005),))
    t2 = threading.Thread(target=Miner.nonceFinder, args=(wallets, miner_pu))
    t3 = threading.Thread(target=walletServer, args=(('localhost',5006),))
    t1.start()
    t2.start()
    t3.start()

    pr1,pu1 = loadKeys("private.key","public.key")
    pr2,pu2 = Signatures.generate_keys()
    pr3,pu3 = Signatures.generate_keys()

    #Query balances
    bal1 = getBalance(pu1)
    print(bal1)
    bal2 = getBalance(pu2)
    bal3 = getBalance(pu3)

    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu2, 0.1, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)
    sendCoins(pu1, 0.1, pr1, pu3, 0.03, miners)

    time.sleep(60)

    #Save/Load all blocks
    TxBlock.saveBlocks(head_blocks, "AllBlocks.dat")
    head_blocks = TxBlock.loadBlocks("AllBlocks.dat")

    #Query balances
    new1 = getBalance(pu1)
    print(new1)
    new2 = getBalance(pu2)
    new3 = getBalance(pu3)

    #Verify balances
    if abs(new1-bal1+2.0) > 0.00000001:
        print("Error! Wrong balance for pu1")
    else:
        print("Success. Good balance for pu1")
    if abs(new2-bal2-1.0) > 0.00000001:
        print("Error! Wrong balance for pu2")
    else:
        print("Success. Good balance for pu2")
    if abs(new3-bal3-0.3) > 0.00000001:
        print("Error! Wrong balance for pu3")
    else:
        print("Success. Good balance for pu3")

    Miner.StopAll()
    
    num_heads = len(head_blocks)
    sister = TxBlock.TxBlock(head_blocks[0].previousBlock.previousBlock)
    sister.previousBlock = None
    SocketUtils.sendObj('localhost',sister,5006)
    time.sleep(10)
    if (len(head_blocks) == num_heads + 1):
        print ("Success! New head_block created")
    else:
        print("Error! Failed to add sister block")
        
    
    StopAll()
    
    t1.join()
    t2.join()
    t3.join()

    print ("Exit successful.")
                
    



