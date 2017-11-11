# -*- encoding: utf8 -*-
# © Toons
__version__ = "0.4.1"

import os, imp, sys, threading, logging, requests, random

try:
	from raven import Client
	client = Client('https://8ba879a5cbed46cea1a4450b07c773ad:8b85ed9b7a3640aa91938082c2aba07c@sentry.io/229186')
except ImportError:
	pass

logging.getLogger('requests').setLevel(logging.CRITICAL)
__PY3__ = True if sys.version_info[0] >= 3 else False
if __PY3__: from io import BytesIO as StringIO
else: from StringIO import StringIO

main_is_frozen = lambda: (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__"))

# deal with home and root directory
ROOT = os.path.normpath(os.path.abspath(os.path.dirname(sys.executable if main_is_frozen() else __file__)))

if sys.platform[:3] == "win":
	HOME = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"])
else:
	HOME = os.environ.get("HOME", ".")

logging.basicConfig(
	filename=os.path.normpath(os.path.join(ROOT, __name__+".log")) if main_is_frozen() else os.path.normpath(os.path.join(HOME, "."+__name__)),
	format='[...][%(asctime)s] %(message)s',
	level=logging.INFO,
)

def setInterval(interval):
	""" threaded decorator
	>> @setInterval(10)
	... def tick(): print("Tick")
	>> stop = tick() # print 'Tick' every 10 sec
	>> type(stop)
	<class 'threading.Event'>
	>> stop.set() # stop printing 'Tick' every 10 sec
	"""
	def decorator(function):
		def wrapper(*args, **kwargs):
			stopped = threading.Event()

			def loop():  # executed in another thread
				while not stopped.wait(interval):  # until stopped
					function(*args, **kwargs)
			t = threading.Thread(target=loop)
			t.daemon = True  # stop if the program exits
			t.start()
			return stopped
		return wrapper
	return decorator


def arkydify(dic):
	result = ArkyDict()
	for k, v in dic.items():
		if isinstance(v, dict): setattr(result, k, arkydify(v))
		else: setattr(result, k, v)
	return result


class ArkyDict(dict):
	"""
	Python dict with javascript behaviour.
	>> ad = ArkyDict()
	>> ad["key1"] = "value1"
	>> ad.key2 = "value2"
	>> sorted(ad.items(), key=lambda e:e[0])
	[('key1', 'value1'), ('key2', 'value2')]
	"""
	def __setattr__(self, attr, value): return dict.__setitem__(self, attr, value)

	def __getattr__(self, attr, default=False): return dict.get(self, attr, default)

	def __delattr__(self, attr): return dict.__delitem__(self, attr)
