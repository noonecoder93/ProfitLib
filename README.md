ProfitLib.py
============

This does the work of websites such as CoinChoose and CoinWarz, only with
data obtained directly from coin daemons under your control (and from
the exchanges you select, which provide exchange-rate data).  

Exchange information is available from your choice of Cryptsy, Bittrex, 
Cryptopia, C-CEX, Poloniex, and Bleutrade.

The constructor takes two dictionaries for configuration;
daemon_config_example.json and exchange_config_example.json provide examples
of the information that needs to be provided.  Most fields are
self-explanatory; the "active" field should be set to 1 to check a coin or 0
to skip it.

On each call of the Calculate() method, updated exchange-rate information is
pulled from the exchanges and updated mining information is pulled from each coin
daemon.  It returns a dictionary with current network hashrate, difficulty,
and block reward, and expected 24-hour revenue in the coin in question and
in Bitcoin.

For informational purposes, the coin algorithm and merge-mining information
are passed through.  The "merged" array for a coin should be populated with
the coins for which the pools you use support merged mining of this coin. 
For instance, Eligius supports merged mining of Namecoin and WeMineLTC
supports merged mining of Dogecoin, so you might set merged to ["BTC"] for
Namecoin and ["LTC"] for Dogecoin.  Leave the merged array empty if merged
mining isn't supported.

This should be enough information for a script to decide which coin would be
most profitable to mine.

ProfitTest.py
=============

This is a trivial test-harness script that loads configuration from a JSON
file and writes JSON to stdout.

profit.py
=========

This is a simple implementation of a coin picker.  It takes the algorithm
(sha256, scrypt, etc.) to check as a parameter and returns a sorted list of
coins and expected 24-hour revenue, with the most profitable at the top.

balances.py
===========

This script dumps all non-zero wallet balances and finds the best exchange
at which to trade each.

Dependencies
============

bitcoinrpc:
  https://github.com/jgarzik/python-bitcoinrpc

PyCryptsy:
  https://github.com/salfter/PyCryptsy

python-bittrex:
  https://github.com/ericsomdahl/python-bittrex

PyCryptopia:
  https://github.com/salfter/PyCryptopia

PyCCEX:
  https://github.com/salfter/PyCCEX

poloniex:
  https://github.com/salfter/poloniex

bleuBot:
  https://github.com/Durendal/bleuBot

Donations
=========

Donations are always welcome if you find this useful...hit the tipjar!

bitcoin://1TipsGocnz2N5qgAm9f7JLrsMqkb3oXe2
