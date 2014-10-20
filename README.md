ProfitLib.py
============

This does the work of websites such as CoinChoose and CoinWarz, only with
data obtained directly from coin daemons under your control (and from
Cryptsy, which provides exchange-rate data).  

The constructor takes a dictionary for configuration;
profit_config_example.json provides an example of the information that needs
to be provided.  Most fields are self-explanatory; the "active" field should
be set to 1 to check a coin or 0 to skip it.

On each call of the Calculate() method, updated exchange-rate information is
pulled from Cryptsy and updated mining information is pulled from each coin
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

Dependencies
============

bitcoinrpc & jsonrpc:
  https://github.com/jgarzik/python-bitcoinrpc

PyCryptsy (included as submodule):
  https://github.com/salfter/PyCryptsy

Donations
=========

Donations are always welcome if you find this useful...hit the tipjar!

bitcoin://1TipsGocnz2N5qgAm9f7JLrsMqkb3oXe2