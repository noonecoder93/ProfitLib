#!/usr/bin/env python
# coding=iso-8859-1

# ProfitLib.py: mining profitability library
#
# Copyright © 2014-2015 Scott Alfter
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
from PyCryptsy import PyCryptsy
from bittrex import bittrex as Bittrex
from PyCCEX import PyCCEX
from PyCryptopia import PyCryptopia
from poloniex import poloniex
from bleuBot import bleuBot

class ProfitLib:

  # store config dictionary, init output dictionary, and initialize PyCryptsy

  def __init__(self, daemons, credentials):
    self.daemons=daemons
    self.out={}
    self.api={}
    for i, exch in enumerate(credentials):
      if (exch=="cryptsy"):
        self.api[exch]=PyCryptsy(str(credentials[exch]["pubkey"]), str(credentials[exch]["privkey"]))
      elif (exch=="bittrex"):
        self.api[exch]=Bittrex.Bittrex(str(credentials[exch]["pubkey"]), str(credentials[exch]["privkey"]))
      elif (exch=="c-cex"):
        self.api[exch]=PyCCEX(str(credentials[exch]["key"]))
      elif (exch=="cryptopia"):
        self.api[exch]=PyCryptopia()
      elif (exch=="poloniex"):
        self.api[exch]=poloniex(str(credentials[exch]["key"]), str(credentials[exch]["secret"]))
      elif (exch=="bleutrade"):
        self.api[exch]=bleuBot(str(credentials[exch]["key"]), str(credentials[exch]["secret"]))
      else:
        raise ValueError("unknown exchange") 

  # update market IDs
  def GetMarketIDs(self):
    self.mkts={}
    for i, exch in enumerate(self.api):
      if (exch=="cryptsy"):
        try:
          self.mkts[exch]={}
          coins=self.api[exch].Query("getcoindata", {})["return"]
          markets=self.api[exch].GetMarketIDs("BTC")
          for j in coins:
            if (j["code"].upper() in markets.keys() and j["maintenancemode"]=="0"):
                self.mkts[exch][j["code"].upper()]=markets[j["code"].upper()]
        except:
          print "warning: Cryptsy offline"
      elif (exch=="cryptopia"):
        try:
          self.mkts[exch]=self.api[exch].GetMarketIDs("BTC")
        except:
          print "warning: Cryptopia offline"
      elif (exch=="bittrex"):
        try:
          self.mkts[exch]={}
          m=self.api[exch].get_markets()["result"]
          for j, market in enumerate(m):
            if (market["BaseCurrency"].upper()=="BTC" and market["IsActive"]):
              self.mkts[exch][market["MarketCurrency"].upper()]=market["MarketName"]
        except:
          print "warning: Bittrex offline"
      elif (exch=="c-cex"):
        try:
          self.mkts[exch]={}
          m=self.api[exch].Query("pairs", {})["pairs"]
          for j, pair in enumerate(m):
            if (pair.split("-")[1].upper()=="BTC"):
              self.mkts[exch][pair.split("-")[0].upper()]=pair
        except:
          print "warning: C-CEX offline"
      elif (exch=="poloniex"):
        try:
          self.mkts[exch]={}
          m=self.api[exch].returnTicker()
          for j, pair in enumerate(m):
            if (pair.split("_")[0].upper()=="BTC" and m[pair]["isFrozen"]=="0"):
              self.mkts[exch][pair.split("_")[1].upper()]=pair
        except:
          print "warning: Poloniex offline"
      elif (exch=="bleutrade"):
        try:
          self.mkts[exch]={}
          m=self.api[exch].getMarketSummaries()["result"]
          for j, pair in enumerate(m):
            if (pair["MarketName"].split("_")[1].upper()=="BTC" and pair["IsActive"]=="true"):
              self.mkts[exch][pair["MarketName"].split("_")[0].upper()]=pair["MarketName"]
        except:
          print "warning: Bleutrade offline"
          
  # get best bid from the exchanges
  def GetBestBid(self, coin):
    bids={}
    for i, exch in enumerate(self.api):
      if (exch=="cryptsy" or exch=="cryptopia"):
        try:
          bids[exch]=Decimal(self.api[exch].GetBuyPriceByID(self.mkts[exch][coin]))
        except:
          pass
      elif (exch=="bittrex"):
        try:
          bids[exch]=Decimal(self.api[exch].get_ticker(self.mkts[exch][coin])["result"]["Bid"])
        except:
          pass
      elif (exch=="c-cex"):
        try:
          bids[exch]=Decimal(self.api[exch].Query(self.mkts[exch][coin], {})["ticker"]["buy"])
        except:
          pass
      elif (exch=="poloniex"):
        try:
          bids[exch]=Decimal(self.api[exch].returnOrderBook(self.mkts[exch][coin], 1)["bids"][0][0])
        except:
          pass
      elif (exch=="bleutrade"):
        try:
          bids[exch]=Decimal(self.api[exch].getTicker(self.mkts[exch][coin])["result"][0]["bid"])
        except:
          pass
    max_bid=(0, "none")
    for i, exch in enumerate(bids):
      if (Decimal(bids[exch])>Decimal(max_bid[0])):
        max_bid=(bids[exch], exch)
    return max_bid
    
  # get latest profitability info

  def Calculate(self):
    self.GetMarketIDs()
    for i, coin in enumerate(self.daemons):
      if (self.daemons[coin]["active"]==1): # only check active configs
        url="http://"+self.daemons[coin]["username"]+":"+self.daemons[coin]["passwd"]+"@"+self.daemons[coin]["host"]+":"+str(self.daemons[coin]["port"])
        hashrate=Decimal(self.daemons[coin]["hashespersec"]) # our hashrate
        self.out[coin]={}
      
        # connect to coind

        b=jsonrpc.ServiceProxy(url)
    
        # get block reward, including transaction fees
        # note #1: Novacoin (and coins derived from it?) report
        #          1% of actual value here
        # note #2: Namecoin doesn't support getblocktemplate, so get 
        #          coinbase value from last block
        # note #3: PPCoin doesn't want any parameters passed to
        #          getblocktemplate.  Bitcoin requires at least 
        #          an empty dictionary to be passed.  Others don't
        #          care.

        reward=Decimal(0)
        try:
          reward=Decimal(b.getblocktemplate()["coinbasevalue"])
        except:
          pass
          
        if (reward==0):
          try:
            reward=Decimal(b.getblocktemplate({})["coinbasevalue"])
          except:
            pass

        if (reward==0):            
          try:
            vouts=b.decoderawtransaction(b.getrawtransaction(b.getblock(b.getblockhash(b.getblockcount()))["tx"][0]))["vout"]
            for j, vout in enumerate(vouts):
              reward+=vout["value"]
          except:
            pass
              
        if (coin=="NVC" or coin=="DEM" or coin=="OSC" or coin=="PPC"):
          reward*=100

        # get proof-of-work difficulty
        # try getmininginfo first to minimize RPC calls; only use
        # getdifficulty if we must (as with NMC)
    
        algo=self.daemons[coin]["algo"]
        if (algo=="sha256"):
          algo="sha256d"
        try:
          mining_info=b.getmininginfo()
          diff=mining_info["difficulty_"+algo] # for MYR & other multi-algo coins
          if (type(diff) is dict):
            diff=diff["proof-of-work"]
        except:
          try:
            diff=mining_info["difficulty"]
            if (type(diff) is dict):
              diff=diff["proof-of-work"]
          except:
            diff=b.getdifficulty()
            if (type(diff) is dict):
              diff=diff["proof-of-work"]
              
        # get network hashrate
        # note 1: Novacoin reports this in MH/s, not H/s
        # note 2: Namecoin and Unobtanium don't report network hashrate, so 
        #         return 0 (it's only informational anyway)
                    
        try:
          nethashrate=mining_info["networkhashps"]
        except:
          try:
            nethashrate=int(mining_info["netmhashps"]*1000000)
          except:
            nethashrate=0
            
        # ported from my C# implementation at
        # https://github.com/salfter/CoinProfitability/blob/master/CoinProfitabilityLibrary/Profitability.cs

        interval=Decimal(86400) # 1 day
        target=Decimal(((65535<<208)*100000000000)/(diff*100000000000))
        revenue=Decimal(interval*target*hashrate*reward/(1<<256))
        
        # write to output dictionary

        self.out[coin]["reward"]=int(reward)
        self.out[coin]["difficulty"]=float(Decimal(diff).quantize(Decimal("1.00000000")))
        self.out[coin]["nethashespersec"]=int(nethashrate)
        self.out[coin]["daily_revenue"]=int(revenue)

        # if not Bitcoin, get exchange rate and BTC equivalent
 
        if (coin!="BTC"):
          bid=self.GetBestBid(coin.split("_")[0]) # 30 Jun 15: multi-algo compatibility
          self.out[coin]["exchrate"]=float(Decimal(bid[0]).quantize(Decimal("1.00000000")))
          self.out[coin]["exchange"]=bid[1]
          self.out[coin]["daily_revenue_btc"]=int(Decimal(revenue*Decimal(bid[0])))
        else:
          self.out[coin]["exchrate"]=float(Decimal(100000000).quantize(Decimal("1.00000000")))
          self.out[coin]["exchange"]="n/a"
          self.out[coin]["daily_revenue_btc"]=int(revenue)

        # copy these informational values from config dictionary

        self.out[coin]["algo"]=self.daemons[coin]["algo"]
        self.out[coin]["merged"]=self.daemons[coin]["merged"]
          
    return self.out

