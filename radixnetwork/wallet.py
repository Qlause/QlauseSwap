from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from mnemonic import Mnemonic
from hdwallet import HDWallet
import bech32
import decouple

class Wallet:
    def __init__(self, password : str, 
                 salt : str, 
                 nonce : str, 
                 ciphertext : str, 
                 mac : str,
                 lengthOfDerivedKey = 32,
                 blockSize = 8,
                 parallelizationParameter = 1,
                 costParameterN = 8192) -> None:
        
        self.wallet_pw = password
        self.wallet_salt = salt
        self.wallet_nonce = nonce
        self.wallet_ciphertext = ciphertext 
        self.wallet_mac = mac
        self.lengthOfDerivedKey = lengthOfDerivedKey
        self.blockSize = blockSize
        self.parallelizationParameter = parallelizationParameter
        self.costParameterN = costParameterN


    def get_wallet_info(self):
        symmetrical_key = scrypt( \
                            self.wallet_pw, \
                            bytearray.fromhex(self.wallet_salt), \
                            key_len=self.lengthOfDerivedKey, \
                            N=self.costParameterN, \
                            r=self.blockSize, \
                            p=self.parallelizationParameter \
                         )

        cipher = AES.new(symmetrical_key, AES.MODE_GCM, nonce=bytearray.fromhex(self.wallet_nonce))
        entropy = cipher.decrypt_and_verify(bytearray.fromhex(self.wallet_ciphertext), bytearray.fromhex(self.wallet_mac))

        mnemo = Mnemonic("english")
        words = mnemo.to_mnemonic(entropy)
        password = ""
        seed = Mnemonic.to_seed(words, passphrase=password)

        purpose = 44
        coinType = 1022
        account = 0
        change = 0

        addressIndex = 0
        hdwallet = HDWallet()
        hdwallet.from_seed(seed=seed.hex())
        hdwallet.from_index(purpose, hardened=True)
        hdwallet.from_index(coinType, hardened=True)
        hdwallet.from_index(account, hardened=True)
        hdwallet.from_index(change)
        hdwallet.from_index(addressIndex, hardened=True)
       
        readdr = b"\x04" + bytearray.fromhex(hdwallet.public_key())
        readdr_bytes5 = bech32.convertbits(readdr, 8, 5)
        wallet_addr = bech32.bech32_encode("rdx", readdr_bytes5)

        return {"Derivation Path": hdwallet.path(),
                "Private Key": hdwallet.private_key(),
                "Public Key": hdwallet.public_key(),
                "Wallet Address": wallet_addr,
                "Symmetrical Key" : symmetrical_key.hex(),
                "Entropy": entropy.hex(),
                "Words": words, 
                "Seed": seed.hex()}
