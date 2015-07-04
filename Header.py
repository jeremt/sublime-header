
#
# Imports some modules.
#

import sublime, sublime_plugin, os, time, locale, ntpath, re
from subprocess import call

#
# Simple class to ask project name.
#

class PromptHeaderCommand(sublime_plugin.WindowCommand):

	def	run(self):
		settings = sublime.load_settings('sublime-header.sublime-settings')
		syntax = self.get_syntax()
		disallowed = settings.get("disallowed_languages")
		allowed = settings.get("allowed_languages")
		if (disallowed and len(disallowed) and syntax in disallowed) or (allowed and len(allowed) and not syntax in allowed):
			self.window.run_command("save")
			return
		filename = ntpath.basename(self.window.active_view().file_name())
		regex = self.get_regex_request()
		region = self.window.active_view().find(self.get_regex_request(), 0)
		if (region == None or region == sublime.Region(-1, -1)) :
			label = "Type project name: "
			self.window.show_input_panel(label, "", self.on_done, None, None)
		else:
			self.on_done(None)
		self.window.run_command("save")

	def	get_syntax(self):
		rawSyntax = self.window.active_view().settings().get("syntax")
		rawTab = rawSyntax.split("/")
		if (len(rawTab)):
			rawSubTab = rawTab[(len(rawTab) - 1)].split(".")
			if (len(rawSubTab)):
				rawSecondSubTab = rawSubTab[0].split(" ")
				if (len(rawSecondSubTab)):
					language = rawSecondSubTab[0];
					return language
		return rawSyntax

	def	get_regex_request(self):
		regex = "[\s\S]*for[\s\S]*in[\s\S]*Made by[\s\S]"
		regex += "[\s\S]*Login	 <[\s\S]*>[\s\S]"
		regex += "[\s\S]*Started on	[\s\S]*Last update	[\s\S]*"
		return regex

	def	on_done(self, text):
		try:
			self.window.active_view().run_command("header", {"project": text})
		except ValueError:
			pass

#
# Main class: create the epitech-style header.
#

class HeaderCommand(sublime_plugin.TextCommand):

	#
	# Get comment type according language.
	#

	def	get_syntax(self):
		rawSyntax = self.view.settings().get("syntax")
		rawTab = rawSyntax.split("/")
		if (len(rawTab)):
			rawSubTab = rawTab[(len(rawTab) - 1)].split(".")
			if (len(rawSubTab)):
				rawSecondSubTab = rawSubTab[0].split(" ")
				if (len(rawSecondSubTab)):
					language = rawSecondSubTab[0];
					return language
		return rawSyntax

	def	get_comment(self):
		syntax = self.get_syntax()

		comments = {}

		comments['Default']				= ['	', '	', '	']
		comments['JavaScript']			= ['/**', ' *', ' */']
		comments['CSS']					= ['/**', ' *', ' */']
		comments['C++']					= ['//', '//', '//']
		comments['C']					= ['/*', '**', '*/']
		comments['Python']				= ['#', '#', '#']
		comments['CoffeeScript']		= ['#', '#', '#']
		comments['Ruby']				= ['#', '#', '#']
		comments['Makefile']			= ['##', '##', '##']
		comments['Makefile Improved']	= ['##', '##', '##']
		comments['Perl']				= ['#!/usr/local/bin/perl -w', '##', '##']
		comments['ShellScript']			= ['#!/bin/sh', '##', '##']
		comments['HTML']				= ['<!--', ' ', '-->']
		comments['LaTeX']				= ['%%', '%%', '%%']
		comments['Lisp']				= [';;', ';;', ';;']
		comments['Java']				= ['//', '//', '//']
		comments['PHP']					= ['#!/usr/local/bin/php\n<?php', '//', '//']
		comments['Jade']				= ['//-', '//-', '//-']
		comments['Stylus']				= ['//', '//', '//']

		if syntax in comments:
			return comments[syntax]
		else:
			return comments["Default"]

	#
	# Get file infos.
	#

	def	get_file_infos(self):
		full = self.view.file_name().split('/')
		return [full.pop(), '/'.join(full)]

	#
	# Get email
	#

	def	get_mail(self):
		mail = self.settings.get("mail")
		if (not mail):
			return "<" + os.environ['USER'] + "@epitech.net>"
		else:
			return "<" + mail + ">"

	def	get_name(self):
		name = self.settings.get("name")
		if (not name):
			name = os.popen("cat /etc/passwd | grep " + os.environ['USER'] + " | cut -d: -f5 | cut -d, -f1").read()
			res = name.replace('\n', '')
		else:
			res = name
		return res

	def	get_file_name(self):
		return ntpath.basename(self.view.file_name())

	#
	# Get date epitech-formated (e.g Thu Jan	3 00:22:41 2013)
	#

	def	get_date(self):
		loc = locale.getlocale()
		locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
		date = time.strftime("%a %b	")
		day = time.strftime("%d").lstrip('0');
		date = date + day + time.strftime(" %H:%M:%S %Y")
		locale.setlocale(locale.LC_ALL, loc)
		return date

	#
	# Generate header.
	#

	def	get_regex_request(self, update = False):
		regex = "[\s\S]*for[\s\S]*in[\s\S]*Made by[\s\S]"
		regex += "[\s\S]*Login	 <[\s\S]*>[\s\S]"
		regex += "[\s\S]*Started on	[\s\S]"
		regex += "[\s\S]*Last update	[\s\S]*"
		update = " Last update	[\s\S]*?\n"
		if (update):
			comments = self.get_comment()
			update = re.escape(comments[1]) + update + re.escape(comments[2])
			return update
		return regex

	def	generate(self, project):

		# get some infos
		if (not project):
			project = ""
		header = ""
		comment = self.get_comment()
		f = self.get_file_infos()

		# generate the header

		header += comment[0] + '\n'
		header += comment[1] + " " + f[0] + " for " + project + " in " + f[1] + '\n'
		header += comment[1] + " \n"
		header += comment[1] + " Made by " + self.get_name() + '\n'
		header += comment[1] + " Login	 " + self.get_mail() + '\n'
		header += comment[1] + " \n"
		header += comment[1] + " Started on	" + self.get_date()+ " " + self.get_name() + '\n'
		header += comment[1] + " Last update	" + self.get_date() + " " + self.get_name() + '\n'
		header += comment[2] + '\n'

		return header

	def	is_already_here(self):
		regex = self.get_regex_request(True)
		region = self.view.find(regex, 0)
		if (region == None or region == sublime.Region(-1, -1)) :
			return False
		else:
			return True

	def	new_date(self):
		header = ""
		comment = self.get_comment()
		header += comment[1] + " Last update	" + self.get_date() + " " + self.get_name() + '\n'
		header += comment[2]
		return header

	def	get_region_update_start(self):
		size = len(self.view.full_line(0) + self.view.full_line(1) + self.view.full_line(2) + self.view.full_line(3) + self.view.full_line(4) + self.view.full_line(5) + self.view.full_line(6))
		return size

	def	get_region_update_end(self):
		size = len(self.view.full_line(0) + self.view.full_line(1) + self.view.full_line(2) + self.view.full_line(3) + self.view.full_line(4) + self.view.full_line(5) + self.view.full_line(6) + self.new_date())
		return size
	#
	# Run command.
	#

	def	run(self, edit, project):
		self.settings = sublime.load_settings('sublime-header.sublime-settings')
		old = self.is_already_here()
		file_name = self.get_file_name();
		if (old) :
			regex = self.get_regex_request(True)
			region = self.view.find(regex, 0)
			self.view.replace(edit, region, self.new_date())
		else :
			self.view.insert(edit, 0, self.generate(project))
