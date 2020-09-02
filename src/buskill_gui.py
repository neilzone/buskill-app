#!/usr/bin/env python3.7
"""
::

  File:    buskill_gui.py
  Authors: Michael Altfield <michael@buskill.in>
  Created: 2020-06-23
  Updated: 2020-06-23
  Version: 0.1

This is the code to launch the BusKill GUI app

For more info, see: https://buskill.in/
"""

################################################################################
#                                   IMPORTS                                    #
################################################################################

import buskill
import webbrowser

import kivy
#kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import ObjectProperty

#from kivy.garden.navigationdrawer import NavigationDrawer
from garden.navigationdrawer import NavigationDrawer
#import garden.navigationdrawer

from kivy.core.window import Window
Window.size = ( 300, 500 )

# grey background color
Window.clearcolor = [ 0.188, 0.188, 0.188, 1 ]

from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.core.text import LabelBase

import logging
logger = logging.getLogger( __name__ )

################################################################################
#                                  SETTINGS                                    #
################################################################################

# n/a

################################################################################
#                                   CLASSES                                    #
################################################################################

class MainWindow(BoxLayout):

	toggle_btn = ObjectProperty(None)
	status = ObjectProperty(None)
	menu = ObjectProperty(None)
	actionview = ObjectProperty(None)

	def toggleMenu(self):

		# TODO make this slid-out a menu drawer on the left
		print( 'foo' )
		self.nav_drawer.toggle_state()

	def toggleBusKill(self):

		buskill.toggle()

		if buskill.isArmed():
			self.toggle_btn.text = 'Disarm'
			self.status.text = 'BusKill is currently armed.'
			self.toggle_btn.md_bg_color = [1,0,0,1]
			self.toggle_btn.background_color = self.red_color
			self.actionview.background_color = self.red_color
		else:
			self.toggle_btn.text = 'Arm'
			self.status.text = 'BusKill is currently disarmed.'
			self.toggle_btn.background_color = self.primary_color
			self.actionview.background_color = self.primary_color

class CriticalError(BoxLayout):

	msg = ObjectProperty(None)

	def showError( self, msg ):
		self.msg.text = msg

	def fileBugReport( self ):
		# TODO: make this a redirect on buskill.in so old versions aren't tied
		#       to github.com
		webbrowser.open( 'https://docs.buskill.in/buskill-app/en/stable/support.html' )

class BusKill(App):

	# register font aiases so we don't have to specify their full file path
	# when setting font names in our kivy language .kv files
	LabelBase.register( "Roboto", "fonts/Roboto-Regular.ttf",  )
	LabelBase.register( "RobotoMedium", "fonts/Roboto-Medium.ttf",  )
	LabelBase.register( "mdicons", "fonts/MaterialIcons-Regular.ttf" )

	# does some UI-agnostic buskill initialization stuff
	buskill.init()

	# does rapid-fire UI-agnostic cleanup stuff when the GUI window is closed
	def close( self, *args ):
		buskill.close()

	def build(self):

		# TODO: try to remove this (why is it declared twice?)
		buskill.init()

		# is the OS that we're running on supported?
		if buskill.isPlatformSupported():

			# yes, this platform is supported; show the main window
			Window.bind( on_request_close = self.close )
			return MainWindow()

		else:
			# the current platform isn't supported; show critical error window

			msg = buskill.ERR_PLATFORM_NOT_SUPPORTED
			print( msg ); logging.error( msg )

			crit = CriticalError()
			crit.showError( buskill.ERR_PLATFORM_NOT_SUPPORTED )
			return crit
