#TestAll
import Miner
import Wallet
import time

Wallet.WalletStart()
Miner.MinerStart()

time.sleep(60)
Wallet.sendCoins(Wallet.my_public, 1.0, Wallet.my_private,
                 Wallet.my_public, 0.98,
                 [('10.0.0.68',5005)])


Miner.MinerStop()
Wallet.WalletStop()

print("Successfully exited!")
