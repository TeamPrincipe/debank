# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 16:00:38 2021

@author: simosc
"""

from debank.wallet import Wallet

# EXAMPLE  
address = "your_wallet_address"  
wallet = Wallet()

# user/total_balance
total_bal = wallet.get_total_balance(address)

# user/chain_balance
eth_chain_bal = wallet.get_chain_balance("eth")["usd_value"]
cro_chain_bal = wallet.get_chain_balance("cro")["usd_value"]
avax_chain_bal = wallet.get_chain_balance("avax")["usd_value"]

ftm_token_balance = wallet.get_user_token_list(address, 'ftm')