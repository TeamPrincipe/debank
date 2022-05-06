# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 14:42:25 2021

@author: simosc
"""
import os
from typing import Dict, Optional
import requests
import json
import hmac
import hashlib
import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC


class Wallet :
    
    API_URL = "https://openapi.debank.com" 
    URL = 'https://debank.com'
    # api version
    V1 = '/v1'
    
    # path
    CHAIN = '/chain'
    CHAIN_BALANCE = '/chain_balance'
    COMPLEX_PROTOCOL_LIST = '/complex_protocol_list'
    HISTORY = '/history'
    LIST = '/list'
    LIST_BY_IDS = '/list_by_ids'
    PROFILE = '/profile'
    PROTOCOL = '/protocol'
    SIMPLE_PROTOCOL_LIST = '/simple_protocol_list'
    TOKEN = '/token'
    TOKEN_LIST = '/token_list'
    TOKEN_SEARCH = '/token_search'
    TOTAL_BALANCE = '/total_balance'
    USER = '/user'
    
    # request api
    ID = '?id='
    CHAIN_ID = '?chain_id='
    
    # other requirements
    ADDRESS = '&id='
    AND_CHAIN = '&chain_id='
    HAS_BALANCE = '&has_balance='
    IDS = '&ids='
    IS_ALL = '&is_all='
    PROTOCOL_ID = '&protocol_id='
    Q = '&q='
    TOKEN_ID = '&token_id='
    
    # optional GET condition
    OPTION_REQ = 'application/json'
    
    
    def __init__(self
                 , wallet_id: Optional[str] = None, 
                 ):
        
        self.API_URL = "https://openapi.debank.com" 
        self.WALLET_ID = wallet_id
        
        # End Points Chain
        self.chain_information = self.API_URL + self.V1 + self.CHAIN + self.ID + '{}'
        self.supported_chain_list = self.API_URL + self.V1 + self.CHAIN + self.LIST
        
        # End Points Protocol
        self.protocol_information = self.API_URL + self.V1 + self.PROTOCOL + self.ID + '{}'
        self.list_of_protocol_information = self.API_URL + self.V1 + self.PROTOCOL + self.LIST
        
        # End Points Token
        self.token_information = self.API_URL + self.V1 + self.TOKEN + self.CHAIN_ID + '{}' + self.ADDRESS + '{}'     
        self.list_token_information = self.API_URL + self.V1 + self.TOKEN + self.LIST_BY_IDS + self.CHAIN_ID + '{}' + self.IDS + '{}'
        
        # End Points User
        self.user_chain_balance = self.API_URL + self.V1 + self.USER + self.CHAIN_BALANCE + self.ID + '{}' + self.CHAIN_ID + '{}'
        self.user_protocol = self.API_URL + self.V1 + self.USER + self.PROTOCOL + self.ID + '{}' + self.PROTOCOL_ID + '{}'
        self.user_complex_protocol_list = self.API_URL + self.V1 + self.USER + self.COMPLEX_PROTOCOL_LIST + self.ID + '{}' + self.AND_CHAIN + '{}'
        self.user_simple_protocol_list = self.API_URL + self.V1 + self.USER + self.SIMPLE_PROTOCOL_LIST + self.ID + '{}' + self.AND_CHAIN + '{}'
        self.user_token_balance = self.API_URL + self.V1 + self.USER + self.TOKEN + self.ID + '{}' + self.AND_CHAIN + '{}' + self.TOKEN_ID + '{}'
        self.user_token_list =  self.API_URL + self.V1 + self.USER + self.TOKEN_LIST +  self.ID + '{}' + self.AND_CHAIN + '{}' + self.IS_ALL + '{}' + self.HAS_BALANCE + '{}'
        self.search_user_token = self.API_URL + self.V1 + self.USER + self.TOKEN_SEARCH + self.CHAIN_ID + '{}' + self.ADDRESS + '{}' + self.Q + '{}' + self.HAS_BALANCE + '{}'
        self.user_total_balance = self.API_URL + self.V1 + self.USER + self.TOTAL_BALANCE + self.ID + '{}'
        
        # End Points without API
        self.user_history = self.URL + self.PROFILE + '/' + '{}' + self.HISTORY




    def get_chain_information(self, chain):  
        """
        
        https://openapi.debank.com/docs
        
        Parameters
        ----------
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.

        Returns
        -------
        {
          "id": "eth",
          "community_id": 1,
          "name": "Ethereum",
          "logo_url": "https://static.debank.com/image/chain/logo_url/eth/6e0cd1f895af9836ee8c32cfc03bc279.png",
          "native_token_id": "eth",
          "wrapped_token_id": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
        }.

        """
        
        url = self.chain_information.format(chain)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))



    def get_supported_chain_list(self):  
        """
        
        https://openapi.debank.com/docs
        
        Returns
        -------
        {
            "id": "eth",
            "community_id": 1,
            "name": "Ethereum",
            "logo_url": "https://static.debank.com/image/chain/logo_url/eth/6e0cd1f895af9836ee8c32cfc03bc279.png",
            "native_token_id": "eth",
            "wrapped_token_id": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
          }

        """

        
        url = self.supported_chain_list
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))


    def get_protocol_information(self, protocol):  
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        protocol : bsc_pancakeswap, curve, uniswap, ecc.
            DESCRIPTION.

        Returns
        -------
        {
          "id": "compound",
          "chain_id": 1,
          "name": "Compound",
          "logo_url": "https://static.debank.com/image/project/logo_url/compound/b4b9c8de20952846a1c9dfcded47d0db.png",
          "site_url": "https://app.compound.finance",
          "has_supported_portfolio": true
        }

        """

        
        url = self.protocol_information.format(protocol)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))


    def get_list_of_protocol_information(self):  
        """
        https://openapi.debank.com/docs

        Parameters
        ----------


        Returns
        -------
         [
          {
            "id": "compound",
            "chain_id": 1,
            "name": "Compound",
            "logo_url": "https://static.debank.com/image/project/logo_url/compound/b4b9c8de20952846a1c9dfcded47d0db.png",
            "site_url": "https://app.compound.finance",
            "has_supported_portfolio": true
          }
        ]
        """

        
        url = self.list_of_protocol_information
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))


    def get_token_information(self, chain, address): 
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.
        address : string
            DESCRIPTION.

        Returns
        -------
        {
          "id": "0xdac17f958d2ee523a2206206994597c13d831ec7",
          "chain": 1,
          "name": "Tether USD",
          "symbol": "USDT",
          "decimals": 6,
          "logo_url": "https://static.debank.com/image/token/logo_url/0xdac17f958d2ee523a2206206994597c13d831ec7/3c1a718331e468abe1fc2ebe319f6c77.png",
          "is_verified": true,
          "price": 1.01,
          "is_wallet": true
        }

        """

        
        url = self.token_information.format(chain, address)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))
    

    def get_list_token_information(self, chain, address):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.
        address : list of addresses
            DESCRIPTION.

        Returns
        -------
        [
          {
            "id": "0xdac17f958d2ee523a2206206994597c13d831ec7",
            "chain": 1,
            "name": "Tether USD",
            "symbol": "USDT",
            "decimals": 6,
            "logo_url": "https://static.debank.com/image/token/logo_url/0xdac17f958d2ee523a2206206994597c13d831ec7/3c1a718331e468abe1fc2ebe319f6c77.png",
            "is_verified": true,
            "price": 1.01,
            "is_wallet": true
          }
        ]

        """

        
        url = self.list_token_information.format(chain, ','.join(address))
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))
        


    def get_chain_balance(self, address, chain):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        address : address
            DESCRIPTION.
            
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.


        Returns
        -------
        return to the usd value of net assets

        """

        
        url = self.user_chain_balance.format(address, chain)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))
        
    def get_user_protocol(self, address, protocol):
        """
        

        Parameters
        ----------
        address : address
            DESCRIPTION.
        protocol : bsc_pancakeswap, curve, uniswap, ecc.
            DESCRIPTION.

        Returns
        -------
        {
          "id": "compound",
          "chain": "eth",
          "name": "Compound",
          "site_url": "https://app.compound.finance",
          "logo_url": "https://static.debank.com/image/project/logo_url/compound/0b792243f1f68e9ed082f5a49ee6f21d.png",
          "has_supported_portfolio": true,
          "tvl": 12763095483.420198
        }

        """
        
        url = self.user_protocol.format(address, protocol)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'").replace('false',"'false'"))        


    def get_user_complex_protocol_list(self, address, chain):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        address : address
            DESCRIPTION.
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.

        Returns
        -------
        return the list of protocol with user’s portfolio items

        """
        
        url = self.user_complex_protocol_list.format(address, chain)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))        


    def get_user_simple_protocol_list(self, address, chain):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        address : address
            DESCRIPTION.
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.

        Returns
        -------
        	
        return list of protocols with user assets

        """
        
        url = self.user_simple_protocol_list.format(address, chain)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))        


    def get_user_token_balance(self, address, chain, token_address):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        address : address
            DESCRIPTION.
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.
        token_address : token_address
            DESCRIPTION.            

        Returns
        -------
        	
        return list of protocols with user assets

        """
        
        url = self.user_token_balance.format(address, chain, token_address)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))   



    def get_user_token_list(self, address, chain, is_all = 'true', has_balance = 'true'):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        address : address
            DESCRIPTION.
        chain : all_chain, eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.
        is_all: Boolean, true or false. If true, all tokens are returned, including protocol-derived tokens
        Returns
        -------
        	
        return list of protocols with user assets

        """
        if chain == 'all_chain':
            user_token_list =  self.API_URL + self.V1 + self.USER + self.TOKEN_LIST +  self.ID + '{}' + self.IS_ALL + '{}' + self.HAS_BALANCE + '{}'
            url = user_token_list.format(address, is_all, has_balance)
            res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
            res = res.text.replace('null', "'null'").replace('true',"'true'").replace('false',"'false'").replace('\n','')
              
        else:
            url = self.user_token_list.format(address, chain, is_all, has_balance)
            res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
            res = res.text.replace('null', "'null'").replace('true',"'true'").replace('false',"'false'").replace('\n','')
            
            
        return   eval(res)
    
    def get_user_history(self, address):
        """
        class_history_table = 'History_table__9zhFG'
        class_table_line = 'History_tableLine__3dtlF'
        class_button = 'History_loadMore__1DkZs'
        url = self.user_history.format(address)
        istance = webdriver.Firefox()
        istance.get(url)
        wait(istance, 6000).until(EC.presence_of_element_located((By.CLASS_NAME, class_history_table))).text # Wait until table is loaded
        while True:
            istance.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            try:
                istance.find_element_by_class_name(class_button).click()
                wait(istance, 6000).until(EC.presence_of_element_located((By.CLASS_NAME, class_history_table))).text
            except:
                wait(istance, 6000).until(EC.presence_of_element_located((By.CLASS_NAME, class_history_table))).text
                break
            
        page_source = istance.page_source
        html = BeautifulSoup(page_source,"html.parser")  
        table = html.find('div',{'class' : class_history_table})
        divs = table.find_all('div',{'class' : class_table_line})
        """
        pass


    def get_search_user_token(self, chain, address, q, has_balance = 'true'):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        address : address
            DESCRIPTION.
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.
        q: string. filter args
        has_balance: Boolean, true or false. If true, only token with balance will returned.
        
        Returns
        -------
        	
        return list of protocols with user assets

        """
        
        url = self.search_user_token.format(chain, address, q, has_balance)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))       
    
    

    def get_total_balance(self, address):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        address : address
            DESCRIPTION.
        
        Returns
        -------
        	
        return the total net assets and the net assets of each chain

        """
        
        url = self.user_total_balance.format(address)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))    

        





