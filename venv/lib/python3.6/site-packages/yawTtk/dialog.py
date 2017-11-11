# -*- encoding:utf-8 -*-
import os, sys, yawTtk

def _info(toplevel):
	if toplevel.tk.call("wm", "overrideredirect", toplevel) == 0:
		toplevel.overrideredirect(True)
		toplevel.update()
		x, y = toplevel.winfo_rootx(), toplevel.winfo_rooty()
		w, h = toplevel.winfo_width(), toplevel.winfo_height()
		toplevel.overrideredirect(False)
		toplevel.update()
		_x, _y = toplevel.winfo_rootx(), toplevel.winfo_rooty()
		dx, dy = abs(x-_x)//2, abs(y-_y)
	else:
		dx, dy = 0, 0
		w, h = toplevel.winfo_reqwidth(), toplevel.winfo_reqheight()

	return w, h, (dx, dy, dx, dx)

def center(toplevel, onscreen=False):

	W, H = toplevel.winfo_screenwidth(), toplevel.winfo_screenheight()
	w, h, padding = _info(toplevel)

	# center on master ork on screen
	if toplevel.master != None and not onscreen:
		_w, _h = toplevel.master.winfo_width(), toplevel.master.winfo_height()
		x = min(W-w-padding[0]-padding[2], toplevel.master.winfo_rootx() - padding[0] + _w/2 - w/2)
		y = min(H-h-padding[1]-padding[3], toplevel.master.winfo_rooty() - padding[1] + _h/2 - h/2)
	else:
		x = (W-w-padding[0]-padding[2])/2
		y = (H-h-padding[1]-padding[3])/2

	toplevel.geometry("+%d+%d" % (max(0,x), max(0,y)))


class BaseDialog(yawTtk.Toplevel):

	def ismapped(self):
		return self.tk.call('winfo', 'ismapped', self)

	def show(self):
		self.deiconify()
		return self

	def hide(self):
		self.withdraw()
		return self

	def __init__(self, master=None, cnf={}, **kw):
		config = dict(cnf, **kw)
		self.border = config.pop("border", 5)
		self.background = config.pop("background", "white")
		self.override_redirect = config.pop("overrideredirect", False)
		title = config.pop("title", "")

		yawTtk.Toplevel.__init__(self, master, config, border=0)
		yawTtk.Toplevel.withdraw(self)
		yawTtk.Toplevel.overrideredirect(self, self.override_redirect)

		self.title(title)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		self.mainframe = yawTtk.Frame(self, border=0, padding=self.border, relief="flat")
		self.fillMainFrame()

		self.buttonframe = yawTtk.Frame(self, background=self.background, border=0, padding=self.border, relief="flat")
		self.fillButton()

		self.mainframe.grid(row=0, column=0, sticky="nesw")
		yawTtk.Separator(self, padding=0, border=0).grid(row=1, column=0, sticky="ew")
		self.buttonframe.grid(row=2, column=0, sticky="nesw")

		self.tweak()

	def tweak(self):
		center(self)
		self.protocol('WM_DELETE_WINDOW', self.destroy)
		self.resizable(False, False)

	def fillMainFrame(self): pass

	def fillButton(self): pass

	def show(self):
		if not self.ismapped():
			return self.deiconify()
		else:
			self.tkraise()


class MsgDialog(BaseDialog):

	def deiconify(self):
		BaseDialog.deiconify(self)
		if sys.platform.startswith("win"):
			self.master.wm_attributes("-disable", True)

	def destroy(self):
		if sys.platform.startswith("win"): 
			self.master.wm_attributes("-disable", False)
		BaseDialog.destroy(self)
		
	def __init__(self, master=None, cnf={}, **kw):
		config = dict(cnf, **kw)
		self.message = config.pop("message", "")
		self.detail = config.pop("detail", "")
		self.icon = config.pop("icon", None)
		BaseDialog.__init__(self, master, **config)

	def fillMainFrame(self):
		self.mainframe.columnconfigure(1, weight=1)
		yawTtk.Label(self.mainframe, border=0, relief="flat", padding=(self.border, self.border, 0, 0), image=question if self.icon == None else self.icon, compound="image").grid(row=0, column=0)
		yawTtk.Label(self.mainframe, font=("tahoma", 8, "bold"), justfy="left", text=self.message, border=0, padding=self.border).grid(row=0, column=1, sticky="nesw")
		if self.detail != "": yawTtk.Label(self.mainframe, border=0, text=self.detail, padding=(self.border, 0, self.border, self.border), wraplength=200).grid(row=1, column=0, columnspan=2, sticky="nesw")

	def fillButton(self):
		yawTtk.Button(self.buttonframe, font=("tahoma", 8, "bold"), image=tick16, compound="left", background=self.background, default="active", text="Ok", width=-1, padding=2, command=self.destroy).pack(side="right")
		# if sys.platform.startswith("win"): self.attributes("-transparent", "white")


class Toolwindow(BaseDialog):

	def deiconify(self):
		if not self.mapped: center(self)
		yawTtk.Toplevel.deiconify(self)
		self.mapped = True

	def tweak(self):
		self.mapped = False
		self.protocol('WM_DELETE_WINDOW', self.withdraw)
		self.attributes("-topmost", True, "-alpha", 0.9)
		if sys.platform.startswith("win"):
			self.attributes("-toolwindow", True)
		self.resizable(False, False)

	def fillButton(self):
		yawTtk.Button(self.buttonframe, font=("tahoma", 8, "bold"), image=tick16, compound="left", background=self.background, default="active", text="Hide", width=-1, padding=2, command=self.withdraw).pack(side="right")


class ValueDialog(BaseDialog):

	value = None

	def deiconify(self):
		BaseDialog.deiconify(self)
		self.tk.call("tkwait", "window", self._w)

	def close(self):
		self.destroy()

	def cancel(self):
		self.value=False
		self.destroy()

	def ok(self):
		self.value=True
		self.destroy()


close16=\
"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"

cancel=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAHd"\
"SURBVDjLpZNraxpBFIb3a0ggISmmNISWXmOboKihxpgUNGWNSpvaS6RpKL3Ry//Mh1wgf6PElaCyzq67O09nVjdVlJbSDy8Lw77PmfecMwZg/I/GDw3DCo8H"\
"CkZl/RlgGA0e3Yfv7+DbAfLrW+SXOvLTG+SHV/gPbuMZRnsyIDL/OASziMxkkKkUQTJJsLaGn8/iHz6nd+8mQv87Ahg2H9Th/BxZqxEkEgSrq/iVCvLsDK9a"\
"wtvfxb2zjD2ARID+lVVlbabTgWYTv1rFL5fBUtHbbeTJCb3EQ3ovCnRC6xAgzJtOE+ztheYIEkqbFaS3vY2zuIj77AmtYYDusPy8/zuvunJkDKXM7tYWTiyG"\
"WFjAqeQnAD6+7ueNx/FLpRGAru7mcoj5ebqzszil7DggeF/DX1nBN82rzPqrzbRayIsLhJqMPT2N83Sdy2GApwFqRN7jFPL0tF+10cDd3MTZ2AjNUkGCoyO6"\
"y9cRxfQowFUbpufr1ct4ZoHg+Dg067zduTmEbq4yi/UkYidDe+kaTcP4ObJIajksPd/eyx3c+N2rvPbMDPbUFPZSLKzcGjKPrbJaDsu+dQO3msfZzeGY2TCv"\
"KGYQhdSYeeJjUt21dIcjXQ7U7Kv599f4j/oF55W4g/2e3b8AAAAASUVORK5CYII="

cross16=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAIh"\
"SURBVDjLlZPrThNRFIWJicmJz6BWiYbIkYDEG0JbBiitDQgm0PuFXqSAtKXtpE2hNuoPTXwSnwtExd6w0pl2OtPlrphKLSXhx07OZM769qy19wwAGLhM1ddC"\
"184+d18QMzoq3lfsD3LZ7Y3XbE5DL6Atzuyilc5Ciyd7IHVfgNcDYTQ2tvDr5crn6uLSvX+Av2Lk36FFpSVENDe3OxDZu8apO5rROJDLo30+Nlvj5RnTlVNA"\
"Ks1aCVFr7b4BPn6Cls21AWgEQlz2+Dl1h7IdA+i97A/geP65WhbmrnZZ0GIJpr6OqZqYAd5/gJpKox4Mg7pD2YoC2b0/54rJQuJZdm6Izcgma4TW1WZ0h+y8"\
"BfbyJMwBmSxkjw+VObNanp5h/adwGhaTXF4NWbLj9gEONyCmUZmd10pGgf1/vwcgOT3tUQE0DdicwIod2EmSbwsKE1P8QoDkcHPJ5YESjgBJkYQpIEZ2KEB5"\
"1Y6y3ojvY+P8XEDN7uKS0w0ltA7QGCWHCxSWWpwyaCeLy0BkA7UXyyg8fIzDoWHeBaDN4tQdSvAVdU1Aok+nsNTipIEVnkywo/FHatVkBoIhnFisOBoZxcGt"\
"Qd4B0GYJNZsDSiAEadUBCkstPtN3Avs2Msa+Dt9XfxoFSNYF/Bh9gP0bOqHLAm2WUF1YQskwrVFYPWkf3h1iXwbvqGfFPSGW9Eah8HSS9fuZDnS32f71m8KF"\
"Y7xs/QZyu6TH2+2+FAAAAABJRU5ErkJggg=="

folder16=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAGr"\
"SURBVDjLxZO7ihRBFIa/6u0ZW7GHBUV0UQQTZzd3QdhMQxOfwMRXEANBMNQX0MzAzFAwEzHwARbNFDdwEd31Mj3X7a6uOr9BtzNjYjKBJ6nicP7v3KqcJFax"\
"hBVtZUAK8OHlld2st7Xl3DJPVONP+zEUV4HqL5UDYHr5xvuQAjgl/Qs7TzvOOVAjxjlC+ePSwe6DfbVegLVuT4r14eTr6zvA8xSAoBLzx6pvj4l+DZIezuVk"\
"G9fY2H7YRQIMZIBwycmzH1/s3F8AapfIPNF3kQk7+kw9PWBy+IZOdg5Ug3mkAATy/t0usovzGeCUWTjCz0B+Sj0ekfdvkZ3abBv+U4GaCtJ1iEm6ANQJ6fEz"\
"rG/engcKw/wXQvEKxSEKQxRGKE7Izt+DSiwBJMUSm71rguMYhQKrBygOIRStf4TiFFRBvbRGKiQLWP29yRSHKBTtfdBmHs0BUpgvtgF4yRFR+NUKi0XZcYjC"\
"eCG2smkzLAHkbRBmP0/Uk26O5YnUActBp1GsAI+S5nRJJJal5K1aAMrq0d6Tm9uI6zjyf75dAe6tx/SsWeD//o2/Ab6IH3/h25pOAAAAAElFTkSuQmCC"

tick16=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAGr"\
"SURBVDjLvZPZLkNhFIV75zjvYm7VGFNCqoZUJ+roKUUpjRuqp61Wq0NKDMelGGqOxBSUIBKXWtWGZxAvobr8lWjChRgSF//dv9be+9trCwAI/vIE/26gXmvi"\
"W5bqnb8yUK028qZjPfoPWEj4Ku5HBspgAz941IXZeze8N1bottSo8BTZviVWrEh546EO03EXpuJOdG63otJbjBKHkEp/Ml6yNYYzpuezWL4s5VMtT8acCMQc"\
"b5XL3eJE8VgBlR7BeMGW9Z4yT9y1CeyucuhdTGDxfftaBO7G4L+zg91UocxVmCiy51NpiP3n2treUPujL8xhOjYOzZYsQWANyRYlU4Y9Br6oHd5bDh0bCpSO"\
"ixJiWx71YY09J5pM/WEbzFcDmHvwwBu2wnikg+lEj4mwBe5bC5h1OUqcwpdC60dxegRmR06TyjCF9G9z+qM2uCJmuMJmaNZaUrCSIi6X+jJIBBYtW5Cge7cd"\
"7sgoHDfDaAvKQGAlRZYc6ltJlMxX03UzlaRlBdQrzSCwksLRbOpHUSb7pcsnxCCwngvM2Rm/ugUCi84fycr4l2t8Bb6iqTxSCgNIAAAAAElFTkSuQmCC"

stop16=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAJO"\
"SURBVDjLpZI9T1RBFIaf3buAoBgJ8rl6QVBJVNDCShMLOhBj6T+wNUaDjY0WmpBIgYpAjL/AShJ+gVYYYRPIony5IETkQxZ2770zc2fGYpflQy2MJzk5J5M5"\
"z/vO5ESstfxPxA4erL4Zuh4pLnoaiUZdq7XAGKzRJVbIBZ3JPLJaD9c/eCj/CFgZfNl5qK5q8EhTXdxxLKgQjAFr0NK0ppOpt9n51D2gd2cmsvOElVcvOopr"\
"KvuPtriNzsY8rH+H0ECoQEg4WklY1czP8akZby51p6G3b6QAWBl43llSVTlUfuZE3NmYh9Vl0HkHSuVq4ENFNWFdC+uJ5JI/9/V2Y//rkShA1HF6yk/VxJ0f"\
"07CcgkCB7+fSC8Dzcy7mp4l9/khlUzwecaI9hT+wRrsOISylcsphCFLl1RXIvBMpYDZJrKYRjHELACNEgC/KCQQofWBQ5nuV64UAP8AEfrDrQEiLlJD18+p7"\
"BguwfAoBUmKEsLsAGZSiFWxtgWWP4gGAkuB5YDRWylKAKIDJZBa1H8Kx47C1Cdls7qLnQTZffQ+20lB7EiU1ent7sQBQ6+vdq2PJ5dC9ABW1sJnOQbL5Qc/H"\
"pNOYehf/4lW+jY4vh2tr3fsWafrWzRtlDW5f9aVzjUVj72FmCqzBypBQCKzbjLp8jZUPo7OZyYm7bYkvw/sAAFMd7V3lp5sGqs+fjRcZhVYKY0xupwysfpog"\
"k0jcb5ucffbbKu9Esv1Kl1N2+Ekk5rg2DIXRmog1Jdr3F/Tm5mO0edc6MSP/CvjX+AV0DoH1Z+D54gAAAABJRU5ErkJggg=="

error=\
"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"

password=\
"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"

question=\
"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"

warning=\
"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"

