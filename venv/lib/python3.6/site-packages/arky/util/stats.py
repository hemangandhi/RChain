# -*- encoding: utf8 -*-
# © Toons

from .. import api, slots
import datetime

try:
	from matplotlib import pyplot as plt
	__MATPLOTLIB__ = True
except:
	__MATPLOTLIB__ = False


def plot2D(*points, **kw):
	if __MATPLOTLIB__:
		xlabel = kw.pop("xlabel", None)
		ylabel = kw.pop("ylabel", None)
		title = kw.pop("title", None)

		plt.plot([p[:2] for p in points], **kw)
		for x, y, label in [p for p in points if len(p) == 3]: plt.annotate(label, (x, y))

		if xlabel: plt.xlabel(xlabel)
		if ylabel: plt.ylabel(ylabel)
		if title: plt.title(title)
		plt.show()


def getTransactions(timestamp=0, **param):
	param.update(returnKey="transactions", limit=50, orderBy="timestamp:desc")
	txs = api.Transaction.getTransactionsList(**param)
	if isinstance(txs, list) and len(txs):
		while txs[-1]["timestamp"] >= timestamp:
			param.update(offset=len(txs))
			search = api.Transaction.getTransactionsList(**param)
			txs.extend(search)
			if len(search) < 50:
				break
	elif not len(txs):
		raise Exception("Address has null transactions.")
	else:
		raise Exception(txs.get("error", "Api error"))
	return sorted([t for t in txs if t["timestamp"] >= timestamp], key=lambda e: e["timestamp"], reverse=True)


def getHistory(address, timestamp=0):
	# get all inputs
	tx_in = api.Transaction.getTransactionsList(recipientId=address, returnKey="transactions", limit=50, orderBy="timestamp:desc")
	if isinstance(tx_in, list) and len(tx_in):
		while tx_in[-1]["timestamp"] >= timestamp:
			search = api.Transaction.getTransactionsList(recipientId=address, returnKey="transactions", limit=50, offset=len(tx_in), orderBy="timestamp:desc")
			tx_in.extend(search)
			if len(search) < 50:
				break

		# get all outputs
		tx_out = api.Transaction.getTransactionsList(senderId=address, returnKey="transactions", limit=50, orderBy="timestamp:desc")
		while tx_out[-1]["timestamp"] >= timestamp:
			search = api.Transaction.getTransactionsList(senderId=address, returnKey="transactions", limit=50, offset=len(tx_out), orderBy="timestamp:desc")
			tx_out.extend(search)
			if len(search) < 50:
				break

		tx_in += [t for t in tx_out if t not in tx_in]
	elif not len(tx_in):
		raise Exception("Address has null transactions.")
	else:
		raise Exception(tx_in.get("error", "Api error"))
	return sorted([t for t in tx_in if t["timestamp"] >= timestamp], key=lambda e:e["timestamp"], reverse=True)


def getBalanceHistory(address, timestamp=0):
	balance = float(api.Account.getBalance(address, returnKey="balance"))/100000000.
	history = getHistory(address, timestamp)

	if not history:
		return [(slots.getRealTime(timestamp), balance), (datetime.datetime.now(slots.UTC), balance)]

	else:
		result = [(datetime.datetime.now(slots.UTC), balance)]
		for tx in history:
			result.insert(0, (slots.getRealTime(tx["timestamp"]), balance))
			balance += ((tx["fee"]+tx["amount"]) if tx["senderId"] == address else -tx["amount"])/100000000.
		result.insert(0, (slots.getRealTime(timestamp), balance))
		return result


def getVoteHistory(address, timestamp=0):
	history = [tx for tx in getHistory(address, timestamp) if tx["type"] == 3]
	candidates = dict([d["publicKey"], d["username"]] for d in api.Delegate.getCandidates())

	if not history:
		return []
	else:
		result = []
		for tx in history:
			pkey = tx["asset"]["votes"][0][1:]
			way = 0 if tx["asset"]["votes"][0][0] == "-" else 1
			result.insert(0, (slots.getRealTime(tx["timestamp"]), way, candidates[pkey]))
		return result


def getVoteForce(address, **kw):
	delegate_pubk = kw.pop("delegate_pubk", "")
	now = datetime.datetime.now(slots.UTC)
	delta = datetime.timedelta(**kw)
	timestamp_limit = slots.getTime(now - delta)

	# get actual balance and transaction history
	balance = float(api.Account.getBalance(address, returnKey="balance"))/100000000.
	history = getHistory(address, timestamp_limit)

	# if no transaction over periode integrate balance over delay and return it
	if not history:
		return balance*max(1./3600, delta.total_seconds()/3600)

	end = slots.getTime(now)
	sum_ = 0.
	cumulate = True
	for tx in history:
		delta_t = (end - tx["timestamp"])/3600
		if cumulate:
			sum_ += balance * delta_t
		balance += ((tx["fee"]+tx["amount"]) if tx["senderId"] == address else -tx["amount"])/100000000.
		if tx["type"] == 3:
			if delegate_pubk != "":
				if tx["asset"]["votes"][0] == "-%s" % delegate_pubk:
					if cumulate: sum_ = 0.
					else: cumulate = True
				elif tx["asset"]["votes"][0] == "+%s" % delegate_pubk:
					cumulate = False 
			else:
				break
		end = tx["timestamp"]

	if cumulate:
		sum_ += balance * (end - timestamp_limit)/3600

	return sum_


def getExVoters(delegate_pubk, **kw):
	now = datetime.datetime.now(slots.UTC)
	delta = datetime.timedelta(**kw)
	timestamp_limit = slots.getTime(now - delta)
	votes = [t for t in getTransactions(timestamp_limit, type=3) if t["type"] == 3]
	return [t["senderId"] for t in votes if t["asset"]["votes"][0] == "-%s" % delegate_pubk]
