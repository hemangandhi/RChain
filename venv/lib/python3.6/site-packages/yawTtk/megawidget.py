# -*- encoding:latin-1 -*-

'''
Copyright® 2010, THOORENS Bruno
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.
* Neither the name of the *Pytools* nor the names of its contributors may be
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
'''
from . import Frame, Button, Label, Entry, StringVar, Tree
import sys, calendar, datetime
from time import strptime

class Scrolledframe(Frame):

	W = H = w = h = 1
	x1, y1, x2, y2 = 0, 0, 0, 0
	xscrollincrement = yscrollincrement = 5
	xscrollcommand = lambda obj, *args, **kw: None
	yscrollcommand = lambda obj, *args, **kw: None

	lowx = property(lambda obj: abs(obj.x1/obj.w), None, None, "")
	highx = property(lambda obj: abs(obj.x2/obj.w), None, None, "")
	lowy = property(lambda obj: abs(obj.y1/obj.h), None, None, "")
	highy = property(lambda obj: abs(obj.y2/obj.h), None, None, "")

	def __getitem__(self, item):
		if item == "xview": return self.xview
		elif item == "yview": return self.yview
		else: return Frame.__getitem__(self, item)

	def __setitem__(self, item, value):
		if item in ["xscrollcommand", "yscrollcommand"]: setattr(self, item, value)
		else: return Frame.__setitem__(self, item, value)

	def __call__(self):
		return self.content

	def __init__(self, master=None, cnf={}, **kw):
		config = dict(cnf, **kw)
		self.stretch = config.pop("stretch", False)
		Frame.__init__(self, master, padding=config.pop("padding", 0), border=config.pop("border", 0), relief=config.pop("relief", "flat"), **config)
		self.placer = Frame(self, padding=0, border=0, relief="flat", **config)
		self.placer.pack(fill="both", expand=True)
		self.content = Frame(self.placer, padding=0, border=0, relief="flat", **config)
		if sys.platform.startswith("win"):
			self.placer.bind("<Configure>", self.update_scrollregion)
		else:
			self.placer.bind("<Expose>", self.update_scrollregion)
		self.placer.update_scrollregion = self.content.update_scrollregion = self.update_scrollregion

	def add(self, widget, cnf={}, **kw):
		return widget(self.content, cnf, **kw)

	def update_scrollregion(self, *args):
		if not len(self.content.children):
			self.xscrollcommand(0., 1.)
			self.yscrollcommand(0., 1.)
			return

		x1,y1,x2,y2 = [int(str(e)) for e in self["padding"]]
		self.w, self.W = float(self.tk.call("winfo", "reqwidth", self.content._w)), float(self.tk.call("winfo", "width", self._w)-x1-x2)
		self.h, self.H = float(self.tk.call("winfo", "reqheight", self.content._w)), float(self.tk.call("winfo", "height", self._w)-y1-y2)

		if self.lowx <= 0.: self.x1 = 0.
		if self.highx >= 1.: self.x1 = min(0., self.W-self.w)
		self.x2 = self.W - self.x1

		if self.lowy <= 0.: self.y1 = 0.
		if self.highy >= 1.: self.y1 = min(0., self.H-self.h)
		self.y2= self.H - self.y1

		self.tk.call(
			"place", "configure", self.content._w, "-anchor", "nw",
			"-x", self.x1, "-width", max(self.W, self.w) if self.stretch else self.w, 
			"-y", self.y1, "-height", max(self.H, self.h) if self.stretch else self.h
		)
		self.xscrollcommand(self.lowx, self.highx)
		self.yscrollcommand(self.lowy, self.highy)

	def xview(self, event, value, units='pages'):
		value = 0. if self.W > self.w else float(value)
		maxratio = abs(self.W-self.w)/self.w
		x1 = self.x1

		if event == "moveto":
			x1 = 0 if value<=0.0 else self.W-self.w if value>=maxratio else -self.w*value
		elif event == "scroll":
			x1 -= value*self.xscrollincrement if units == "units" else value*self.W*0.99
			x1 = self.W-self.w if x1 < self.W-self.w else 0 if x1>0 else x1
		else: raise

		self.x1 = x1
		self.x2 = self.W - self.x1
		self.tk.call("place", "configure", self.content._w, "-anchor", "nw", "-x", self.x1, "-width", self.w)
		return self.xscrollcommand(self.lowx, self.highx)

	def yview(self, event, value, units='pages'):
		value = 0. if self.H > self.h else float(value)
		maxratio = abs(self.H-self.h)/self.h
		y1 = self.y1

		if event == "moveto":
			y1 = 0 if value<=0.0 else self.H-self.h if value>=maxratio else -self.h*value
		elif event == "scroll":
			y1 -= value*self.yscrollincrement if units == "units" else value*self.H*0.99
			y1 = self.H-self.h if y1 < self.H-self.h else 0 if y1>0 else y1
		else: raise

		self.y1 = y1
		self.y2= self.H - self.y1
		self.tk.call("place", "configure", self.content._w, "-anchor", "nw", "-y", self.y1, "-height", self.h)
		return self.yscrollcommand(self.lowy, self.highy)

# ==================================================================================================
class CalendarFrame(Frame):
	"""
	"""

	_calendar = calendar.Calendar()

	# icon set
	backward = \
	"R0lGODlhEAAQAOMMAAwMDBwbHBscHC4vLy8vL0RERFtbW3Nzc3NzdHR0c4yLjIyMi////////////////yH5BAEKAA8ALAAAAAAQABAAAAQo8MlJq7046z0X"\
	"VVoyIYdmSEaqFU/hshkhEYOcCVOAZwDVc8CgcBiMAAA7"
	foreward = \
	"R0lGODlhEAAQAOMNAAwMDBsbHBwbHBscGy4uLy4vLi8vL0RERFtbW1tcXHNzc3RzdIyMjP///////////yH5BAEKAA8ALAAAAAAQABAAAAQo8MlJq7046z0Z"\
	"9ZmiTIuGnFKiHezxuBlhGFKhCcE0aADVc8CgcBiMAAA7"
	left = \
	"R0lGODlhEAAQAOMMAA0NDR4eHx8fHzQzMzQzNDM0NEtLS0xLS2VlZX+Af4CAf5qZmv///////////////yH5BAEKAA8ALAAAAAAQABAAAAQf8MlJq704630X"\
	"l4nyISR3HIbxEUPxPYHwPsBs33j+RAA7"
	right = \
	"R0lGODlhEAAQAOMNAA4NDh8eHh8eHzQ0MzQ0NExLS0xLTEtMS0xMTGVlZYB/f3+AgJqamv///////////yH5BAEKAA8ALAAAAAAQABAAAAQf8MlJq704600Z"\
	"n8ryPUn5HQVicAQxfEIwAmNt33gWAQA7"

	# return current date
	get = lambda self: self.date
	more_one_year = lambda self: self.fill(datetime.date(self.date.year +1, self.date.month, self.date.day))
	minus_one_year = lambda self: self.fill(datetime.date(self.date.year -1 , self.date.month, self.date.day))
# ==================================================================================================
	getvalue = lambda self: str(self.date)
	getformatedvalue = lambda self: self.date.strftime(self.format)
	def __init__(self, master = None, cnf = {}, **kw):
		cnf = dict( cnf, **kw)
		# search for a date - format definition in cnf or in kw
		# %a Locale's abbreviated weekday name
		# %A Locale's full weekday name
		# %b Locale's abbreviated month name
		# %B Locale's full month name
		# %c Locale's appropriate date and time representation
		# %d Day of the month as a decimal number [01,31]
		# %j Day of the year as a decimal number [001,366]
		# %m Month as a decimal number [01,12]
		# %x Locale's appropriate date representation
		# %y Year without century as a decimal number [00,99]
		# %Y Year with century as a decimal number
		self.format = cnf.pop("format") if "format" in cnf else "%x"
		# search for a week day definition
		self.days = cnf.pop("days") if "days" in cnf else list(["lu", "ma", "me", "je", "ve", "sa", "di"])
		# search for date
		self.date = cnf.pop("date") if "date" in cnf else datetime.date.today()

		Frame.__init__(self, master, cnf)
		self.columnconfigure(2, weight = 1)
		self.rowconfigure(1, weight = 1)

		self.var = StringVar(self)
		self.content = Frame(self, padding = 0, border = 0)
		self.content.rowconfigure(0, weight = 0)
		self.content.grid(row = 1, column = 0, sticky = "new", columnspan = 5)

		# here the head User Interface with arrow button and date entry
		# for time navigation
		action_button_cnf = {
			"style": "action.Toolbutton",
			"width": -1,
			"padding": (2,0),
			"anchor": "center",
			"font": ("tahoma", "8", "bold"),
			"background": self["background"]
		}
		Button(self, action_button_cnf, takefocus = False, image = CalendarFrame.backward, command = self.minus_one_year).grid(row = 0, column = 0, sticky = "nesw")
		Button(self, action_button_cnf, takefocus = False, image = CalendarFrame.left, command = self.minus_one_month) .grid(row = 0, column = 1, sticky = "nesw")
		self.entry = Entry(self, textvariable = self.var, justify = "center", width = 0, padding = (1, 0))
		self.entry.grid(row = 0, column = 2, sticky = "nesw", padx = 3, pady = 3)
		self.entry.bind("<FocusOut>", self.set_date)
		Button(self, action_button_cnf, takefocus = False, image = CalendarFrame.right, command = self.more_one_month) .grid(row = 0, column = 3, sticky = "nesw")
		Button(self, action_button_cnf, takefocus = False, image = CalendarFrame.foreward, command = self.more_one_year).grid(row = 0, column = 4, sticky = "nesw")

		days_cnf = {
			"pqdding": 0,
			"anchor": "center",
			"width": 0,
			"font": ("tahoma", "8", "bold")
		}
		for day in self.days[:-2]:
			column = self.days.index(day)
			Label(self.content, days_cnf, text = day).grid(row = 0, column = column, sticky = "nesw")
			self.content.columnconfigure(column, minsize = 26)
		for day in self.days[-2:]:
			column = self.days.index(day)
			Label(self.content, days_cnf, text = day, background = "SystemHighlight").grid(row = 0, column = column, sticky = "nesw")
			self.content.columnconfigure(column, minsize = 26)

		# fill the dalendar at the current date
		self.fill(self.date)

	def set_date(self, *args):
		try:
			year, month, day = strptime(self.entry.get(), self.format)[:3]
			self.fill(datetime.date(year, month, day))
			self.entry["foreground"] = "black"
		except:
			self.entry["foreground"] = "red"

	def more_one_month(self):
		month, year = (1, self.date.year +1) if self.date.month == 12 else (self.date.month +1, self.date.year)
		try:
			self.fill(datetime.date(year, month, self.date.day))
		except ValueError:
			self.fill(datetime.date(year, month, self.date.day - 3))

	def minus_one_month(self):
		month, year = (12, self.date.year -1) if self.date.month == 1 else (self.date.month -1, self.date.year)
		try:
			self.fill(datetime.date(year, month, self.date.day))
		except ValueError:
			self.fill(datetime.date(year, month, self.date.day - 3))

	def clear(self):
		self.entry.delete(0, "end")
		columns, rows = self.content.grid_size()
		for row in range(1, rows):
			for widget in self.content.grid_slaves(row = row):
				widget.destroy()

	def fill(self, date, end = False):
		self.entry["foreground"] = "black"
		self.clear()
		self.date = date

		year = self.date.year
		month = self.date.month
		day = self.date.day
		self.entry.delete(0, "end")
		self.entry.insert(0, self.date.strftime(self.format))

		row = 0
		for num, column in CalendarFrame._calendar.itermonthdays2(year, month):
			row += 1 if column == 0 else 0
			config = {"width": -1, "padding": (0,-2), "anchor": "center", "takefocus": False}

			if column < 5: config.update(background = "SystemButtonFace", foreground = "SystemButtonText", style = "custom.TButton")
			else:          config.update(background = "SystemHighlight", style = "weekend.TButton")

			if num == day: config.update(text = num, style = "custom.TLabel", font = ("tahoma", "7", "bold"))
			elif num == 0: config.update(text = "", style = "custom.TLabel", font = ("tahoma", "7")) #, command = lambda arg = num: self.fill(datetime.date(year, month, arg)))
			else:          config.update(text = num, command = lambda arg = num: self.fill(datetime.date(year, month, arg), True))

			(Button if num != 0 else Label)(self.content, config).grid(row = row, column = column, sticky = "nsew")
			self.content.rowconfigure(row, minsize = 18)

		if row <= 5:
			for j in range(row, 6):
				self.content.rowconfigure(j+1, minsize = 18)
				for i in range(7):
					Label(
						self.content,
						background = "SystemButtonFace" if i < 5 else "SystemHighlight",
						foreground = "SystemButtonText" if i < 5 else "SystemHighlightText",
						padding = (0,-2)
					).grid(row = j+1, column = i, sticky = "nesw")

		if end and self.winfo_toplevel().overrideredirect():
			self.winfo_toplevel().withdraw()


class SQLiteView(Tree):

	def __init__(self, parent=None, cnf={}, **kw):
		self.__cursor = kw.pop("sqlite_cursor", None)
		Tree.__init__(self, parent, cnf, **kw)
		self.tag_configure("even", background="lavender")
		self.__sort_meaning = True
		self.__table_name = ""

	def populate(self, tablename, order_by=[], asc=None, **kw):
		if not self.__cursor: return

		if asc != None: self.__sort_meaning = bool(asc)
		else: self.__sort_meaning = not self.__sort_meaning

		# get table column names
		headers = [r[1] for r in self.__cursor.execute("PRAGMA table_info(%s);" % tablename).fetchall()]

		data = self.__cursor.execute('SELECT * FROM "%s" ORDER BY "%s" %s;' % (tablename, '","'.join(k for k in order_by if k in headers), "ASC" if self.__sort_meaning else "DESC")).fetchall() if len(order_by) else \
		       self.__cursor.execute('SELECT * FROM "%s";' % (tablename,)).fetchall()

		# clear data
		self.delete(*self.xchildren())

		# redefine headers if needed
		if self.__table_name != tablename:
			self['columns'] = " ".join(["{%s}"%h for h in headers])
			for i in range(len(headers)):
				text = headers[i]
				self.heading("#%d"%(i+1), text=text, command=lambda o=self,t=tablename,k=text,kw=kw: o.populate(t,[k],**kw))
				self.column("#%d"%(i+1), **kw)
			self.__table_name = tablename

		# populate data
		even=False
		for row in data:
			self.insert(value=tuple(row), tags=("even",) if even else ())
			even = not even

		self.update()
