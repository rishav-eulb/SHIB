#AnotherMiner
import Signatures
import Miner
import threading
import time
import TxBlock
my_ip='localhost'
wallets=[(my_ip,5006),(my_ip,5005)]
Miner.verbose = True
my_pr,my_pu = Signatures.generate_keys()
tMS = threading.Thread(target=Miner.minerServer, args=((my_ip,5007),))
tNF = threading.Thread(target=Miner.nonceFinder, args=(wallets, my_pu))
tMS.start()
time.sleep(4)
tNF.start()


time.sleep(20)
Miner.StopAll()
tMS.join()
tNF.join()
print(TxBlock.findLongestBlockchain(Miner.head_blocks)
                      .previousBlock.previousBlock.previousBlock.previousBlock.nonce)
print(TxBlock.findLongestBlockchain(Miner.head_blocks)
                      .previousBlock.previousBlock.previousBlock.nonce)
print(TxBlock.findLongestBlockchain(Miner.head_blocks)
                      .previousBlock.previousBlock.nonce)
print(TxBlock.findLongestBlockchain(Miner.head_blocks).previousBlock.nonce)

print(TxBlock.findLongestBlockchain(Miner.head_blocks).nonce)

