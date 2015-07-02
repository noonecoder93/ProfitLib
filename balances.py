#!/usr/bin/env python
# coding=iso-8859-1

# balances.py: get wallet balances and find best bid on all exchanges
#
# Copyright © 2015 Scott Alfter
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
import json
import pprint
from ProfitLib import *

daemons=json.loads(open("daemon_config.json").read())
exchanges=json.loads(open("exchange_config.json").read())
pl=ProfitLib(daemons, exchanges)
pl.GetMarketIDs()

for i, coin in enumerate(daemons):
  if (daemons[coin]["active"]==1):
    url="http://"+daemons[coin]["username"]+":"+daemons[coin]["passwd"]+"@"+daemons[coin]["host"]+":"+str(daemons[coin]["port"])
    b=jsonrpc.ServiceProxy(url)
    try:
      bal=b.getbalance()
      if (bal>0):
        bid=pl.GetBestBid(coin)
        print coin+": "+str(bal),
        if (coin!="BTC"):
          print " ("+str((bid[0]*Decimal(bal)).quantize(Decimal("1.00000000")))+" BTC @ "+bid[1]+")"
        else:
          print
    except IOError:
      print coin+": offline"
