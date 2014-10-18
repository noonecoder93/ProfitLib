#!/usr/bin/env python
# coding=iso-8859-1

# profit.py: a simple coin picker
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

from ProfitLib import *
import json
from decimal import *
import pprint
import sys
import operator

if (len(sys.argv)!=2):
  print "Usage: "+sys.argv[0]+" algo"
  sys.exit(1)
  
algo=sys.argv[1]

pl=ProfitLib(json.loads(open("profit_config.json").read()))
profit=pl.Calculate()

result={}

for i, coin in enumerate(profit):
  if (profit[coin]["algo"]==algo and profit[coin]["merged"]==[]):
    result[coin]=Decimal(profit[coin]["daily_revenue_btc"])/100000000
    for j, mergecoin in enumerate(profit):
      if (profit[mergecoin]["algo"]==algo and profit[mergecoin]["merged"]!=[]):
        for k, basecoin in enumerate(profit[mergecoin]["merged"]):
          if (basecoin==coin):
            result[coin]+=Decimal(profit[mergecoin]["daily_revenue_btc"])/100000000

sorted_result=sorted(result.items(), key=operator.itemgetter(1), reverse=True)

for i, r in enumerate(sorted_result):
  print r[0]+" "+str(r[1])

  