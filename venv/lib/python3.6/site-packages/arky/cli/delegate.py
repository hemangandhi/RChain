# -*- encoding: utf8 -*-
# © Toons

"""
Usage: delegate link [<secret> <2ndSecret>]
	   delegate save <name>
	   delegate unlink
	   delegate status
	   delegate voters

Subcommands:
	link   : link to delegate using secret passphrases. If secret passphrases
			 contains spaces, it must be enclosed within double quotes
			 ("secret with spaces"). If no secret given, it tries to link
			 with saved account(s).
	save   : save linked delegate to a *.tokd file.
	unlink : unlink delegate.
	status : show information about linked delegate.
	voters : show voters contributions ([address - vote] pairs).
"""

from .. import cfg, api, core, ROOT
from .. util import stats
from . import common

import io, os, sys

ADDRESS = None
PUBLICKEY = None
KEY1 = None
KEY2 = None
USERNAME = None
DELEGATE = None


def link(param):
	global ADDRESS, PUBLICKEY, KEY1, KEY2, USERNAME, DELEGATE
	
	if param["<secret>"]:
		keys = core.getKeys(param["<secret>"].encode("ascii"))
		KEY1 = keys.signingKey
		PUBLICKEY = keys.public
		ADDRESS = core.getAddress(keys)
		USERNAME = _checkIfDelegate()

	else:
		choices = common.findTokens("tokd")
		if choices:
			ADDRESS, PUBLICKEY, KEY1 = common.loadToken(common.tokenPath(common.chooseItem("Delegate account(s) found:", *choices), "tokd"))
			USERNAME = _checkIfDelegate()
		else:
			sys.stdout.write("No token found\n")
			unlink({})
			return

	if not USERNAME:
		sys.stdout.write("Not a delegate\n")
		ADDRESS, PUBLICKEY, KEY1, KEY2, USERNAME, DELEGATE = None, None, None, None, None, None
	elif param["<2ndSecret>"]:
		keys = core.getKeys(param["<2ndSecret>"].encode("ascii"))
		KEY2 = keys.signingKey
		
	if ADDRESS:
		common.BALANCES.register(ADDRESS)


def save(param):
	if KEY1 and PUBLICKEY and ADDRESS:
		common.dropToken(common.tokenPath(param["<name>"], "tokd"), ADDRESS, PUBLICKEY, KEY1)


def unlink(param):
	global ADDRESS, PUBLICKEY, KEY1, KEY2, USERNAME, DELEGATE
	common.BALANCES.pop(ADDRESS, None)
	ADDRESS, PUBLICKEY, KEY1, KEY2, USERNAME, DELEGATE = None, None, None, None, None, None


def status(param):
	if ADDRESS:
		common.prettyPrint(dict(DELEGATE, **api.Account.getAccount(ADDRESS, returnKey="account")))


def voters(param):
	if PUBLICKEY:
		accounts = api.Delegate.getVoters(common.hexlify(PUBLICKEY), returnKey="accounts")
		sum_ = 0.
		for addr, vote in ([c["address"],float(c["balance"]) / 100000000] for c in accounts):
			line = "    %s: %.3f\n" % (addr, vote)
			sys.stdout.write(line)
			sum_ += vote
		sys.stdout.write("    " + "-"*(len(line) - 5) + "\n")
		sys.stdout.write("    %s: %.3f\n" % (("%d voters" % len(accounts)).rjust(len(addr)), sum_))


# --------------
def _whereami():
	if USERNAME:
		return "delegate[%s]" % USERNAME
	else:
		return "delegate"


def _checkIfDelegate():
	global DELEGATE
	search = [d for d in api.Delegate.getCandidates() if d['publicKey'] == common.hexlify(PUBLICKEY)]
	if len(search):
		DELEGATE = search[0]
		return DELEGATE["username"]
	else:
		return None
