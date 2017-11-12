# -*- encoding: utf8 -*-
# © Toons

# -p <pkeys> --public-keys <pkeys> 64-char message
#        account send <amount> <address> [-p <pkeys> <message>]

"""
Usage: account link [<secret> <2ndSecret>]
	   account save <name>
	   account unlink
	   account status
	   account register <username>
	   account register 2ndSecret <secret>
	   account vote [-ud] [<delegate>]
	   account send <amount> <address> [<message>]

Options:
-u --up    up vote delegate name folowing
-d --down  down vote delegate name folowing

Subcommands:
	link     : link to account using secret passphrases. If secret passphrases
			   contains spaces, it must be enclosed within double quotes
			   ("secret with spaces"). If no secret given, it tries to link
			   with saved account(s).
	save     : save linked account to a *.tok file.
	unlink   : unlink account.
	status   : show information about linked account.
	register : register linked account as delegate (cost 25 ARK);
			   or
			   register second signature to linked account (cost 5 ARK).
	vote     : up or down vote delegate.
	send     : send ARK amount to address. You can set a 64-char message.
"""

from .. import cfg, api, core, ROOT, ArkyDict
from . import common

import io, os, sys

ADDRESS = None
PUBLICKEY = None
KEY1 = None
KEY2 = None


def link(param):
	global ADDRESS, PUBLICKEY, KEY1, KEY2
	
	if param["<secret>"]:
		keys = core.getKeys(param["<secret>"].encode("ascii"))
		KEY1 = keys.signingKey
		PUBLICKEY = keys.public
		ADDRESS = core.getAddress(keys)

	else:
		choices = common.findTokens("tok")
		if choices:
			ADDRESS, PUBLICKEY, KEY1 = common.loadToken(common.tokenPath(common.chooseItem("Delegate account(s) found:", *choices), "tok"))
		else:
			sys.stdout.write("No token found\n")
			unlink({})
			return

	if param["<2ndSecret>"]:
		keys = core.getKeys(param["<2ndSecret>"].encode("ascii"))
		KEY2 = keys.signingKey

	if ADDRESS:
		common.BALANCES.register(ADDRESS)


def save(param):
	if KEY1 and PUBLICKEY and ADDRESS:
		common.dropToken(common.tokenPath(param["<name>"], "tok"), ADDRESS, PUBLICKEY, KEY1)


def unlink(param):
	global ADDRESS, PUBLICKEY, KEY1, KEY2
	common.BALANCES.pop(ADDRESS, None)
	ADDRESS, PUBLICKEY, KEY1, KEY2 = None, None, None, None


def status(param):
	if ADDRESS:
		common.prettyPrint(api.Account.getAccount(ADDRESS, returnKey="account"))


def register(param):
	global ADDRESS, PUBLICKEY, KEY1, KEY2

	KEY2 = common.checkKeys(KEY1, KEY2, ADDRESS)
	if KEY2 != False:
		if param["2ndSecret"]:
			newPublicKey = common.hexlify(core.getKeys(param["<secret>"].encode("ascii")).public)
			tx = common.generateColdTx(KEY1, PUBLICKEY, KEY2,
				type=1,
				recipientId=ADDRESS,
				asset=ArkyDict(signature=ArkyDict(publicKey=newPublicKey))
			)
		else:
			username = param["<username>"].encode("ascii").decode()
			tx = common.generateColdTx(KEY1, PUBLICKEY, KEY2,
				type=2,
				asset=ArkyDict(delegate=ArkyDict(username=username))
			)
		tx.address = ADDRESS
		if common.askYesOrNo("Broadcast %s?" % common.reprColdTx(tx)):
			common.prettyPrint(api.broadcastSerial(tx), log=True)
		else:
			sys.stdout.write("Broadcast canceled\n")


def vote(param):
	global ADDRESS, PUBLICKEY, KEY1, KEY2

	KEY2 = common.checkKeys(KEY1, KEY2, ADDRESS)
	if KEY2 != False:
		candidates = api.Delegate.getCandidates() if param["--up"] else api.Account.getVotes(ADDRESS, returnKey="delegates")
		if param["<delegate>"]:
			delegate = param["<delegate>"].encode("ascii").decode()
			delegates = [("+" if param["--up"] else "-")+d['publicKey'] for d in candidates if d['username'] == delegate]
			if len(delegates):
				tx = common.generateColdTx(KEY1, PUBLICKEY, KEY2,
					type=3,
					recipientId=ADDRESS,
					asset=ArkyDict(votes=delegates)
				)
				tx.address = ADDRESS
				if common.askYesOrNo("Broadcast %s?" % common.reprColdTx(tx)):
					common.prettyPrint(api.broadcastSerial(tx), log=True)
				else:
					sys.stdout.write("Broadcast canceled\n")
			else:
				sys.stdout.write("Nothing to vote\n")
		elif len(candidates):
			common.prettyPrint(candidates[0])


def send(param):
	global ADDRESS, PUBLICKEY, KEY1, KEY2

	KEY2 = common.checkKeys(KEY1, KEY2, ADDRESS)
	if KEY2 != False:
		amount = common.floatAmount(param["<amount>"], ADDRESS)*100000000
		if amount:
			tx = common.generateColdTx(KEY1, PUBLICKEY, KEY2, type=0, amount=amount, recipientId=param["<address>"], vendorField=param["<message>"])
			tx.address = ADDRESS
			if common.askYesOrNo("Broadcast %s?" % common.reprColdTx(tx)):
				sys.stdout.write("Sending A%.8f to %s...\n" % (tx["amount"]/100000000, tx["recipientId"]))
				common.prettyPrint(api.broadcastSerial(tx), log=True)
			else:
				sys.stdout.write("Broadcast canceled\n")
		else:
			sys.stdout.write("No transaction defined\n")


# --------------
def _whereami():
	if ADDRESS:
		return "account[%s]" % common.shortAddress(ADDRESS)
	else:
		return "account"
