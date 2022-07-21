#MinerExec
import Signatures
import Miner
import time

miner_pu = Signatures.loadPublic("miner_public.key")
wallets = [('10.0.0.68',5006)]


t1 = threading.Thread(target=Miner.minerServer, args=(('10.0.0.68',5005),))
t2 = threading.Thread(target=Miner.nonceFinder, args=(wallets, miner_pu))

t1.start()
t2.start()

time.sleep(600)
Miner.StopAll()

t1.join()
t2.join()


