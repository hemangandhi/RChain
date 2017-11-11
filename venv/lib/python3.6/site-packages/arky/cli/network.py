# -*- encoding: utf8 -*-
# © Toons

"""
Usage: network use [<name> -b <number> -s <seed> -l <ms>]
	   network browse [<element>]
	   network publickey <secret>
	   network address <secret>
	   network wif <secret>
	   network delegates
	   network staking
	   network update
	   network ping

Options:
-b <number> --broadcast <number> peer number to use for broadcast       [default: 10]
-s <seed> --custom-seed <seed>   custom seed you want to connect with
-l <ms> --latency <ms>           maximum latency allowed in miliseconds [default: 1000]

Subcommands:
	use       : select network.
	browse    : browse network.
	publickey : returns public key from secret.
	address   : returns address from secret.
	delegates : show delegate list.
	staking   : show coin-supply ratio used on delegate voting.
	update    : update balance of all linked account.
	ping      : print selected peer latency.
"""

from .. import cfg, api, core
from . import common

import sys, hashlib, webbrowser


def _whereami():
	return "network"


def use(param):
	if not param["<name>"]:
		choices = common.findNetworks()
		if choices:
			param["<name>"] = common.chooseItem("Network(s) found:", *choices)
		else:
			sys.stdout.write("No Network found\n")
			return False
	api.use(
		param.get("<name>"),
		custom_seed=param.get("--custom-seed"),
		broadcast=int(param.get("--broadcast")),
		latency=float(param.get("--latency"))/1000
	)


def ping(param):
	common.prettyPrint(dict(
		[[peer,api.checkPeerLatency(peer)] for peer in api.PEERS] +\
		[["api>"+seed,api.checkPeerLatency(seed)] for seed in api.SEEDS]
	))


def browse(param):
	element = param["<element>"]
	if element:
		if len(element) == 34:
			webbrowser.open(cfg.__EXPLORER__ + "/address/" + element)
		elif len(element) == 64:
			webbrowser.open(cfg.__EXPLORER__ + "/tx/" + element)
		elif element == "delegate":
			webbrowser.open(cfg.__EXPLORER__ + "/delegateMonitor")
	else:
		webbrowser.open(cfg.__EXPLORER__)


def address(param):
	sys.stdout.write("    %s\n" % core.getAddress(core.getKeys(param["<secret>"].encode("ascii"))))


def publickey(param):
	sys.stdout.write("    %s\n" % common.hexlify(core.getKeys(param["<secret>"].encode("ascii")).public))


def wif(param):
	sys.stdout.write("    %s\n" % core.getWIF(hashlib.sha256(param["<secret>"].encode("ascii")).digest(), cfg.__NETWORK__))


def delegates(param):
	delegates = api.Delegate.getDelegates(limit=51, returnKey='delegates')
	maxlen = max([len(d["username"]) for d in delegates])
	i = 1
	for name, vote in sorted([(d["username"], float(d["vote"]) / 100000000) for d in delegates], key=lambda e: e[-1], reverse=True):
		sys.stdout.write("    #%02d - %s: %.3f\n" % (i, name.ljust(maxlen), vote))
		i += 1


def update(param):
	common.BALANCES.reset()
	common.prettyPrint(common.BALANCES)
	

def staking(param):
	sys.stdout.write("    %.2f%% of coin supply used to vote for delegates\n" % sum(d["approval"] for d in api.Delegate.getCandidates()))
