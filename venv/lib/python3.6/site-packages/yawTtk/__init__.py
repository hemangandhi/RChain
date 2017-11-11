# -*- coding:latin-1 -*-
"""
(~) https://github.com/Moustikitos/yawTtk

Copyright© 2006-2015, THOORENS Bruno
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.
* Neither the name of the *yawTtk* nor the names of its contributors may be
used to endorse or promote products derived from this software without specific
prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

import sys, os

try: from Tkinter import *
except ImportError: from tkinter import *

if sys.version_info[:2] <= (2,7):
	from yawTtk import *
	from megawidget import *
else:
	from yawTtk.yawTtk import *
	from yawTtk.megawidget import *


__version__ = "1.0.5"
__author__ = "Bruno THOORENS"

# SIMPLE DEMO ======================================================================================
def demo():
	main = Tk()

	image1 = main.tk.call("image", "create", "photo", "-data",
"R0lGODlhUgBZAPcAAAAAAAY6NApOMg5vLgFmMwdxLQN3MhpnLBRoNRl3KxV5MydVNjl9Hi5uJxlPQhhzQiZNSidUSClXUjpJSTlbTDdaWCNkSS1nViJ5TCh8"\
"UDpmSDtjWj9wWT1iYkF3N3J+Lk9VVUtwVEdqaEp3bFZublV5Zld3dml5RGp0dAWGMgybLgOZMxqHKxWJNBWZLRmYNAqjMheoLBSpMh2yLhu0Mj6DHyeGKSOJ"\
"MSWWKCGSODSFIzuPNTSYJDi9HyaqKyOpMyi3KyW5MjmjIzW5Jx+GQBGfQCeMRSyDUiGTQDmIWzObRTaYVTyOYT2RYCSiRi6pVzeqQTyoVTm6RDeyWz7DHy3B"\
"LSvDMjjIKjTKMj7RKzvQMD7LQEuXG1SVLVKtGEuzJ3mFN2W4EWqwKk6BVESKZkmWaV2FbF+CfVKfbVaadEKmWkC+Ske3VlK+U0miY1KmalmldFmybV21cGOK"\
"VWWEaGSCeGuZYWOdfnGLZn+Xb3yYemKifWa6d1XUHEzWJVzgHF7gIGzVEGvWMHDpEm/kLUzNS0nCVFDBS1LEW1XTVl3HZm3aSmrEd2fUanHCfnfWe3nkSFuB"\
"gWuHhmSfgHONjHSRj3qUkmekgm20hHWvj3eskXK4h3ewknjGhn3ThJK5LYydVo6VZpWqTZ2wcqa4U6Swc4PUEIjOJpD4BZPtLaL+F7L7K5PNR47rRbPMTbHR"\
"cbL1TrzrbcT+M8fWXNDZZM37Utf4aOv/V+77cImJiYOZmZeZl4mfoIqhiIqomoe2nZClhZ2lnJO8hYykpJWopp6xsaSumqWlpa2yqKe4uLO7qLq6uq6/wIrF"\
"m4PZh4/QmpXcmZbHp53WpofghI/hkJfjmLTIj6LLr6bLt6LYq6fTtLXCp7nKvbDZuqjiibTkuKzBwbXJw7TTwr3lwsrUm8nMsdr1jdLgpO/8kPX7ssLDw8LN"\
"0MbYysnU1Nna2sPrxcvk08TwxNrjytTm2tfy2dzm4t/14fD60ejr6un06u7x8PX45/n5+QAAAAAAAAAAACH5BAEAAP8ALAAAAABSAFkAAAj/AP+pG0iwoMGD"\
"CBMqXKaOocNlECNKnEhx4r+LAt3hq7cRn0Z399zVmyfSHUl3KFOqXMmypcuXMFOqO4ZRHT96786Ne8fz3c6dPdn5HEdU3DhxRpEqXSouHFKnSqE27RaOajdu"\
"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")

	image2 = main.tk.call("image", "create", "photo", "-data",
"R0lGODlhEAAQAPcAAAAAAD9QclJXfH19fX5+fn9/fwtivAxjvA1nuw1kvRBkvTBPiDFRizFRjDJRjjlYlDdvsyBzyih4yEddhEdehUVgh0Nlj0VhikRijENm"\
"kUBmlFp5mj2HziOL5CaO5iuP5iuP5yuR5iyQ5iyQ5y6S5i+S5yqQ6DSQ4zWU5WKAuXeUrUia4IS035ux1p653Jy635e+55u74pm95aO525vD7b3a7Mva48nb"\
"58za48/c5NDc5NDc5dfg5fL19/L1+PL1+fP1+v//+v//+/7//P7//f7//v///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAP8ALAAAAAAQABAAAAipAP8JHEiwoMGD"\
"BFegKDEixAcSIjx0AGHiBAeBCBQcSMDxgAEDByREgCBAxT8WPHLsWKmDpQ0cN2ps+EfDiJEiOIvczGlTwz8YRoIIHTpUiJAiGf7JCCqEqNMiFv7FCOqUqJAh"\
"GP69oFpVqBAiF/654Nr1a4V/M4wQITKkrdu2RIpQ+NcCyA8fPX7o3fvD7oR/KR40aMBgsOHBCxwEGFiAgOPHkAcgnPwvIAA7")

	image3 = main.tk.call("image", "create", "photo", "-data",
"R0lGODlhEAAQAPcAAAAAAAA27wgz7hNX9Rld+BdkySNU8zBa5CRszSRx1y9z0Tl51UZs7Upy5UV39ld48ll78g2XEBeeCCGhJzahLjmrMECsKEy2Mk22N0q7"\
"NWXASXXEX3fLUESB2VCK30yG/VuV52yC02WD6GGL+WWc6m6V8XKi7O9sQetqVO9/WvV8R5WQXImuaYTJZY3Odc+Mbv6FReSEYOeObOWBdOmEcPCEZvCRb/GW"\
"bPeadP+ndtPLL/bGDvvJDf/RAPzSBP/VAP/dAP/gAP/mAP/rAP/0AP/8AsXKRdvCZOTcSPfZROzNapOTk5WVlZmRnJmZmZubm5u4i6Kioqampqenp5ug4ZSo"\
"8ZvShKPXjqbWkqzVnKrG9LHM/7jC9bvR+b7T+duVg9iXje+pou3Zi/fgn/biv9fHz9bJ0MTM8NbV69Td7Nbg7tnj79zg7N7m8+LVzOvfyfnZ2OLo3e3i0PPo"\
"1eXg6urq6uHq+ers8Ovt8u3u8+7v+e7x++7z/e70/e/0/vHv8PH07/Xz8PTz9vb08vX19fb29Pb29ff39/f3+PX59vf5/f3y8/v48fr69/n5+fv7+/j7//n+"\
"//34/Pz4/v/7///9+v/++P//+fz8/P39/f78///+/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAP8ALAAAAAAQABAAAAjmAJ8IHEiwoMAt"\
"XbxoMUEChIcOCxQgKJBAYCQ/fPrQKWOGjZ02a9SksSNwk0k4NGzckOEmESVJgSqVNBmmBo4cMVi4wHLFCqCZi1CcUAHjxQYOGi60mDQTzgwwX1KsyIChgoQs"\
"mmZygTCiBBUoFCZEsBAn65NNmR4YcPAhRBIkRnSI0ZNJoKUzAgIMINCkCBEhQMbs2STwUhUGIhocODIkyA8ecu7UfYIpzyBGf9Ao8dFjh8FNhQwRMtRI0Bwy"\
"b84+cvLv7KHXrxEpgoTnSZ0l/1qb3M3b0RMmuf9JmSKluPHhUYLnDggAOw==")

	image4 = main.tk.call("image", "create", "photo", "-data",
"R0lGODlhEAAQAPcAAAAAAAAAXQAAZQAAbwAAdAAAdwAAeQ4oVRQtWxUvXilHczZEaERBYgYujx49jCM8jChFmjZXpTdYpDZYpk5XjkxkikFjlEtrll5phVxq"\
"hltvj1xqiE14q2VviWV1k212kHJ+l09wwGSHr2SJrWuKrWKBtFyN3W+fzmOV6Xum34eXr4KTs5qlup2nuoeqypSvzZWyz5S215O42Jm20pu92qOuwqCyxae2"\
"yaK4y6+1xa6/z6290arB1rfCz73H0KjK56/K5KbI+bTK4rjV7bHW9LPW9bfX9bfW+LPc/7/k/cPL2MnO18jU38DX7MHY7sfb6MnZ5sne8tXe6MTl98Pn/8Xj"\
"/Mbl/8fp/8rl/8nn/87n/8nq/8vt/8/o/83q/8/u/8T3/9rm79zj6tXn+NDp/9Hr/9Ls/9Hv/9br/9Xs/9nu/93u/9fw/9H4/9ny/9zw/9/0/+Xl5OLn7O/t"\
"7ebr8eDv/eP0/+by/+L//+X6/+/z9u/09+n1/ej1/+z2/+v4/+v6/+/6/+/9/+3+//X08vP7//H///T4+/n///7//wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAP8ALAAAAAAQABAAAAjeAP8J/CdGT6KD"\
"h5QMXEiH0MElDHIcTCRloZw5EykEgDAx0Y6BcRIhKiQyyKBEfQIdVPGPyR5EfhBBWcGiBiI7awAlEgLCB58/dwSFcSDgQaI3aNTkiQKiRx2cbxLxKDABURoy"\
"Ztw0yaBjDJw0aQy9IBDBUBcsXsoA2WDjCRszWgbBGCDBUBYrW6qQ+IDjiZMzX/CUMNBgChcqRmggEHjjyRAvR0KgMJGCCpEYCjoMbNFixo8kV9oUkTEiAYaF"\
"Aj1U+IEEiYgDC06jHnjBBRgLsmcvvHCCQ27dAzFomB0QADs="
)

	main["background"] = "pink"
	style = Style()
	
	customize_all_widgets(True)
	if sys.platform == "win32": style.theme_use("xpnative")
	else: style.theme_use("clam")

	style.configure("TButton", foreground = "steelblue3", relief = "flat")
	style.configure("Horizontal.TPanedwindow.Sash", background = "green")
	style.layout("Vertical.MacScrollbar", """
		Vertical.Scrollbar.trough -children {
			Scrollbar.uparrow -side top -sticky {}
			Scrollbar.downarrow -side bottom -sticky {}
			Scrollbar.uparrow -side bottom -sticky {}
			Vertical.Scrollbar.thumb -sticky nswe
		}"""
	)

	main["borderwidth"] = 2
	main.columnconfigure(0, weight = 1)
	main.rowconfigure(0, weight = 1)
	main.title("All Tile widgets")

	panedzone = Paned(main, orient = "horizontal", background = "pink")
	panedzone.grid(row = 0, column = 0, sticky = "nwse")

	widgetpanel = Notebook(panedzone, background = "pink", tabposition="n", tabforeground = "steelblue3", tabrelief = "flat", tabfont = ("tahoma", "7", "bold"))
	widgetpanel.enableTraversal()

	label_info = Label(widgetpanel,

		background = "lightgreen", foreground="yellow4",
		font = ("calibri", "10", "bold"),
		padding = (15, 15),
		anchor = "center",
		justify = "right",

		image = image1, compound = "left",

		text = "yawTtk " + __version__ + "\n"\
		       "Python version : " + sys.version.split(" ")[0] + "\n"\
		       "TCL\\Tk version : " + Tkinter._tkinter.TK_VERSION + "\n"\
		       "Ttk version : %s" % main.tk.call("package","version","tile")
	)

	radiovalue = Tkinter.StringVar(main, "1", "radiovalue")

	labelwidget = Frame(widgetpanel, padding = 0, background = "lightgreen")

	b = Button(labelwidget, background = "lightgreen", anchor = "center", text = "button", font = ("calibri", "10", "bold"),
		image = (image2, {"active" : image4, "focus" : image3}), compound = "left"
	)
	b.pack(expand = "yes", fill = "both", padx = 1, pady = 1)

	mb = Menubutton(labelwidget, utext = "_menubutton", direction = "right", background = "green4", foreground = "grey", font = ("calibri", "10", "bold"))
	mb.menu_insert("command", ulabel = "_command")
	mb.menu_insert("separator")
	mb.menu_insert("radiobutton", image=image2, selectimage=image3, compound="left", indicatoron=False, ulabel = "_radiobutton 2", variable = radiovalue, value = "second")
	mb.menu_insert("radiobutton", image=image2, selectimage=image3, compound="left", indicatoron=False, ulabel = "r_adiobutton 1", variable = radiovalue, value = "first")
	mb.menu_insert("separator")
	mb.menu_insert("checkbutton", image=image2, selectimage=image3, compound="left", indicatoron=False, ulabel = "chec_kbutton", variable = radiovalue)
	mb.pack(expand = "yes", fill = "both", padx = 1, pady = 1)

	Checkbutton(labelwidget, padding = (5, 0), text = "checkbutton", variable = radiovalue, background = "green4").pack(expand = "yes", fill = "both", padx = 1, pady = 1)
	Radiobutton(labelwidget, padding = (5, 0), text = "radiobutton 1", variable = radiovalue, value = "first", background = "green3").pack(expand = "yes", fill = "both", padx = 1, pady = 1)
	Radiobutton(labelwidget, padding = (5, 0), text = "radiobutton 2", variable = radiovalue, value = "second", background = "green1").pack(expand = "yes", fill = "both", padx = 1, pady = 1)

	# ===================================
	scalevalue = Tkinter.IntVar(main, 61, "scalevalue")
	packer = Frame(widgetpanel, padding = 0)
	packer.rowconfigure(0, weight = 1)
	packer.columnconfigure(0, weight = 1)

	specialwidget = megawidget.Scrolledframe(packer, padding = 2, relief="solid", stretch = True)
	scrollx = Autoscrollbar(packer, target=specialwidget, orient = "horizontal")
	scrolly = Autoscrollbar(packer, target=specialwidget, orient = "vertical", style="MacScrollbar")
	scrollx.grid(row = 1, column = 0, sticky = "nwse")
	scrolly.grid(row = 0, column = 1, sticky = "nwse")
	specialwidget.grid(row = 0, column = 0, sticky = "nwse")

	sc = Scale(specialwidget(), variable = scalevalue, from_ = 1, to = 100, orient = "vertical")
	sc.pack(side = "right", expand = "no", fill = "both", padx = 1, pady = 1)
	sc["background"] = "blue"
	w = Progressbar(specialwidget(), variable = scalevalue, orient = "vertical")
	w.pack(side = "right", expand = "no", fill = "both", padx = 1, pady = 1)
	print(style.layout("Vertical.TProgressbar"))

	Scale(specialwidget(), variable = scalevalue, from_ = 1, to = 100, orient = "horizontal").pack(expand = "no", fill = "both", padx = 1, pady = 1)
	Progressbar(specialwidget(), variable = scalevalue, orient = "horizontal").pack(expand = "no", fill = "both", padx = 1, pady = 1)
	Separator(specialwidget()).pack(expand = "no", fill = "both", padx = 5, pady = 10)
	Entry(specialwidget(), textvariable = scalevalue).pack(expand = "yes", fill = "both", padx = 1, pady = 1)

	cb = Combobox(specialwidget(), state = "readonly", values = style.theme_names(), listbackground="red", listheight=4)
	cb.pack(expand = "yes", fill = "both", padx = 1, pady = 1)
	cb.bind("<<ComboboxSelected>>", lambda arg: style.theme_use(arg.widget.get()))
	if sys.platform == "win32": cb.set("xpnative")
	else: cb.set("clam")

	Frame(specialwidget(), background = "lightblue", height = 200).pack(expand = "yes", fill = "both", padx = 1, pady = 1)
	# ===================================

	# ===================================
	packer002 = Frame(widgetpanel, padding = 0)
	packer002.rowconfigure(0, weight = 1)
	packer002.columnconfigure(0, weight = 1)

	customwidget = megawidget.Scrolledframe(packer002, padding = 0, stretch = True)
	scrollx = Autoscrollbar(packer002, target=customwidget, orient="horizontal")
	scrolly = Autoscrollbar(packer002, target=customwidget, orient="vertical")
	scrollx.grid(row = 1, column = 0, sticky = "nwse")
	scrolly.grid(row = 0, column = 1, sticky = "nwse")
	customwidget.grid(row = 0, column = 0, sticky = "nwse")

	test2 = megawidget.CalendarFrame(customwidget(), format = "%d/%m/%Y", relief = "flat", padding = 3, background = "lightblue")
	test2.pack(padx = 2, pady = 2)

	# ===================================

	widgetpanel.add(labelwidget, utext = "_Classic", compound = "left", padding = 2, image = image2)

	# specialwidget.update()
	widgetpanel.add(packer, utext = "_Special", compound = "left", padding = 2, image = image3)

	widgetpanel.add(packer002, utext = "C_ustom", compound = "left", padding = 2, image = \
	"R0lGODlhEAAQAPcAAAAAAJwLCq8ZE7UtHb4iF6AwMKI+O6NAO45YV55ORpBwdpN0c6lXV6heWrVVUr51ctArHN4yHuQ4IeeEf4qKjouMko6Plo+PmJyFhZOT"\
	"nJiYmZqampaYoJ6ep9KIg+uJgfKTivWWiv+Xg/ubjeqooOqqpfS6s9zc6QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
	"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
	"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
	"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
	"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
	"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
	"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\
	"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAP8ALAAAAAAQABAAAAhPAP8JHEiwoEAK"\
	"Ggwq/FfhxIaFBi10gKjwAkWDGS4W5KCRoAIHCDoGmPCgYwEBHzxg6EgARIkFGhlACGEC5kUDEUaQ6HhAgogEHRsM6FgwIAA7")

	widgetpanel.add(label_info, utext = "_Info", compound = "left", padding = 2, image = image4)

	widgetoption = Labelframe(
		panedzone,
		background = "pink",
		text = "paned",
		width = 100,
		labelbackground = "pink",
		labelforeground = "steelblue3",
		labelfont = ("tahoma", "8", "bold"),
		labelanchor = "n",
		labeloutside = True,
		labelmargins = 0
	)

	panedzone.add(widgetpanel, weight = 0)
	panedzone.add(widgetoption, weight = 0)

	Sizegrip(widgetoption, background = "pink").place(relx = 1.0, rely = 1.0, anchor = "se")

	main.focus()
	main.mainloop()
