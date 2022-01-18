# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 14:42:25 2021

@author: simosc
"""

from typing import Dict, Optional
import requests
import json
import hmac
import hashlib
import time
import datetime


class Wallet :
    
    API_URL = "https://openapi.debank.{}/" 

    def __init__(
        self, wallet_id: Optional[str] = None, tld: str = 'com', 
        ):
        
        self.tld = tld
        self.API_URL = self.API_URL.format(tld)
        self.WALLET_ID = wallet_id

# USER ENDPOINTS 
        
    def get_total_balance(self):
        """
    
        Parameters
        ----------
        
    
        Returns
        -------
        dict : 
            Total balance, balance split by chain. 
    
        """    
        
        # Request param
        req = {
          "id": self.WALLET_ID
        };        
        
        response = requests.get("https://openapi.debank.com/v1/user/total_balance" + "?" + list(req.items())[0][0] + "=" + req["id"],
                                 headers={"Content-Type":"application/json"})
        response = json.loads(response.text) 
        return response
    
    def get_chain_balance(self, chain):
        """
    
        Parameters
        ----------
        chain : str
            Available values : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt
    
        Returns
        -------
        dict : 
            usd_value for requested chain 
    
        """    
        
        # Request param
        req = {
          "id" : self.WALLET_ID,
          "chain_id" : chain
        };        
        
        response = requests.get("https://openapi.debank.com/v1/user/chain_balance" + "?" + list(req.items())[0][0] + "=" + req["id"] + \
                                "&" + list(req.items())[1][0] + "=" + req["chain_id"],
                                 headers={"Content-Type":"application/json"})
        response = json.loads(response.text)
        return response





















