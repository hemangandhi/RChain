# -*- encoding: utf8 -*-
# © Toons

from . import __PY3__
if not __PY3__: import cfg
else: from . import cfg

import datetime, pytz
UTC = pytz.UTC

INTERVAL = 10
DELEGATES = 11


def getTime(time=None):
	delta = (datetime.datetime.now(UTC) if not time else time) - cfg.__BEGIN_TIME__
	return delta.total_seconds()


def getRealTime(epoch=None):
	epoch = getTime() if epoch == None else epoch
	return cfg.__BEGIN_TIME__ + datetime.timedelta(seconds=epoch)


def getSlotNumber(epoch=None):
	return int((getTime() if not epoch else epoch) // INTERVAL)


def getSlotTime(slot):
	return slot * INTERVAL


def getNextSlot():
	return getSlotNumber() + 1


def getLastSlot(slot):
	return slot + DELEGATES
