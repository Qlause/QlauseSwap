import ecdsa
from ecdsa.util import sigencode_der
import requests
from wallet import Wallet

class Transaction:
    def __init__(self, wallet:Wallet):
        self.endpoint = "https://mainnet.radixdlt.com/"
        self.header = {'X-Radixdlt-Target-Gw-Api' : '1.0',
                       'Content-Type': 'application/json'}
        self.derivation_path = wallet.get_wallet_info()["Derivation Path"]
        self.private_key = wallet.get_wallet_info()["Private Key"]
        self.public_key = wallet.get_wallet_info()["Public Key"]
        self.wallet_address = wallet.get_wallet_info()["Wallet Address"]
        self.symmetrical_key = wallet.get_wallet_info()["Symmetrical Key"]
        self.entropy = wallet.get_wallet_info()["Entropy"]
        self.words = wallet.get_wallet_info()["Words"]
        self.seed = wallet.get_wallet_info()["Seed"]
        

    def get_info_token(self, rri:str):
        endpoint = self.endpoint + "token"
        body = {
            "network_identifier": {
                "network": "mainnet"
                    },
            "token_identifier": {
                "rri": rri
                    }
        }
        
        res = requests.post(endpoint, json=body, headers=self.header)
        return res.json()
    
    def build_tx_send_token(self, to : str, rri:str, value:str):
        endpoint = self.endpoint + "transaction/build"
        body = {
                "network_identifier": {
                    "network": "mainnet"
                    },
                "actions": [
                    {"type": "TransferTokens",
                        "from_account": {"address": self.wallet_address},
                        "to_account": {"address": to},
                        "amount": {"token_identifier": {
                                        "rri": rri},
                                    "value": value}
                    }
                ],
                "fee_payer": {
                    "address": self.wallet_address
                },
                    "disable_token_mint_and_burn": "true"
            }
        
        res = requests.post(endpoint, json=body, headers=self.header)
        return res.json()
    
    def sign_tx_send_token(self, payload_to_sign:str):
        sk = ecdsa.SigningKey.from_string(bytearray.fromhex(str(self.private_key)), curve=ecdsa.SECP256k1)
        signed = sk.sign_digest(bytes.fromhex(payload_to_sign), sigencode=sigencode_der).hex()
        return signed

    def finalize_tx_send_token(self, unsigned_tx:str, signed_tx:str):
        endpoint = self.endpoint + "transaction/finalize"
        body = {
                  "network_identifier": {
                    "network": "mainnet"},
                  "unsigned_transaction": unsigned_tx,
                  "signature": {
                    "public_key": {
                      "hex": self.public_key},
                    "bytes": signed_tx},
                  "submit": "true"
                }
        
        res = requests.post(endpoint, json=body, headers=self.header)
        return res.json()
    
    def status(self, hash_:str):
        endpoint = self.endpoint + "transaction/status"
        body = {
                    "network_identifier": {
                        "network": "mainnet"
                    },
                    "transaction_identifier": {
                        "hash": hash_
                    }
                }
        res = requests.post(endpoint, json=body, headers=self.header)

        return res.json()
    
    def send_token(self, to:str, rri:str, value:str):
        build_tx = self.build_tx_send_token(to, rri, value)
        unsigned_tx = build_tx['transaction_build']['unsigned_transaction']
        payload_to_sign = build_tx['transaction_build']['payload_to_sign']
        
        signed_tx = self.sign_tx_send_token(payload_to_sign)      
        finalized_tx = self.finalize_tx_send_token(unsigned_tx, signed_tx)
        
        return self.status(finalized_tx['transaction_identifier']['hash'])
        
# import decouple

# WALLET_PASSWORD = decouple.config("WALLET_PASSWORD")
# WALLET_NONCE = decouple.config("WALLET_NONCE")
# WALLET_CIPHERTEXT = decouple.config("WALLET_CIPHERTEXT")
# WALLET_SALT = decouple.config("WALLET_SALT")
# WALLET_MAC = decouple.config("WALLET_MAC")

# wallet = Wallet(password=WALLET_PASSWORD, salt=WALLET_SALT, nonce=WALLET_NONCE, ciphertext=WALLET_CIPHERTEXT, mac=WALLET_MAC)

# tx = Transaction(wallet)
# res = tx.send_token("rdx1qsp222hghu4s3hpscenxvrwjz62tqkz30sa0kvqy5x6v8ncj55dr68ch8ph2n", "inu_rr1qw9zhy7tzs85jhsm0y3jrlggfkjku673h4aze6836g8qslavfy", "1000000000000000000")
# res = tx.status("e145049d81403d6d5cb28f8eb0b57ede53afebd9e4f7bf326b62cbd2b73e5ede")
# print(res)