# -*- encoding: utf8 -*-
# © Toons

import binascii
import datetime
import json
import logging
import os
import pytz
import random
import requests
import sys
import traceback

# only GET method is implemented, no POST or PUT for security reasons
from .. import cfg, core, arkydify, ArkyDict, __version__, ROOT

UTC = pytz.UTC


# define api exceptions
class TransactionError(Exception):
	pass


class NetworkError(Exception):
	pass


class SeedError(Exception):
	pass


class PeerError(Exception):
	pass


def get(api, dic={}, **kw):
	"""
	ARK API call using requests lib. It returns server response as ArkyDict object.
	It uses default peers registered in SEEDS list.

	Argument:
	api (str) -- api url path

	Keyword argument:
	dic (dict) -- api parameters as dict type
	**kw       -- api parameters as keyword argument (overwriting dic ones)

	Returns ArkyDict
	"""
	# merge dic and kw values
	args = dict(dic, **kw)
	# API response contains several fields and wanted one can be extracted using
	# a returnKey that match the field name
	returnKey = args.pop("returnKey", False)
	args = dict([k.replace("and_", "AND:") if k.startswith("and_") else k, v] for k, v in args.items())
	try:
		text = requests.get(random.choice(SEEDS) + api, params=args, headers=cfg.__HEADERS__, timeout=10).text
		data = ArkyDict(json.loads(text))
	except Exception as error:
		data = ArkyDict({"success": False, "error": error})
		data.error = error
		if hasattr(error, "__traceback__"):
			data.details = "\n" + ("".join(traceback.format_tb(error.__traceback__)).rstrip())
	else:
		if data.success:
			data = data[returnKey] if returnKey in data else data
	return data


def _signTx(tx, secret=None, secondSecret=None):
	"""
	Try to sign Transaction with secret and secondSecret.

	Argument:
	tx (core.Transaction) -- transaction
	secret (str)          -- secret passphrase
	secondSecret (str)    -- second secret passphrase

	Returns core.Transaction object
	"""
	if not secret:
		try:
			return tx.sign()
		except core.NoSecretDefinedError:
			return tx
	else:
		return tx.sign(secret, secondSecret)


def sendTx(tx, secret=None, secondSecret=None, url_base=None):
	"""
	Send backed transaction using optional url_base and eventualy secrets. It
	returns server response as ArkyDict object. If secrets are given, transaction is
	signed and then broadcasted with signatures and id. It does not send secrets.

	Argument:
	tx (core.Transaction | list | tuple) -- transaction object(s) to be send

	Keyword argument:
	url_base     (str) -- the base api url to use
	secret       (str) -- secret of the account sending the transaction
	secondSecret (str) -- second secret of account sending the transaction

	Returns ArkyDict
	"""
	# use registered peer if no url_base is given
	if url_base == None:
		url_base = random.choice(SEEDS)

	if isinstance(tx, (list, tuple)):
		tx = [_signTx(t, secret, secondSecret) for t in tx]
	elif isinstance(tx, core.Transaction):
		tx = [_signTx(tx, secret, secondSecret)]
	else:
		raise TransactionError("Can not send %r into blockchain" % tx)
	transactions = json.dumps({"transactions": [t.serialize() for t in tx if t]})

	if cfg.__HOT_MODE__:
		try:
			text = requests.post(url_base + "/peer/transactions", data=transactions, headers=cfg.__HEADERS__, timeout=10).text
			data = ArkyDict(json.loads(text))
		except Exception as error:
			data = ArkyDict({"success": False, "error": error})
			if hasattr(error, "__traceback__"):
				data.details = "\n" + ("".join(traceback.format_tb(error.__traceback__)).rstrip())
		else:
			if data.success:
				data.transaction = "%r" % tx
	else:
		data = {"success": False, "error": "No connection found"}

	return data


def broadcast(tx, secret=None, secondSecret=None):
	"""
	Send transaction using multiple peers. It avoid broadcasting errors when large
	amount of peers are unresponsive or not up to date.

	Argument:
	tx (core.Transaction | list | tuple) -- transaction object(s) to be send

	Keyword argument:
	secret       (str) -- secret of the account sending the transaction
	secondSecret (str) -- second secret of account sending the transaction

	Returns ArkyDict
	"""
	result = sendTx(tx, secret=None, secondSecret=None)
	ratio = 0.
	if result.success:
		for peer in PEERS:
			if sendTx(tx, secret, secondSecret, peer).success:
				ratio += 1
	result.broadcast = "%.1f%%" % (ratio / len(PEERS) * 100)
	return result


def postData(url_base, data):
	"""
	Send serialized transaction using url_base node.

	Argument:
	url_base (str) -- node address to use as api entry point
	data (dict)    -- serialized transaction

	Returns ArkyDict server response
	"""
	if cfg.__HOT_MODE__:
		try:
			text = requests.post(url_base + "/peer/transactions", data=data, headers=cfg.__HEADERS__, timeout=10).text
			data = ArkyDict(json.loads(text))
		except Exception as error:
			data = ArkyDict({"success": False, "error": error})
			if hasattr(error, "__traceback__"):
				data.details = "\n" + ("".join(traceback.format_tb(error.__traceback__)).rstrip())
	else:
		data = {"success": False, "error": "No connection found"}
	return data


def broadcastSerial(serial):
	"""
	Send serialized transaction using multiple peers. It avoid broadcasting errors
	when large amount of peers are unresponsive or not up to date.

	Argument:
	serail (dict) -- serialized transaction

	Returns ArkyDict server response
	"""
	data = json.dumps({"transactions": [serial]})
	result = postData(random.choice(SEEDS), data)
	ratio = 0.
	if result["success"]:
		for peer in PEERS:
			if postData(peer, data).success: ratio += 1
	result["broadcast"] = "%.1f%%" % (ratio / len(PEERS) * 100)
	return result


def checkPeerLatency(peer, timeout=10):
	"""
	Return peer latency in seconds.
	"""
	try:
		r = requests.get(peer + '/api/blocks/getNethash', timeout=timeout)
	except:
		return False
	else:
		return r.elapsed.total_seconds()


def use(network="dark", custom_seed=None, broadcast=10, latency=1):
	"""
	Select ARK network.

	Keyword argument:
	network     (str) -- network name you want to connetc with
	custom_seed (str) -- a custom peer you want to choose
	broadcast   (int) -- max valid peer number to use for broadcasting
	latency     (int) -- max latency you want in second

	Returns None
	"""
	global SEEDS, PEERS, ROOT

	# find network configuration files (*.net) and load it if a filename match asked
	# network else throw error
	networks = [os.path.splitext(name)[0] for name in os.listdir(ROOT) if name.endswith(".net")]
	if len(networks) and network in networks:
		in_ = open(os.path.join(ROOT, network + ".net"), "r")
		data = json.load(in_)
		in_.close()
		network_properties = ([k, v] for k, v in data.items() if k in ["wif", "pubKeyHash", "messagePrefix"])
		for key, value in network_properties:
			data[key] = binascii.unhexlify(value)
		cfg.__NETWORK__.update(arkydify(data))
	else:
		raise NetworkError("Unknown %s network properties" % network)

	# update logger data so network appear on log
	logger = logging.getLogger()
	logger.handlers[0].setFormatter(logging.Formatter('[%s]' % network + '[%(asctime)s] %(message)s'))

	# in js month value start from 0, in python month value start from 1
	cfg.__BEGIN_TIME__ = datetime.datetime(2017, 3, 21, 13, 0, 0, 0, tzinfo=UTC)
	cfg.__NET__ = network

	# find seeds
	if custom_seed:
		seed_list = [custom_seed]
	else:
		port = cfg.__NETWORK__.port
		seed_list = ["http://%s:%s" % (ip, port) for ip in cfg.__NETWORK__.seeds]

	if not len(seed_list):
		sys.ps1 = "cold@%s>>> " % network
		sys.ps2 = "cold@%s... " % network
		cfg.__HOT_MODE__ = False
		PEERS = SEEDS = []
		return

	# select a valid seed
	SEEDS = []
	while not len(SEEDS) >= min(5, len(seed_list)):
		temp = random.choice(seed_list)
		if checkPeerLatency(temp, timeout=latency):
			SEEDS.append(temp)
		seed_list.pop(seed_list.index(temp))

	if not len(SEEDS):
		sys.ps1 = "cold@%s>>> " % network
		sys.ps2 = "cold@%s... " % network
		cfg.__HOT_MODE__ = False
		PEERS = SEEDS = []
		return

	# get all valid peers
	api_peers = []
	while not len(api_peers):
		try:
			result = requests.get(random.choice(SEEDS) + "/api/peers", timeout=latency).json()
			api_peers = result.get("peers", [])
		except requests.exceptions.ConnectionError:
			sys.ps1 = "cold@%s>>> " % network
			sys.ps2 = "cold@%s... " % network
			cfg.__HOT_MODE__ = False
			PEERS = SEEDS = []
			return

	peer_list = []
	result = requests.get(random.choice(SEEDS) + '/api/peers/version', timeout=latency).json()
	version = result.get("version", '0.0.0')

	good_peers = ["http://%(ip)s:%(port)s" % p for p in api_peers if p["status"] == "OK" and p["version"] == version]
	random.shuffle(good_peers)
	# select a set of peers for transaction broadcasting
	for peer in good_peers:
		if checkPeerLatency(peer, timeout=latency):
			peer_list.append(peer)
		if len(peer_list) == broadcast:
			break
	if not len(peer_list):
		sys.ps1 = "cold@%s>>> " % network
		sys.ps2 = "cold@%s... " % network
		cfg.__HOT_MODE__ = False
		PEERS = SEEDS = []
		return
	PEERS = peer_list

	# finish network conf
	cfg.__FEES__.update(get('/api/blocks/getFees', returnKey="fees"))
	autoconf = get('/api/loader/autoconfigure', returnKey="network")
	cfg.__EXPLORER__ = autoconf.get("explorer", False)
	cfg.__SYMBOL__ = autoconf.get("symbol", False)
	cfg.__TOKEN__ = autoconf.get("token", False)
	cfg.__HEADERS__.update({
		'Content-Type': 'application/json; charset=utf-8',
		'os': 'arky',
		'port': '1',
		'version': __version__,
		'nethash': autoconf.get("nethash", "")
	})

	sys.ps1 = "@%s>>> " % network
	sys.ps2 = "@%s... " % network
	cfg.__HOT_MODE__ = True


#################
## API wrapper ##
#################

class Loader:
	@staticmethod
	def getLoadingStatus(**param):
		return get('/api/loader/status', **param)

	@staticmethod
	def getSynchronisationStatus(**param):
		return get('/api/loader/status/sync', **param)

	@staticmethod
	def getAutoConfigure(**param):
		return get('/api/loader/autoconfigure', **param)


class Block:
	@staticmethod
	def getBlocks(**param):
		return get('/api/blocks', **param)

	@staticmethod
	def getBlock(id, **param):
		return get('/api/blocks/get', id=id, **param)

	@staticmethod
	def getNethash(**param):
		return get('/api/blocks/getNethash', **param)

	@staticmethod
	def getBlockchainFee(**param):
		return get('/api/blocks/getFee', **param)

	@staticmethod
	def getBlockchainFees(**param):
		return get('/api/blocks/getFees', **param)

	@staticmethod
	def getBlockchainHeight(**param):
		return get('/api/blocks/getHeight', **param)

	@staticmethod
	def getBlockchainEpoch(**param):
		return get('/api/blocks/getEpoch', **param)

	@staticmethod
	def getBlockchainMilestone(**param):
		return get('/api/blocks/getMilestone')

	@staticmethod
	def getBlockchainReward(**param):
		return get('/api/blocks/getReward')

	@staticmethod
	def getBlockchainSupply(**param):
		return get('/api/blocks/getSupply')

	@staticmethod
	def getBlockchainStatus(**param):
		return get('/api/blocks/getStatus')

	@staticmethod
	def getForgedByAccount(publicKey, **param):
		return get('/api/delegates/forging/getForgedByAccount', generatorPublicKey=publicKey, **param)


class Account:
	@staticmethod
	def getBalance(address, **param):
		return get('/api/accounts/getBalance', address=address, **param)

	@staticmethod
	def getPublicKey(address, **param):
		return get('/api/accounts/getPublicKey', address=address, **param)

	@staticmethod
	def getAccount(address, **param):
		return get('/api/accounts', address=address, **param)

	@staticmethod
	def getDelegates(address, **param):
		return get('/api/accounts/delegates', address=address, **param)

	@staticmethod
	def getDelegateFee(**param):
		return get('/api/accounts/delegates/fee', **param)

	@staticmethod
	def getTopAccounts(**param):
		return get('/api/accounts/top', **param)


class Delegate:
	@staticmethod
	def getDelegates(**param):
		return get('/api/delegates', **param)

	@staticmethod
	def getDelegate(username, **param):
		return get('/api/delegates/get', username=username, **param)

	@staticmethod
	def getVoters(publicKey, **param):
		return get('/api/delegates/voters', publicKey=publicKey, **param)

	@staticmethod
	def getCandidates(**param):
		delegates = []
		while 1:
			found = Delegate.getDelegates(offset=len(delegates), limit=51, **param).get("delegates", [])
			delegates += found
			if len(found) < 51:
				break
		return delegates

	@staticmethod
	def getDelegatesCount(address, **param):
		return get('/api/delegates/count', address=address, **param)

	@staticmethod
	def getDelegatesVoters(publicKey, **param):
		return get('/api/delegates/voters', publicKey=publicKey, **param)

	@staticmethod
	def getDelegateFee(address, **param):
		return get('/api/delegates/fee', address=address, **param)

	@staticmethod
	def getForgedByAccount(generatorPublicKey, **param):
		return get('/api/delegates/forging/getForgedByAccount', generatorPublicKey=generatorPublicKey, **param)

	@staticmethod
	def getNextForgers(address, **param):
		return get('/api/delegates/getNextForgers', address=address, **param)


class Transaction(object):
	@staticmethod
	def getTransactionsList(**param):
		return get('/api/transactions', **param)

	@staticmethod
	def getUnconfirmedTransactions(**param):
		return get('/api/transactions/unconfirmed', **param)

	@staticmethod
	def getTransaction(transactionId, **param):
		return get('/api/transactions/get', id=transactionId, **param)

	@staticmethod
	def getUnconfirmedTransaction(transactionId, **param):
		return get('/api/transactions/unconfirmed/get', id=transactionId, **param)


class Peer:
	@staticmethod
	def getPeersList(**param):
		return get('/api/peers', **param)

	@staticmethod
	def getPeer(ip, port, **param):
		return get('/api/peers', ip=ip, port=port, **param)

	@staticmethod
	def getPeerVersion(**param):
		return get('/api/peers/version', **param)


class Multisignature:
	@staticmethod
	def getPendingMultiSignatureTransactions(publicKey, **param):
		return get('/api/multisignatures/pending', publicKey=publicKey, **param)

	@staticmethod
	def getAccountsOfMultisignature(publicKey, **param):
		return get('/api/multisignatures/accounts', publicKey=publicKey, **param)


class Signature:
	@staticmethod
	def getSignatureFee(address, **param):
		return get('/api/signatures/fee', address=address, **param)


class Transport:
	@staticmethod
	def getPeersList(**param):
		return get('/peer/list', **param)

	@staticmethod
	def getBlocksByIds(ids, **param):
		return get('/peer/blocks/common', id=id, **param)

	@staticmethod
	def getBlock(address, **param):
		return get('/peer/block', address=address, **param)

	@staticmethod
	def getBlocks(address, **param):
		return get('/peer/blocks', **param)

	@staticmethod
	def getTransactions(**param):
		return get('/peer/transactions', **param)

	@staticmethod
	def getTransactionsFromIds(ids, **param):
		return get('/peer/transactions', ids=ids, **param)

	@staticmethod
	def getHeight(**param):
		return get('/peer/height', **param)

	@staticmethod
	def getStatus(**param):
		return get('/peer/status', **param)
