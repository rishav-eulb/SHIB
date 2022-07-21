#EZCoin
import time
import Wallet
import Miner
import threading
import Signatures

wallets=[]
miners=[]
my_ip = 'localhost'
wallets.append((my_ip,5006))
miners.append((my_ip,5005))

tMS = None
tNF = None
tWS = None

def startMiner():
    global tMS,tNF
    try:
        my_pu = Signatures.loadPublic("public.key")
    except:
        print("No public.key Need to generate?")
        pass #TODO
    tMS = threading.Thread(target=Miner.minerServer, args=((my_ip,5005),))
    tNF = threading.Thread(target=Miner.nonceFinder, args=(wallets, my_pu))
    tMS.start()
    tNF.start()
    return True
def startWallet():
    global tWS
    Wallet.my_private, Wallet.my_public = Signatures.loadKeys(
                                                 "private.key","public.key")
    
    tWS = threading.Thread(target=Wallet.walletServer, args=((my_ip,5006),))
    tWS.start()
    return True

def stopMiner():
    global tMS, tNF
    Miner.StopAll()
    if tMS: tMS.join()
    if tNF: tNF.join()
    tMS = None
    tNF = None
    return True
def stopWallet():
    global tWS
    Wallet.StopAll()
    if tWS: tWS.join()
    tWS = None
    return True

def getBalance(pu_key):
    if not tWS:
        print("Start the server by calling startWallet before checking balances")
        return 0.0
    return Wallet.getBalance(pu_key)
 
def sendCoins(pu_recv, amt, tx_fee):
    Wallet.sendCoins(Wallet.my_public, amt+tx_fee, Wallet.my_private, pu_recv,
                     amt, miners)
    return True

def makeNewKeys():
    return Signatures.generate_keys()






if __name__ == "__main__":
    startMiner()
    startWallet()
    other_public = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtgVDX501+HzGJxusVfOJ\n8V7VXUlCs1sDgIXxq2uc38fC3fO8GmYMVVeMZ34KAZ3HMBKwMKVbN1tIPVNBz22m\n54tP+3RS8xN2lDNByiSKIFsmtDMO7JpP/hl13Lj+IiVs3bI0n1uShlOIJ8QozEud\nlwkMz39xfrvX0NN6MYl/OibIkPW6cle8hwKWE6kxiUz4nLDB4i9YuRcjWsSSW/a/\n9oU4TZWk128O4BWnqru8XNyz2km4vsq5k07WCVSCqlpyF26v85sWqDTGCHXIeZre\nEKuKiZpgAVCjgHAbYkin1BGWRVXohPnEZECrZqoTjVVEl5wAdGXntjrsWIXaumG5\nhQIDAQAB\n-----END PUBLIC KEY-----\n'
    time.sleep(2)
    print("Balance: " +str(getBalance(Wallet.my_public)))
    sendCoins( other_public, 1.0, 0.1 )
    time.sleep(20)
    print(getBalance(other_public))
    print(getBalance(Wallet.my_public))

    time.sleep(1)
    stopWallet()
    stopMiner()
    
    
