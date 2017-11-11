# -*- encoding: utf8 -*-
# © Toons

"""
Usage: escrow register <2ndPublicKey>
		escrow link [<secret> -e]
		escrow send <amount> <address> [<message>]
		escrow validate [<id>]
		escrow save <name>
		escrow unlink

Options:
-e --escrow  tag to link account as escrower

Subcommands:
	register  : set second signature using escrow public key.
	link      : link to delegate using secret passphrases. If secret passphrases
				contains spaces, it must be enclosed within double quotes
				("secret with spaces"). If no secret given, it tries to link
				with saved escrow(s).
	send      : create cold transaction to send ARK if validated.
	validate  : broadcast cold transactions.
	save      : save linked escrow to a *.tok1 or *.tok2 file.
	unlink    : unlink from escrow.
"""

from .. import ArkyDict, ROOT, core, api, cfg
from . import common

import io, os, sys, binascii

ADDRESS = None
PUBLICKEY = None
KEY1 = None
KEY2 = None


def register(param):
	if _checkKey1():
		tx = common.generateColdTx(KEY1, PUBLICKEY, type=1, recipientId=ADDRESS, asset=ArkyDict(signature=ArkyDict(publicKey=param["<2ndPublicKey>"])))
		tx.address = ADDRESS
		if common.askYesOrNo("Broadcast %s?" % common.reprColdTx(tx)):
			common.prettyPrint(api.broadcastSerial(tx), log=True)
		else:
			sys.stdout.write("Broadcast canceled\n")


def link(param):
	global KEY1, KEY2, PUBLICKEY, ADDRESS

	if param["--escrow"]:
		if param["<secret>"]:
			KEY2 = core.getKeys(param["<secret>"].encode("ascii")).signingKey
		else:
			choices = common.findTokens("tok2")
			if choices:
				KEY2 = _load2ndToken(common.tokenPath(common.chooseItem("Second signature account(s) found:", *choices), "tok2"))
			else:
				sys.stdout.write("No second-tokend found\n")
		KEY1 = None
		PUBLICKEY = None
		ADDRESS = None

	else:
		if param["<secret>"]:
			keys = core.getKeys(param["<secret>"].encode("ascii"))
			KEY1 = keys.signingKey
			PUBLICKEY = keys.public
			ADDRESS = core.getAddress(keys)
		else:
			choices = common.findTokens("tok1")
			if choices:
				ADDRESS, PUBLICKEY, KEY1 = common.loadToken(common.tokenPath(common.chooseItem("First signature account(s) found:", *choices), "tok1"))
			else:
				sys.stdout.write("No first-token found\n")
		KEY2 = None
		
	if ADDRESS:
		common.BALANCES.register(ADDRESS)


def send(param):
	if _checkKey1():
		amount = common.floatAmount(param["<amount>"], ADDRESS) * 100000000
		if amount:
			tx = common.generateColdTx(KEY1, PUBLICKEY, type=0, amount=amount, recipientId=param["<address>"], vendorField=param["<message>"])
		else:
			tx = False
			sys.stdout.write("No %s left\n" % cfg.__TOKEN__)
		if tx:
			tx.address = ADDRESS
			sys.stdout.write("You can now give %s file to your escrow\n" % common.dropColdTx(tx))


def validate(param):
	if KEY2:
		if param["<id>"]:
			tx = common.loadColdTx(param["<id>"])
			filename = common.coldTxPath(param["<id>"])
		else:
			choices = common.findColdTx()
			if choices:
				choice = common.chooseItem("Cold transaction(s) found:", *choices)
				filename = common.coldTxPath(choice)
				tx = common.loadColdTx(choice)
			else:
				tx = False
		if tx:
			tmp = core.signSerial(tx, KEY2)
			tx.update({"id": tmp["id"], "signSignature": tmp["signature"]})
			if common.askYesOrNo("Broadcast %s?" % common.reprColdTx(tx)):
				broadcast = api.broadcastSerial(tx)
				common.prettyPrint(broadcast, log=True)
				if broadcast["success"]:
					os.remove(filename)
			else:
				sys.stdout.write("Broadcast canceled\n")
		else:
			sys.stdout.write("Cold transaction not found\n")


def save(param):
	if KEY1 and PUBLICKEY and ADDRESS:
		common.dropToken(common.tokenPath(param["<name>"], "tok1"), ADDRESS, PUBLICKEY, KEY1)
	elif KEY2:
		_drop2ndToken(common.tokenPath(param["<name>"], "tok2"), KEY2)


def unlink(param):
	global KEY1, KEY2, PUBLICKEY, ADDRESS
	KEY1, KEY2, PUBLICKEY, ADDRESS = None, None, None, None


# --------------
def _whereami():
	if ADDRESS:
		return "escrow[%s]" % common.shortAddress(ADDRESS)
	elif KEY2:
		k2 = binascii.hexlify(KEY2.to_string())
		k2 = k2.decode() if isinstance(k2, bytes) else k2
		return "escrow[%s]" % (common.shortAddress(k2))
	else:
		return "escrow"


def _checkKey1():
	if not KEY1:
		sys.stdout.write("No account linked\n")
		return False
	return True


def _drop2ndToken(filename, signingKey):
	common.checkFolderExists(filename)
	out = io.open(filename, "w")
	out.write(common.signingKey2Hex(signingKey))
	out.close()


def _load2ndToken(filename):
	in_ = io.open(filename, "r")
	data = in_.read()
	in_.close()
	return common.hex2SigningKey(data)
