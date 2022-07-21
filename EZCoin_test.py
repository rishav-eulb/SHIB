#EZCoin
import time
import Wallet

wallets=[]
miners=[]
my_ip = 'localhost'

def startMiner():
    #Start nonceFinder
    #Start minerServer
    #Load tx_list
    #Load head_blocks
    #Load public_key
    return True
def startWallet():
    #Start walletServer
    #Load public and private keys
    #Load head_blocsk
    return True

def stopMiner():
    #Stop nonceFinder
    #Stop minerServer
    #Save tx_list
    #Save head_blocks
    return True
def stopWallet():
    #Stop walletServer
    #Save head_blocks
    return True

def getBalance(pu_key):
    return 0.0

def sendCoins(pu_recv, amt, tx_fee):
    return True

def makeNewKeys():
    return None, None






if __name__ == "__main__":
    startMiner()
    startWallet()
    other_public = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtgVDX501+HzGJxusVfOJ\n8V7VXUlCs1sDgIXxq2uc38fC3fO8GmYMVVeMZ34KAZ3HMBKwMKVbN1tIPVNBz22m\n54tP+3RS8xN2lDNByiSKIFsmtDMO7JpP/hl13Lj+IiVs3bI0n1uShlOIJ8QozEud\nlwkMz39xfrvX0NN6MYl/OibIkPW6cle8hwKWE6kxiUz4nLDB4i9YuRcjWsSSW/a/\n9oU4TZWk128O4BWnqru8XNyz2km4vsq5k07WCVSCqlpyF26v85sWqDTGCHXIeZre\nEKuKiZpgAVCjgHAbYkin1BGWRVXohPnEZECrZqoTjVVEl5wAdGXntjrsWIXaumG5\nhQIDAQAB\n-----END PUBLIC KEY-----\n'
    time.sleep(2)
    print(getBalance(Wallet.my_public))
    sendCoins( other_public, 1.0, 0.1 )
    print(getBalance(other_public))
    print(getBalance(Wallet.my_public))

    time.sleep(1)
    stopWallet()
    stopMiner()
    
    
