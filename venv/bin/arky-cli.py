# -*- coding:utf-8 -*-
# created by Toons on 01/05/2017

import os, sys
sys.path.append(os.path.join(os.path.dirname(sys.executable), "site-packages.zip"))

from arky import cli
from arky import api

if __name__ == "__main__":
	if len(sys.argv) > 1 and os.path.exists(sys.argv[-1]):
		cli.launch(sys.argv[-1])
	else:
		cli.start()
