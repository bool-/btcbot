from decimal import *

def to_btc(value):
	return int(round(value * 1e8))

def to_string(value):
	return str(to_float(value))

def to_float(value):
	return float(value / 1e8)

def getbalance(bitcoin, account):
	return to_btc(bitcoin.getbalance(account, 1))
