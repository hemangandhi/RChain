# -*- encoding: utf8 -*-
# © Toons

from . import wdg
from .. import __PY3__
from arky import cli, api, cfg, core

import io, os, imp, sys, json, yawTtk

_exit=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAAG7AAABuwBHnU4NQAAAAd0SU1FB9sMFws0LDm0tJ4AAAKWSURBVDjLjZJNSxtR"\
"FIafO6OGMaMkuhCF0A8DAbd1W8yq1IWbQin40eImLjSiXUhIgwS1aiOoiY2g4sIPuutKqq104V9QpCK0pV0NipQx6kykzp0ubIJSW3p2997zPuflvQduqImJCQBGRka6BwYGRgESiQT/VWNjYwBMT0/3ZDIZN5vN"\
"ut3d3c8BOjs7/+gXN0FSqVSitrZ22DRN6TgOiqIo29vb0cXFxdd/ndzX14frusVzf39/aHZ21k2n0y7gK9xvbGyg63qxrwSgtbWVqakphBBks9m3uVzuVmVlZZuqqti2DeCmUqmvpmm+aW5uTmxtbREOhwFQAObn"\
"5xFCsLCw8KW6uvqREOJHPp/H4/HgOA6AUFU1FwgEXsTj8dVwOMzMzMwloKOjA13XmZubG9N1/a6UEsMw3juO49E0DSklQOn5+fmOlJL6+vq2SCTSEo1GLwErKysAlJeXxwD29vZW0un0pGmaOcMwPliWtSmEkPF4"\
"/Klt258dxyEUCqWvZTA5OXm/pKSEi4sLhoeHewFGR0e/AQ+vBn16ehqtqKjY8Pv9dwAVcJTfbwGAk5MTAPNvP7W7u7vtui6KolBTUxMohuj1eg9d10XTtH8uWTAYrAWQUnJwcHBYBHR1dX0sAHp6enoB2tvbi8Kh"\
"oSEAfD5fDOD4+PgUsACUQppnZ2frUkoaGxvTTU1N91ZXV4uAwcFBYrFYRNO0x0IIDMN4eeMqLy0tuaWlpQWLm7Ztr5eVlXm8Xu8zv9/fcHR0hGVZ32Ox2O2CRrlqcXl52W9ZlqWqKnV1dQ+CweB0IBB4VVVV1aAo"\
"Cvl8fqcgDoVC1x0kk0mSySQA4+PjEZ/P9wSoB346jvNpf39/PpPJvANoaWlhbW0NgF/89hAL3mpSPAAAAABJRU5ErkJggg=="\

wdg.DataView.headers = ["id", "date", "type", "amount", "senderId", "recipientId", "vendorField"]


@wdg.setInterval(60)
def _update_candidates():
	wdg.AddressPanel.candidates = api.Delegate.getCandidates()


class Glob:
	"""
	Class containing all global variables and functions
	"""

	sendpanel = None
	votepannel = None
	rootfolder = ""
	history = {"version": 0}

	@staticmethod
	def main_is_frozen():
		return (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__"))

	@staticmethod
	def getRootFolder():
		Glob.rootfolder = os.path.normpath(os.path.abspath(os.path.dirname(sys.executable if Glob.main_is_frozen() else __file__)))
# ----------------------


def checkWalletMenu():
	if wdg.AddressPanel.address:
		pass


def appendHistoryValue(key, value):
	if key not in Glob.history[cfg.__NET__]:
		Glob.history[cfg.__NET__][key] = [value]
	elif value not in Glob.history[cfg.__NET__][key]:
		Glob.history[cfg.__NET__][key].append(value)


def getHistoryList(key):
	return Glob.history.get(cfg.__NET__, {}).get(key, [])


def dropHistory():
	out = io.open(os.path.join(Glob.rootfolder, "history.json"), "w" if __PY3__ else "wb")
	json.dump(Glob.history, out, indent=2)
	out.close()


def loadHistory():
	in_ = io.open(os.path.join(Glob.rootfolder, "history.json"), "r" if __PY3__ else "rb")
	Glob.history = json.load(in_)
	in_.close()


def signTransaction(widget, destroy=True):
	wdg.KeyDialog.address = wdg.AddressPanel.address
	wdg.KeyDialog(widget.winfo_toplevel(), border=8).show()
	if wdg.KeyDialog.check:
		sys.stdout.write("Sending Transaction...")
		tx = widget.getTransaction()
		tx.sign(wdg.KeyDialog.passphrase1, wdg.KeyDialog.passphrase2)
		answer = api.broadcast(tx)
		cli.common.prettyPrint(answer, log=True)
		if destroy:
			widget.destroy()
		if answer.success:
			appendHistoryValue("sendpanel.recipientId", tx.recipientId)


def hidePanels():
	try: Glob.sendpanel.destroy()
	except: pass
	try: Glob.votepannel.destroy()
	except: pass


def showSendPanel(master):
	hidePanels()
	Glob.sendpanel = wdg.SendPanel(master, relief="solid", padding=4).place(anchor="center", relx=0.5, rely=1-1/1.618033989)
	Glob.sendpanel.recipientId["values"] = Glob.history.get(cfg.__NET__, {}).get("sendpanel.recipientId", [])
	Glob.sendpanel.button["command"] = lambda w=Glob.sendpanel: signTransaction(w)


def showVotePanel(master):
	hidePanels()
	Glob.votepannel = wdg.VotePanel(master, relief="solid", padding=4).place(anchor="center", relx=0.5, rely=1-1/1.618033989)
	Glob.votepannel.button["command"] = lambda w=Glob.votepannel: signTransaction(w, destroy=False)


def loadTransaction(*args, **kwargs):
	Glob.addresspanel.update()
	Glob.transactionpanel.update()
	if wdg.AddressPanel.address != None:
		appendHistoryValue("addresspanel.wallet", wdg.AddressPanel.address)
		Glob.addresspanel.combo["values"] = tuple(getHistoryList("addresspanel.wallet"))


def networkUse(network):
	hidePanels()
	api.use(network)
	wdg.AddressPanel.candidates = api.Delegate.getCandidates()
	if cfg.__NET__ not in Glob.history:
		Glob.history[cfg.__NET__] = {}
	Glob.addresspanel.wallet.set("")
	Glob.addresspanel.combo["values"] = tuple(getHistoryList("addresspanel.wallet"))


def exit():
	dropHistory()
	sys.exit()


#############
def launch():

	# main window
	root = yawTtk.Tkinter.Tk()
	if not __PY3__:
		root.tk.eval("package require Img")

	root.withdraw()
	root.title(u"\u0466rky wallet")

	Glob.getRootFolder()
	try: loadHistory()
	except: pass
	if cfg.__NET__ not in Glob.history:
		Glob.history[cfg.__NET__] = {}

	style = yawTtk.Style()
	style.layout("Treeview", "Treeview.treearea -sticky nswe")

	toplevel = yawTtk.Toplevel(root)
	toplevel.withdraw()
	toplevel["border"] = 4

	# menu widget
	menubar = yawTtk.Menu(root)

	walletmenu = yawTtk.Menu(menubar, tearoff=False, name="walletmenu")
	def check_wm():
		if wdg.AddressPanel.address == None:
			walletmenu.entryconfigure(0, state="disabled")
			walletmenu.entryconfigure(1, state="disabled")
		else:
			walletmenu.entryconfigure(0, state="normal")
			walletmenu.entryconfigure(1, state="normal")
	walletmenu["postcommand"] = check_wm
	walletmenu.add("cascade", ulabel=u"_Send", command=lambda m=toplevel: showSendPanel(m))
	walletmenu.add("cascade", ulabel=u"_Vote", command=lambda m=toplevel: showVotePanel(m))
	walletmenu.add("separator")
	walletmenu.add("command", compound="left", image=_exit, ulabel="_Close", command=sys.exit)

	networkmenu = yawTtk.Menu(menubar, tearoff=False, name="networkmenu")
	for net in cli.common.findNetworks():
		networkmenu.add("radiobutton", variable="ui.network", label=net, value=net, command=lambda n=net: networkUse(n))

	menubar.add("cascade", ulabel="_Wallet", menu=walletmenu)
	menubar.add("cascade", ulabel="_Network", menu=networkmenu)

	Glob.addresspanel = wdg.AddressPanel(toplevel).grid(row=0, column=0, sticky="nesw")
	Glob.addresspanel.wallet.trace("w", loadTransaction)
	Glob.transactionpanel = wdg.TransactionPanel(toplevel, padding=1, relief="solid", width=0).grid(row=1, column=0, padx=4, pady=4, sticky="nesw")
	sys.stdout = wdg.LogPanel(
		toplevel,
		relief="flat", 
		selectbackground="black", selectforeground="lightgrey", 
		highlightthickness=0, 
		activestyle="none", 
		height=5, 
		font=("courier", 8), 
		background="black", foreground="lightgrey"
	).grid(row=2, column=0, sticky="nesw", padx=4, pady=4)

	# show toplevel
	toplevel.rowconfigure(1, weight=1)
	toplevel.columnconfigure(0, weight=1)
	toplevel.rowconfigure(2, minsize=180)

	networkUse("ark")
	root.setvar("ui.network", cfg.__NET__)

	if "win" in sys.platform: 
		try: toplevel.iconbitmap('ark.ico')
		except: pass
	toplevel.geometry("800x500+0+0")
	toplevel.minsize(800, int(800/1.618033989))
	toplevel.bind("<Escape>", lambda event: hidePanels())
	toplevel.protocol('WM_DELETE_WINDOW', exit)
	toplevel.configure(menu=menubar)
	wdg.Dialog.center(toplevel, True)
	toplevel.deiconify()

	__stop_update_candidates = _update_candidates()
	root.mainloop()
	__stop_update_candidates.set()
