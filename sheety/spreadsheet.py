import requests

class Sheet():
    def __init__(self, key:str, url:str) -> None:
        self.header = {"Authorization":key,
                       "Content-Type":"application/json"}
        self.url = url
        self.query = {"get":requests.get, 
                      "post":requests.post, 
                      "put": requests.put, 
                      "delete":requests.delete}
        
    def retrieve(self, endpoint:str, filter_m="", ID=""):    
        data = self.query["get"](url=f"{self.url}/{endpoint}/{str(ID)}", params=filter_m, headers=self.header)
        return data
        
    def del_row(self, endpoint:str, ID):    
        data = self.query["delete"](url=f"{self.url}/{endpoint}/{str(ID)}", headers=self.header)
        return data
                
    def add_row(self, endpoint:str, **kw):
        message = {
            endpoint :
                {}
        }
        
        for k, v in kw.items():
            message[endpoint][k] = v
        
        data = self.query["post"](url=f"{self.url}/{endpoint}", json=message, headers=self.header)
        return data
            
    def edit_row(self, endpoint:str, doc_name, ID, **kw):    
        message = {
            doc_name :
                {}
        }
        
        for k, v in kw.items():
            message[doc_name][str(k)] = str(v)

        data = self.query["put"](url=f"{self.url}/{endpoint}/{str(ID)}", json=message, headers=self.header)
        return data


# import decouple
# ar = Sheet(decouple.config("SHEETY_TOKEN"), "https://api.sheety.co/a60d5392a0f366cfd5dfee198f97ab4d/qlauseRekber")
# contract_ = ar.retrieve("contract").json()
# contract_value = ar.retrieve("userRegistered").json()
# print(contract_value)
# user_registered = ar.retrieve("userRegistered").json()
# print(user_registered)
# ar.add_row('contract', user_id="ardial", contract="023123qweasd")
# ar.add_row('contractValue', contract="023123qweasd", address_1="rdx123123", address_2="rdx908098", value_1="10000", value_2="3000")
# ar.add_row('contractValue', contract="023123qweasd", address_1="rdx123123", value_1="10000")
# print(ar.add_row('userRegistered', userId="023123234", balance="100").text)