#!/usr/bin/env python
# coding=iso-8859-1

# ProfitLib.py: mining profitability library
#
# Copyright © 2014 Scott Alfter
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import bitcoinrpc
import jsonrpc
import sys
from decimal import *
sys.path.insert(0, './PyCryptsy/')
from PyCryptsy import PyCryptsy

class ProfitLib:

  def __init__(self, config):
    self.config=config
    self.out={}
    self.api=PyCryptsy(str(self.config["cryptsy_pubkey"]), str(self.config["cryptsy_privkey"]))

  def Calculate(self):
    self.mkts=self.api.GetMarketIDs("BTC")
    for i, coin in enumerate(self.config):
      if (coin!="cryptsy_pubkey" and coin!="cryptsy_privkey"):
        if (self.config[coin]["active"]==1):
          url="http://"+self.config[coin]["username"]+":"+self.config[coin]["passwd"]+"@"+self.config[coin]["host"]+":"+str(self.config[coin]["port"])
          hashrate=Decimal(self.config[coin]["hashespersec"])
          self.out[coin]={}
        
          b=jsonrpc.ServiceProxy(url)
    
          reward=Decimal(b.getblocktemplate({})["coinbasevalue"])
          if (coin=="NVC"):
            reward*=100
    
          diff=b.getdifficulty()
          if (type(diff) is dict):
            diff=diff["proof-of-work"]
    
          try:
            nethashrate=b.getmininginfo()["networkhashps"]
          except:
            nethashrate=int(b.getmininginfo()["netmhashps"]*1000000)
    
          self.out[coin]["reward"]=int(reward)
          self.out[coin]["difficulty"]=float(diff.quantize(Decimal("1.00000000")))
          self.out[coin]["nethashespersec"]=int(nethashrate)

          interval=Decimal(86400) # 1 day
          target=Decimal(((65535<<208)*100000000000)/(diff*100000000000))
          revenue=Decimal(interval*target*hashrate*reward/(1<<256))

          self.out[coin]["daily_revenue"]=int(revenue)
 
          if (coin!="BTC"):
            exch=self.api.GetBuyPriceByID(self.mkts[coin])
            self.out[coin]["exchrate"]=int(exch)
            self.out[coin]["daily_revenue_btc"]=int(Decimal(revenue*Decimal(exch)))
          else:
            self.out[coin]["exchrate"]=100000000
            self.out[coin]["daily_revenue_btc"]=int(revenue)

          self.out[coin]["algo"]=self.config[coin]["algo"]
          self.out[coin]["merged"]=self.config[coin]["merged"]
          
    return self.out

