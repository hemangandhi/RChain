TtkWidget class is the core of the yawTtk package. It loads Tile and
override configure function to manage both widget options and style
options.

Support this project
====================

.. image:: http://bruno.thoorens.free.fr/img/gratipay.png
   :target: https://gratipay.com/yawttk

---

.. image:: http://bruno.thoorens.free.fr/img/bitcoin.png

3Jgib9SQiDLYML7QKBYtJUkHq2nyG6Z63D

Extend
------

A yawTtk widget extends TtkWidget and can be configured mostly as a
Tkinter widget if its extend option is True. There are two ways to 
disable this feature :

>>> # for all widgets
>>> customize_all_widgets(False)
>>> # or
>>> # for a single widget on its creation
>>> button = Button(extend = False, text = "Simple button")

Configure 
--------- 

In Tile, widget options and style are separated. yawTtk merges them to
simplify and match as possible Tkinter way of coding. Remember that it is
only available if extend option is True. configure funcion is called 
by __init__ and __setattr__ class method so there are 3
different ways to configure widgets.

>>> # configure widget with __init__ function
>>> button = Button(
... style = "custom.Toolbutton",
... anchor = "center",
... font = ("Tahoma", "8", "bold"),
... )
>>> # or with __setattr__ function
>>> button["foreground"] = "steelblue3"
>>> button["background"] = "lightgreen"
>>> # or even with configure function
>>> button.configure(
... command = exit,
... text = "Toolbutton",
... padding = (5, 1, 5, 1)
... )
>>> # pack and see...
>>> button.pack(fill = "x", padx = 5, pady = 5)

.. image:: http://bruno.thoorens.free.fr/yawttk/wiki/images/steelblue_button.png

In this example, widget style is explicitly defined. If it is not, yawTtk
gives one according to widget type and name. Next example shows different
possibilities of style determination by yawTtk. Notice that name
option is not necessary because of automatic naming in Tkinter.

>>> b1 = Button(extend = False, text = "Button 1", name = "button001")
>>> # style widget is "TButton"
>>> b2 = Button(extend = False, text = "Button 2", name = "button002", style = "custom.TButton")
>>> # style widget is "custom.TButton"
>>> b3 = Button(extend = True, text = "Button 3", name = "button003")
>>> # style widget is "button003.TButton"
>>> b4 = Button(extend = True, text = "Button 4", name = "button004", style = "TButton")
>>> # style widget is "TButton"


* b1 and b2 can only be configured with ttk::style configure command
* b3 and b4 can configure themselves with __setattr__ and configure functions
* b1 and b4 are default button i.e. modifications affect all buttons

Limitations 
----------- 

There are many themes defined in tile (or Tk 8.5). The winnative and xpnative  ones 
do not allow modification for all widget options. Just see the example below :

>>> # other way to configure widget is to give a dictionary...
>>> cnf = dict(
... # relief is not supported in "xpnative" and "winnative" theme
... relief = "solid",
... # options supported by all theme
... anchor = "center",
... font = ("Tahoma", "8", "bold"),
... foreground = "steelblue3",
... background = "lightgreen",
... command = exit,
... text = "Flat button",
... padding = (5, 1, 5, 1)
... )

For each theme fo Tile :

>>> Button(None, cnf).pack(fill = "x", padx = 5, pady = 5)

Windows themes :

.. image:: http://bruno.thoorens.free.fr/yawttk/wiki/images/winnative_flatbutton.png
.. image:: http://bruno.thoorens.free.fr/yawttk/wiki/images/xpnative_flatbutton.png

Other themes :

.. image:: http://bruno.thoorens.free.fr/yawttk/wiki/images/default_flatbutton.png
.. image:: http://bruno.thoorens.free.fr/yawttk/wiki/images/alt_flatbutton.png
.. image:: http://bruno.thoorens.free.fr/yawttk/wiki/images/clam_flatbutton.png
.. image:: http://bruno.thoorens.free.fr/yawttk/wiki/images/classic_flatbutton.png



