# -*- coding:latin-1 -*-

import os, sys, _tkinter
# Tkinter library of python 2.5 is moved to tkinter package in python 2.6+ -> 3.0+
try: import Tkinter
except ImportError: import tkinter as Tkinter

# shortcuts
Tk = Tkinter.Tk
mainloop = Tkinter.mainloop
Toplevel = Tkinter.Toplevel
TclError = Tkinter.TclError

# PIL image increment
_nbPILimg = 0

# return python widget from name
def searchWidget(widget, name):
	for child in widget.children:
		if name.endswith(child):
			return widget.children[child]
		else:
			w = searchWidget(widget.children[child], name)
			if w != False: return w
	return False

# loads Tile package
def loadTile(tk):
	# append "[pyTtk.py path]/tcl" to AUTO_PATH in order to find Tile package here
	ttk_path = os.path.join(os.path.dirname(__file__), "tcl")
	if tk.eval("lsearch auto_path {%s}" % ttk_path) == "-1":
		tk.eval("lappend auto_path {%s}" % ttk_path)
	tk.eval("package require tile")
		
def customize_all_widgets(value):
	TtkWidget.extend = bool(value)

def _style(widget_or_style):
	return Tkinter.BaseWidget.cget(widget_or_style, "style") if isinstance(widget_or_style, Tkinter.BaseWidget) else \
	       widget_or_style

def _img(img, kind="photo", **statespec):
	"""
	This fonction simplify the image definition of widget, img can be
	 - a PIL Tkimage
	 - a tk image name
	 - a base64 string
	 - a pathfile
	 """

	global _nbPILimg

	if hasattr(img, "tk"):
		_nbPILimg = _nbPILimg + 1
		setattr(Tkinter._default_root, "PILimg%03d" % _nbPILimg, img)

	elif isinstance(img, str) and img not in Tkinter._default_root.tk.call("image", "names"):
		img = Tkinter._default_root.tk.call(
			"image", "create", kind,
			"-file" if os.path.lexists(img) else "-data",
			img
		)

	if len(statespec) > 0:
		result = "%s" % _img(img)
		for key,value in statespec.items():
			result += " {%s} %s" % (key, _img(value, kind=kind))
		return result

	else:
		return img

def _cnf(cnf = {}, **kw):
	config = dict(cnf, **kw)
	del cnf, kw

	for key in ["ulabel", "utext"]:
		if key in config:
			text = config.pop(key)
			index = text.find("_")
			if index >= 0 and not text.endswith("_"):
				config[key[1:]] = text[:index] + text[index+1:]
				config["underline"] = index

	for key in ["image", "selectimage", "bitmap"]:
		image = config.pop(key, None)
		if image != None:
			if isinstance(image, tuple) and len(image) == 2:
				config[key] = _img(image[0], kind="photo", **image[-1])
			else:
				config[key] = _img(image, kind="photo" if "image" in key else "bitmap")

	padding = config.pop("padding", None)
	if padding != None:
		if isinstance(padding, int):
			config["padding"] = (padding, ) * 4
		if isinstance(padding, tuple):
			if len(padding) == 2: config["padding"] = padding * 2
			elif len(padding) == 3: config["padding"] = padding + (0, )
			else: config["padding"] = padding

	return config

def _cnfpopstartswith(start, excludes, cnf = {}, **kw):
	new = {}
	for key in [k for k in cnf if k.startswith(start) if k not in excludes]:
		new[key.replace(start, "")] = cnf.pop(key)
	for key in [k for k in kw if k.startswith(start) if k not in excludes]:
		new[key.replace(start, "")] = kw.pop(key)
	return new

def _dict(Tcl_pairs):
	Tcl_pairs = tuple(str(elem)[1:] if isinstance(elem, _tkinter.Tcl_Obj) else elem for elem in Tcl_pairs)
	return dict((Tcl_pairs[i], Tcl_pairs[i+1]) for i in range(0, len(Tcl_pairs), 2))
	
# ==================================================================================================
if sys.version_info[0] >= 3:
	import functools
	reduce = functools.reduce

_convertto =  lambda value, encoding="utf-8": Tkinter._default_root.tk.call("encoding", "convertto", encoding, value)
_options = lambda cnf, **kw: reduce(tuple.__add__, (("-" + k, v) for (k,v) in dict(cnf, **kw).items()))
# http://www.gidhome.com/ManHtml/tcl8.5.1/html/TkCmd/getOpenFile.htm
def getOpenFile(master = None, cnf = {}, encoding="utf-8", **kw):
	return _convertto(Tkinter._default_root.tk.call(("tk_getOpenFile", "-parent", "." if master == None else master) + _options(cnf, **kw)), encoding)
# http://www.gidhome.com/ManHtml/tcl8.5.1/html/TkCmd/getSaveFile.htm
def getSaveFile(master = None, cnf = {}, encoding="utf-8", **kw):
	return _convertto(Tkinter._default_root.tk.call(("tk_getSaveFile", "-parent", "." if master == None else master) + _options(cnf, **kw)), encoding)
# http://www.gidhome.com/ManHtml/tcl8.5.1/html/TkCmd/chooseDirectory.htm
def getFolder(master = None, cnf = {}, encoding="utf-8", **kw):
	return _convertto(Tkinter._default_root.tk.call(("tk_chooseDirectory", "-parent", "." if master == None else master) + _options(cnf, **kw)), encoding)
# http://www.gidhome.com/ManHtml/tcl8.5.1/html/TkCmd/chooseColor.htm
def getColor(master = None, cnf = {}, **kw):
	return Tkinter._default_root.tk.call(("tk_chooseColor", "-parent", "." if master == None else master) + _options(cnf, **kw))

# ==================================================================================================
class Style:
	"""
	Each widget is assigned a style, which specifies the set of elements making
	up the widget and how they are arranged, along with dynamic and default settings
	for element options. By default, the style name is the same as the widget's class;
	this may be overridden by the -style option.
	"""
	theme_use = lambda self, themename=None: self.tk.call("ttk::style", "theme", "use", themename)
	theme_names = lambda self: self.tk.call("ttk::style", "theme", "names")
	element_options = lambda self, element: self.tk.call("ttk::style", "element", "options", element)
	element_names = lambda self: self.tk.call("ttk::style", "element", "names")
# ==================================================================================================
	def __init__(self, master = None):


		if Tkinter._support_default_root:
			if not master:
				if not Tkinter._default_root:
					Tkinter._default_root = Tk()
				master = Tkinter._default_root
		else:
			master = Tk()

		self.master = master
		self.tk = master.tk

		if not "Ttk" in self.tk.eval("package names"):
			loadTile(self.tk)

	def style_configure(self, widget_or_style, cnf = {}, **kw):
		items = _cnf(cnf, **kw).items()
		style = _style(widget_or_style)

		if not len(items):
			return self.tk.call("ttk::style", "configure", style)

		options = ()
		for key, value in items:
			options += ('-' + (key[:-1] if key[-1] == '_' else key), self._register(value) if hasattr(value, '__call__') else value)
		self.tk.call(("ttk::style", "configure", style) + options)
	configure = style_configure

	def style_map(self, widget_or_style, cnf = {}, **kw):
		items = _cnf(cnf, **kw).items()
		style = _style(widget_or_style)

		options = ()
		for option, statespec_value in items:
			list_ = ""
			if type(statespec_value) == type({}):
				for state in statespec_value:
					list_ += "{%s} %s " % (state, statespec_value[state])
				options += ("-" + option, list_)

		self.tk.call(("ttk::style", "map", style,) + options)
	map = style_map

	def style_lookup(self, widget_or_style, option, states = None):
		return self.tk.call("ttk::style", "lookup", _style(widget_or_style), "-" + option, None if not states else "{%s}" % states)
	lookup = style_lookup

	def style_layout(self, widget_or_style, layout_spec = None):
		return self.tk.call("ttk::style", "layout", _style(widget_or_style), layout_spec)
	layout = style_layout

	def style_element_create(self, name, img, statespec={}, **options):
		tupple_options = ()
		for key, value in options.items(): tupple_options += ("-" + key , value)
		return self.tk.call(("ttk::style", "element", "create", name, "image", _img(img, **statespec)) + tupple_options)
	element_create = style_element_create

# TODO if really needed

# ttk::style theme create themeName ?-parent basedon? ?-settings script... ?
# Creates a new theme. It is an error if themeName already exists. If -parent is
# specified, the new theme will inherit styles, elements, and layouts from the
# parent theme basedon. If -settings is present, script is evaluated in the context
# of the new theme as per ttk::style theme settings.

# ttk::style theme settings themeName script
# Temporarily sets the current theme to themeName, evaluate script, then restore
# the previous theme. Typically script simply defines styles and elements, though
# arbitrary Tcl code may appear.


# ==================================================================================================
class Menu(Tkinter.Menu):
	_nbPILimg = 0
# ==================================================================================================
	def __init__(self, master = None, cnf = {}, **kw):
		Tkinter.Menu.__init__(self, master, cnf, **kw)

		if not "Ttk" in self.tk.eval("package names"):
			loadTile(self.tk)

	# Tile does not provide Menu widgets. This function is created to allow the new
	# options and ways to manage images.
	def fix_options(self, cnf = {}, **kw):
		return self._options(_cnf(cnf, **kw))
	# easier ways to insert, add and modify menu items
	def add(self, item, cnf = {}, **kw): return self.tk.call((self._w, "add", item) + self.fix_options(cnf, **kw))
	def insert(self, index, item, cnf = {}, **kw): return self.tk.call((self._w, "insert", index, item) + self.fix_options(cnf, **kw))
	def entryconfigure(self, index, cnf = {}, **kw): return self.tk.call((self._w, 'entryconfigure', index) + self.fix_options(cnf, **kw))
	def clone(self, master = None, name = None, cloneType = "normal"):
		name = "clony" + self._w if name == None else name
		name = (self._w if master == None else master._w) + "." + name
		self.tk.call(self._w, "clone", name, cloneType)
		return name
# ==================================================================================================

# ==================================================================================================
class TtkWidget(Tkinter.BaseWidget):
	"""
	"""
	extend = True
	# __names__ = {}
# ==================================================================================================
	def __init__(self, master, widgetName, cnf = {}, kw = {}, extra = ()):
		"""
		"""
		config = dict(cnf, **kw)
		self.extend = bool(config.pop("extend", True))
		Tkinter.BaseWidget._setup(self, master, config)

		# load Tile if not already loaded
		if not "Ttk" in self.tk.eval("package names"):
			loadTile(self.tk)

		# here is a fix for panedwindow widget because of its readonly attribute -orient !
		if "orient" in config.keys():
			self.tk.call(("ttk::" + widgetName, self._w, "-orient", config.pop("orient")) + extra)
		else:
			self.tk.call(("ttk::" + widgetName, self._w) + extra)

		classes = []
		for key in [k for k in config.keys() if isinstance(k, type)]:
			classes.append((key, config.pop(key)))

		# if user does not give explicitly a style (and implicitly wants to extend the widget)
		# we create a style based on widget name to allow customisation of this and only this widget.
		if self.extend and "style" not in config and widgetName not in ["scrollbar", "scale", "panedwindow", "progressbar"]:
			config["style"] = self._name + "." + "T" + widgetName.capitalize()

		# configure widget with given options
		self.configure(config)

		for key, value in classes:
			key.configure(self, value)

	def configure(self, cnf = {}, **kw):
		items = _cnf(cnf, **kw).items()

		if not len(items): 
			return dict([elem[0][1:],str(elem[-1])] for elem in self.tk.call(self._w, "configure"))

		# list of widget options != style options
		widget_keys = list(self.keys())

		# builds tupple for widget configuration
		widget_options = ()
		for key, value in [item for item in items if item[0] in widget_keys]:
			widget_options += (
				'-' + (key[:-1] if key[-1] == '_' else key),
				self._register(value) if hasattr(value, '__call__') else value
			)
		self.tk.call((self._w, "configure") + widget_options)

		# appends other options given in cnf and **kw and uses 'ttk::style configure' command.
		# if user explicitly gived a style on initialisation it will affect all widgets of the
		# same style...
		if self.extend:
			widget_style = ()
			for key, value in [item for item in items if item[0] not in widget_keys]:
				widget_style += (
					'-' + (key[:-1] if key[-1] == '_' else key),
					self._register(value) if hasattr(value, '__call__') else value
				)
			self.tk.call(("ttk::style", "configure", self["style"]) + widget_style)

	__setitem__ = lambda self, item, value: self.configure(**{item : value})
	config = configure

	def cget(self, item):
		result = self.tk.call("ttk::style", "lookup", Tkinter.BaseWidget.cget(self,"style"), "-" + item, self.state())
		if result == "":
			try:    result = Tkinter.BaseWidget.cget(self,item)
			except: return None
		return result
	__getitem__ = cget
# ==================================================================================================

# ==================================================================================================
class Widget(TtkWidget, Tkinter.Pack, Tkinter.Place, Tkinter.Grid):
	"""
	"""
	widgetName = None
# ==================================================================================================
	def __init__(self, master = None, cnf = {}, **kw):
		TtkWidget.__init__(self, master, self.widgetName, cnf, kw)

	def identify(self, x, y):
		"""
		Returns the name of the element at position x, y, or the empty
		string if the point does not lie within any element.
		x and y are pixel coordinates relative to the widget.
		"""
		return self.tk.call(self._w, "identify", x, y)

	def instate(self, state, command = None, *args):
		"""
		Test the widget's state. Returns 1 if the widget state matches
		statespec and 0 otherwise.
		"""
		if command: return self.tk.call(self._w, 'instate', state, command, args)
		else: return self.tk.call(self._w, 'instate', state)

	def state(self,state = None):
		"""
		Modify or inquire widget state. Returns a new state spec indicating
		which flags were changed.
		"""
		if state: self.tk.call(self._w, 'state', state)
		else: return self.tk.call(self._w, 'state')

	def grid(self, *args, **kwargs):
		Tkinter.Grid.grid(self, *args, **kwargs)
		return self

	def pack(self, *args, **kwargs):
		Tkinter.Pack.pack(self, *args, **kwargs)
		return self

	def place(self, *args, **kwargs):
		Tkinter.Place.place(self, *args, **kwargs)
		return self
# ==================================================================================================

# ==================================================================================================
class Button(Widget, Tkinter.Button):
	"""
	A button widget displays a textual label and/or image, and evaluates
	a command when pressed.
	"""
	widgetName = "button"
# ==================================================================================================
# ==================================================================================================
class Menubutton(Widget, Tkinter.Menubutton):
	"""
	A menubutton widget displays a textual label and/or image,
	and displays a menu when pressed.
	"""
	widgetName = "menubutton"
	menu = None
# ==================================================================================================
	def __call__(self): return self.menu

	def menu_insert(self, item, index = 0, cnf = {}, **kw):
		if not self.menu:
			self.menu = Menu(self)
			self["menu"] = self.menu
		self.menu.insert(index, item, cnf, **kw)

	def menu_add(self, item, cnf = {}, **kw):
		if not self.menu:
			self.menu = Menu(self)
			self["menu"] = self.menu
		self.menu.add(item, cnf, **kw)

	def menu_modify(self, index, cnf, **kw):
		if self.menu: self.menu.entryconfigure(index, cnf, **kw)

	def menu_option(self, index, option):
		if self.menu: self.menu.entrycget(index, option)

	def menu_delete(self, index1, index2 = None):
		if self.menu: self.menu.delete(index1, index2)

	def menu_configure(self, cnf = {}, **kw):
		if self.menu: return self.menu.configure(cnf, **kw)
# ==================================================================================================
# ==================================================================================================
class Checkbutton(Widget, Tkinter.Checkbutton):
	"""
	A checkbutton widget is used to show or change a setting. It has
	two states, selected and deselected. The state of the checkbuton
	may be linked to a Tcl variable.
	"""
	widgetName = "checkbutton"
# ==================================================================================================
# ==================================================================================================
class Radiobutton(Widget, Tkinter.Radiobutton):
	"""
	Radiobutton widgets are used in groups to show or change a set of
	mutually - exclusive options. Radiobuttons are linked to a Tcl
	variable, and have an associated value; when a radiobutton is clicked,
	it sets the variable to its associated value.
	"""
	widgetName = "radiobutton"
# ==================================================================================================
# ==================================================================================================
class Label(Widget, Tkinter.Label):
	"""
	A label widget displays a textual label and/or image. The label may
	be linked to a Tcl variable to automatically change the displayed text.
	"""
	widgetName = "label"
# ==================================================================================================
# ==================================================================================================
class Scale(Widget, Tkinter.Scale):
	"""
	"""
	widgetName = "scale"
# ==================================================================================================
# ==================================================================================================
class Separator(Widget):
	"""
	A separator widget displays a horizontal or vertical separator bar
	"""
	widgetName = "separator"
# ==================================================================================================
# ==================================================================================================
class Sizegrip(Widget):
	"""
	A sizegrip widget (also known as a grow box) allows the user to resize
	the containing toplevel window by pressing and dragging the grip.
	"""
	widgetName = "sizegrip"
# ==================================================================================================
# ==================================================================================================
class Frame(Widget, Tkinter.Frame):
	"""
	A frame widget is a container, used to group other widgets together.
	"""
	widgetName = "frame"
# ==================================================================================================
# ==================================================================================================
class Labelframe(Widget, Tkinter.LabelFrame):
	"""
	A container used to group other widgets together. It has an optional label,
	which may be a plain text string or another widget.
	"""
	widgetName = "labelframe"
	labelkeys  = ["labelanchor", "labelwidget", "labelmargins", "labeloutside"]
# ==================================================================================================
	def configure(self, cnf = {}, **kw):
		label_cnf = _cnfpopstartswith("label", self.labelkeys, cnf, **kw)
		Widget.configure(self, cnf, **kw)
		self.tk.call(("ttk::style", "configure", self["style"] + ".Label") + self._options(label_cnf))

	def cget(self, item):
		if item.startswith("label") and item not in self.labelkeys:
			result = self.tk.call("ttk::style", "lookup", Widget.cget(self,"style") + ".Label", "-" + item.replace("label", ""))
		else:
			result = self.tk.call("ttk::style", "lookup", Widget.cget(self,"style"), "-" + item, self.state())
		if result == "":
			try:    result = Widget.cget(self,item)
			except: return None
		return result
	__getitem__ = cget
# ==================================================================================================
class Entry(Widget, Tkinter.Entry):
	"""
	An entry widget displays a one-line text string and allows that
	string to be edited by the user. The value of the string may be
	linked to a Tcl variable with the -textvariable option. Entry
	widgets support horizontal scrolling with the standard -xscrollcommand
	option and xview widget command.
	"""
	widgetName="entry"
# ==================================================================================================
# ==================================================================================================
class Combobox(Entry):
	"""
	A combobox combines a text field with a pop-down list of values;
	the user may select the value of the text field from among the
	values in the list.
	"""
	widgetName = "combobox"
# 	==================================================================================================
	def configure(self, cnf = {}, **kw):
		list_cnf = _cnfpopstartswith("list", [], cnf, **kw)

		Widget.configure(self, cnf, **kw)
		for option, value in list_cnf.items():
			self.tk.call("option", "add", "*%s*Listbox.%s" % (self._name, option), value)

	def get(self):
		"""
		Returns the current value of the combobox.
		"""
		return self.tk.call(self._w, 'get')

	def current(self,index=None):
		"""
		If index is supplied, sets the combobox value to the element at
		position index in the list of values. Otherwise, returns the index
		of the current value in the list of values or -1 if the current
		value does not appear in the list.
		"""
		return self.tk.call(self._w, 'current', index)

	def set(self, value):
		"""
		Sets the value of the combobox to value.
		"""
		self.tk.call(self._w, 'set', value)
# ==================================================================================================
# ==================================================================================================
class Scrollbar(Widget, Tkinter.Scrollbar):
	"""
	Scrollbar widgets are typically linked to an associated window
	that displays a document of some sort, such as a file being edited
	or a drawing. A scrollbar displays a thumb in the middle portion
	of the scrollbar, whose position and size provides information about
	the portion of the document visible in the associated window. The thumb
	may be dragged by the user to control the visible region. Depending
	on the theme, two or more arrow buttons may also be present; these are
	used to scroll the visible region in discrete units.
	"""
	widgetName="scrollbar"
# ==================================================================================================
	def configure(self, cnf={}, **kw):
		config = dict(cnf, **kw)
		self.__target = config.pop("target", False)
		Tkinter.Scrollbar.configure(self, **config)

		if self.__target:
			if not isinstance(self.__target, Tkinter.BaseWidget):
				self.__target = searchWidget(self.winfo_toplevel(), self.__target)
				if not self.__target:
					raise TclError('Could not find scrolltarget for "%s" widget' % self)
					return
			try:
				if str(self["orient"]) == "horizontal":
					Tkinter.Scrollbar.configure(self, command=self.__target.xview)
					self.__target["xscrollcommand"] = self.set
				elif str(self["orient"]) == "vertical":
					Tkinter.Scrollbar.configure(self, command=self.__target.yview)
					self.__target["yscrollcommand"] = self.set
			except:
				raise TclError('"%s" is not a scrollable widget' % self.__target)
# ==================================================================================================
# ==================================================================================================
class Autoscrollbar(Scrollbar):
	"""
	A scrollbar that hides itself if it's not needed.
	"""
# ==================================================================================================
	def grid(self, *args, **kw):
		self.__layout = Scrollbar.grid
		self.__layout_remove = Scrollbar.grid_forget
		self.__layout_args = args
		self.__layout_kw = kw
		self.__layout(self, *self.__layout_args, **self.__layout_kw)
		return self

	def pack(self, *args, **kw):
		self.__layout = Scrollbar.pack
		self.__layout_remove = Scrollbar.pack_forget
		self.__layout_args = args
		self.__layout_kw = kw
		self.__layout(self, *self.__layout_args, **self.__layout_kw)
		return self

	def place(self, *args, **kw):
		self.__layout = Scrollbar.place
		self.__layout_remove = Scrollbar.place_forget
		self.__layout_args = args
		self.__layout_kw = kw
		self.__layout(self, *self.__layout_args, **self.__layout_kw)
		return self

	def set(self, lo ,hi):
		if float(lo) <= 0.0 and float(hi) >= 1.0:
			self.__layout_remove(self)
		else:
			self.__layout(self, *self.__layout_args, **self.__layout_kw)
		return Scrollbar.set(self, lo, hi)
# ==================================================================================================
# ==================================================================================================
class Progressbar(Widget):
	"""
	A progress bar widget shows the status of a long-running operation.
	They can operate in two modes: determinate mode shows the amount
	completed relative to the total amount of work to be done, and
	indeterminate mode provides an animated display to let the user
	know that something is happening.
	"""
	widgetName="progressbar"
# ==================================================================================================
	def start(self, interval=50):
		"""
		Begin autoincrement mode: schedules a recurring timer event that
		calls step every interval milliseconds. If omitted, interval
		defaults to 50 milliseconds (20 steps/second).
		"""
		self.tk.call(self._w, 'start', interval)
		self.update()

	def stop(self):
		"""
		Stop autoincrement mode: cancels any recurring timer event initiated
		by self.start.
		"""
		self.tk.call(self._w, 'stop')
		self.update()

	def step(self, amount):
		"""
		Increments the value by amount. amount defaults to 1.0 if omitted.
		"""
		self.tk.call(self._w, 'step', amount)
		self.update()
# ==================================================================================================

# ==================================================================================================
class Notebook(Widget):
	"""
	A notebook widget manages a collection of subpanes and displays
	a single one at a time. Each pane is associated with a tab,
	which the user may select to change the currently-displayed pane.

	List of available tab options :
	text      : Specifies a string to be displayed in the tab.
	sticky    : Specifies how the child pane is positioned within the
	            pane area. Value is a string containing zero or more of
	            the characters n, s, e, or w. Each letter refers to a
	            side (north, south, east, or west) that the child window
	            will "stick" to, as per the grid geometry manager.
	compound  : Specifies how to display the image relative to the text,
	            in the case both -text and -image are present.
	underline : Specifies the integer index (0-based) of a character to
	            underline in the text string. The underlined character is
	            used for mnemonic activation if ttk::notebook::enableTraversal
	            is called.
	image     : Specifies an image to display in the tab, which must have
	            been created with the image create command.
	"""
	widgetName="notebook"
	tabkeys = ["tabposition", "tabmargins"]
# ==================================================================================================
	def configure(self, cnf = {}, **kw):
		tab_cnf = _cnfpopstartswith("tab", self.tabkeys, cnf, **kw)

		Widget.configure(self, cnf, **kw)
		self.tk.call(("ttk::style", "configure", self["style"] + ".Tab") + self._options(tab_cnf))

	def insert(self, pos, pane, **options):
		"""
		Inserts a pane at the specified position. pos is either the string end,
		an integer index, or the name of a managed subwindow. If subwindow is
		already managed by the notebook, moves it to the specified position.
		"""
		tabid = self.tk.call(self._w, "insert", pos, pane)
		self.tab(pane, **options)
		return tabid

	def add(self, child, **options):
		"""
		Adds a new tab to the notebook. When the tab is selected, the child
		window will be displayed. child must be a direct child of the
		notebook window.
		"""
		return self.tk.call((self._w, 'add', child) + self._options(_cnf(options)))

	def tab(self, child, option = None, **options):
		"""
		Query or modify the options of the specific tab. If no option is specified,
		returns a dictionary of the tab option values. If one option is specified,
		returns the value of that option. Otherwise, sets the options to the
		corresponding values.
		"""
		if option: return self.tk.call(self._w, "tab", child, "-" + option)
		elif len(options): self.tk.call((self._w,"tab", child) + self._options(_cnf(options)))
		else: return self.tk.call(self._w, "tab", child)

	def index(self, tabid):
		"""
		Returns the numeric index of the tab specified by tabid, or the
		total number of tabs if tabid is the string "end".
		"""
		return self.tk.call(self._w, "index", tabid)

	def tabs(self):
		"""
		Returns a list of all windows managed by the widget.
		"""
		return self.tk.call(self._w, "tabs")

	def hide(self, tabid):
		"""
		Hides the tab specified by tabid. The tab will not be displayed,
		but the associated window remains managed by the notebook and
		its configuration remembered. Hidden tabs may be restored with
		the add command.
		"""
		self.tk.call(self._w, "hide", tabid)

	def forget(self, tabid):
		"""
		Removes the tab specified by tabid, unmaps and unmanages the
		associated child window.
		"""
		self.tk.call(self._w, "forget", tabid)

	def select(self, tabid = None):
		"""
		Selects the specified tab. The associated child pane will be displayed,
		and the previously-selected pane (if different) is unmapped. If tabid
		is omitted, returns the widget name of the currently selected pane.
		"""
		return self.tk.call(self._w, "select", tabid)

	def enableTraversal(self): self.tk.call('ttk::notebook::enableTraversal', self._w)
# ==================================================================================================

# ==================================================================================================
class Paned(Widget):
	"""
	A paned widget displays a number of subwindows, stacked either
	vertically or horizontally. The user may adjust the relative
	sizes of the subwindows by dragging the sash between panes.
	"""
	widgetName="panedwindow"
# ==================================================================================================
	def insert(self, pos, pane, **options):
		"""
		Inserts a pane at the specified position. pos is either the string end,
		an integer index, or the name of a managed subwindow. If subwindow
		is already managed by the paned window, moves it to the specified
		position.
		"""
		self.tk.call((self._w, "insert", pos, pane) + self._options(_cnf(options)))

	def add(self, pane, **options):
		"""
		Adds a new pane to the window. subwindow must be a direct child
		of the paned window pathname.
		"""
		return self.tk.call((self._w, "add", pane) + self._options(_cnf(options)))

	def forget(self, pane):
		"""
		Removes the specified subpane from the widget. pane is either
		an integer index or the name of a managed subwindow.
		"""
		self.tk.call(self._w, "forget", pane)

	def pane(self, pane, option = None, **options):
		"""
		Query or modify the options of the specified pane, where pane is
		either an integer index or the name of a managed subwindow. If no
		-option is specified, returns a dictionary of the pane option values.
		If one -option is specified, returns the value of that option.
		Otherwise, sets the -options to the corresponding values.
		"""
		if option: return self.tk.call(self._w, "pane", pane, "-" + option)
		elif len(options): self.tk.call((self._w, "pane", pane) + self._options(_cnf(options)))
		else: return self.tk.call(self._w, "pane", pane)

	def panes(self):
		"""
		Returns the list of all windows managed by the widget.
		"""
		return self.tk.call(self._w, "panes")

	def sashpos(self, index = 0, newpos = None):
		"""If newpos is specified, sets the position of sash number index.
		May adjust the positions of adjacent sashes to ensure that positions
		are monotonically increasing. Sash positions are further constrained
		to be between 0 and the total size of the widget. Returns the new
		position of sash number index.
		"""
		if newpos != None: return self.tk.call(self._w, "sashpos", index, newpos)
		else: return self.tk.call(self._w, "sashpos", index)
# ==================================================================================================

# ==================================================================================================
class Tree(Widget):
	"""
	This widget displays a hierarchical collection of items. Each item has a textual
	label, an optional image, and an optional list of data values. The data values
	are displayed in successive columns after the tree label.

	The order in which data values are displayed may be controlled by setting the
	displaycolumns widget option. The tree widget can also display column headings.
	Columns may be accessed by number or by symbolic names listed in the columns widget
	option (see COLUMN IDENTIFIERS).

	Each item is identified by a unique name. The widget will generate item IDs if
	they are not supplied by the caller. There is a distinguished root item, named {}.
	The root item itself is not displayed; its children appear at the top level of the
	hierarchy.

	Each item also has a list of tags, which can be used to associate event bindings
	with individual items and control the appearance of the item.

	Treeview widgets support horizontal and vertical scrolling with the standard
	[xy]scrollcommand options and [xy]view widget commands.

	columns        : A list of column identifiers, specifying the number of columns and
	                 their names.
	displaycolumns : A list of column identifiers (either symbolic names or integer
	                 indices) specifying which data columns are displayed and the
	                 order in which they appear, or the string #all. If set to #all
	                 (the default), all columns are shown in the order given.
	height         : Specifies the number of rows which should be visible.
	                 -Note- the requested width is determined from the sum of the column widths.
	padding        : Specifies the internal padding for the widget. The padding is a
	                 list of up to four length specifications (see Ttk_GetPaddingFromObj()).
	selectmode     : Controls how the built-in class bindings manage the selection. One of
	                 extended, browse, or none.
                     If set to extended (the default), multiple items may be selected. If browse,
                     only a single item will be selected at a time. If none, the selection will
                     not be changed.
                     Note that application code and tag bindings can set the selection
                     however they wish, regardless of the value of -selectmode.

	show           : A list containing zero or more of the following values, specifying
	                 which elements of the tree to display.
                    - tree - Display tree labels in column #0. (default)
                    - headings - Display the heading row.

	NOTE: Column #0 always refers to the tree column, even if -show tree is not specified.
	"""
	widgetName="treeview"
	# pathname configure ?option? ?value option value ...? [OK] from master class
	# pathname cget option [OK] from master class
	# pathname state ?stateSpec?  [OK] from master class
	# pathname instate statespec ?script?  [OK] from master class
# ==================================================================================================
	__iter__ = lambda self: self.walk("")

	def __init__(self, master = None, cnf = {}, **kw):
		cnf = dict(cnf, **kw)
		cnf["style"] = "Treeview"
		Widget.__init__(self, master, cnf)

	def font(self, item):
		for tag in self.item(item, "tags"):
			font = self.tag_configure(tag, "font")
			if font != "": break
		return "TkDefaultFont" if font == "" else font

	def find_withtag(self, tag):
		return tuple(item for item in self if tag in self.item(item, "tags"))

	def walk(self, item):
		for child in self.tk.call(self._w, "children", item):
			yield child
			for elem in self.walk(child):
				yield elem

	# pathname bbox item ?column? [OK]
	def bbox(self, item, column=None):
		return self.tk.call(self._w, "bbox", item, column)

	# pathname children item ?newchildren? [OK] --> TODO get better name
	def xchildren(self, item="", newchildren=None):
		return self.tk.call(self._w, "children", item, newchildren)

	# pathname column column ?-option ?value -option value...? [OK]
	# COLUMN OPTIONS : id, anchor, minwidth, stretch, width
	def column(self, column, option = None, **options):
		if option: return self.tk.call(self._w, "column", column, "-" + option)
		elif len(options): self.tk.call((self._w, "column", column) + self._options(_cnf(options)))
		else: return self.tk.call(self._w, "column", column)

	# pathname delete itemList [OK]
	def delete(self, *itemlist):
		return self.tk.call(self._w, "delete", " ".join(itemlist))

	# pathname detach itemList [OK]
	def detach(self, *itemlist):
		return self.tk.call(self._w, "detach", " ".join(itemlist))

	# pathname exists item [OK]
	def exists(self, item):
		return self.tk.call(self._w, "exists", item)

	# pathname focus ?item? [X] can get current focus but can not set it
	def focus(self, item = None):
		return self.tk.call(self._w, "focus", item)

	# pathname heading column ?-option ?value -option value...? [OK]
	# HEADING OPTIONS : text, image, anchor, command
	def heading(self, heading="#0", option = None, **options):
		if option: return self.tk.call(self._w, "heading", heading, "-" + option)
		elif len(options): self.tk.call((self._w, "heading", heading) + self._options(_cnf(options)))
		else: return self.tk.call(self._w, "heading", heading)

	# pathname identify row x y
	# pathname identify column x y
	def identify(self, what="row", x=0, y=0):
		return self.tk.call(self._w, "identify", what, x, y)

	# pathname index item [OK]
	def index(self, item = None):
		return self.tk.call(self._w, "index", item)

	# pathname insert parent index ?-id id? options... [OK]
	# ITEM OPTIONS : text, image, values, open, tags
	def insert(self, parent = "", index = "end", cnf = {}, **kw):
		return self.tk.call((self._w, "insert", parent, index, ) + self._options(_cnf(cnf, **kw)))

	# pathname item item ?-option ?value -option value...? [OK]
	# ITEM OPTIONS : text, image, values, open, tags
	def item(self, item, option = None, **options):
		if option: return self.tk.call(self._w, "item", item, "-" + option)
		elif len(options): self.tk.call((self._w, "item", item) + self._options(_cnf(options)))
		else: return _dict(self.tk.call(self._w, "item", item))

	# pathname move item parent index [OK]
	def move(self, item, parent, index):
		return self.tk.call(self._w, "move", item, parent, index)

	# pathname next item [OK]
	def next(self, item):
		return self.tk.call(self._w, "next", item)

	# pathname parent item [OK]
	def parent(self, item):
		return self.tk.call(self._w, "parent", item)

	# pathname prev item [OK]
	def prev(self, item):
		return self.tk.call(self._w, "prev", item)

	# pathname see item [OK]
	def see(self, item):
		return self.tk.call(self._w, "see", item)

	# pathname selection ?selop itemList? [OK]
		# pathname selection set itemList
		# pathname selection add itemList
		# pathname selection remove itemList
		# pathname selection toggle itemList
	def selection(self, operation=None, *itemlist):
		if operation and len(itemlist): self.tk.call(self._w, "selection", operation, " ".join(itemlist))
		else: return self.tk.call(self._w, "selection")

	# pathname set item ?column? ?value? [OK]
	def set(self, item, column = None, value = None):
		if column == None and value == None: return _dict(self.tk.call(self._w, "set", item))
		else: return self.tk.call(self._w, "set", item, column, value)

	# pathName tag args... [OK]
	# TAG OPTIONS : foreground, background, font, image
	def tag_configure(self, tagname, option = None, **options):
		if option: return self.tk.call(self._w, "tag", "configure", tagname, "-" + option)
		elif len(options): self.tk.call((self._w, "tag", "configure", tagname) + self._options(_cnf(options)))
		else: return self.tk.call(self._w, "tag", "configure", tagname)

	# pathName tag has tagName ?item?
# 	def tag_has(self, tagname, item = None):
# 		if item: self.tk.call(self._w, "tag", "has", tagname, item)
# 		else: self.tk.call(self._w, "tag", "has", tagname)

		# pathName tag configure tagName ?option? ?value option value...?
		# pathName tag names
		# pathName tag add tag items
		# pathName tag remove tag ?items?

	# pathName tag bind tagName ?sequence? ?script?
	def tag_bind(self, tagname, sequence, command):
		cmd = self._register(command)
		self.tk.call(self._w, "tag", "bind", tagname, sequence, cmd)
		return cmd

	# pathName xview args [OK]
	def xview(self, *args):
		return self.tk.call((self._w, "xview",) + args)

	# pathName yview args [OK]
	def yview(self, *args):
		return self.tk.call((self._w, "yview",) + args)
