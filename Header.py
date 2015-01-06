
#
# Imports some modules.
#

import sublime, sublime_plugin, os, time, locale, ntpath

#
# Simple class to ask project name.
#

class PromptHeaderCommand(sublime_plugin.WindowCommand):

  def run(self):
    filename = ntpath.basename(self.window.active_view().file_name())
    if (filename.endswith(".c") or filename.endswith(".h")):
      region = self.window.active_view().find("\/\*\n\*\*[\s\S]+for[\s\S]+in[\s\S]+\n\*\* \n\*\* Made by [\s\S]+\n\*\* Login [\s\S]+<[\s\S]+_[\s\S]@epitech.net>\n\*\* \n\*\* Started on[\s\S]+\n\*\* Last update[\s\S]+\n\*\/", 0)
      if (region == None or region == sublime.Region(-1, -1)) :
        label = "Type project name: "
        self.window.show_input_panel(label, "", self.on_done, None, None)
      else:
        self.on_done(None)
    else:
      if (filename == "Makefile"):
        if (region == None or region == sublime.Region(-1, -1)) :
          label = "Type project name: "
          self.window.show_input_panel(label, "", self.on_done, None, None)
        else:
          self.on_done(None)
    self.window.run_command("save")
    pass

  def on_done(self, text):
    try:
      self.window.active_view().run_command("header", {"project": text})
    except ValueError:
      pass

#
# Main class: create the epitech-style header.
#

class HeaderCommand(sublime_plugin.TextCommand):

  #
  # /!\ Find how to get this from system!
  #

  fullname = "Hugo SCHOCH"

  #
  # Get comment type according language.
  #

  def get_comment(self):
    comments = {}

    comments['Default']      = ['  ', '  ', '  ']
    comments['JavaScript']   = ['/**', ' *', ' */']
    comments['CSS']          = ['/**', ' *', ' */']
    comments['C++']          = ['/*', '**', '*/']
    comments['C']          = ['/*', '**', '*/']
    comments['Python']       = ['#', '#', '#']
    comments['CoffeeScript'] = ['#', '#', '#']
    comments['Ruby']         = ['#', '#', '#']
    comments['Makefile']     = ['##', '##', '##']
    comments['Makefile Improved']     = ['##', '##', '##']
    comments['Perl']         = ['#!/usr/local/bin/perl -w', '##', '##']
    comments['ShellScript']  = ['#!/bin/sh', '##', '##']
    comments['HTML']         = ['<!--', ' ', '-->']
    comments['LaTeX']        = ['%%', '%%', '%%']
    comments['Lisp']         = [';;', ';;', ';;']
    comments['Java']         = ['//', '//', '//']
    comments['PHP']          = ['#!/usr/local/bin/php\n<?php', '//', '//']
    comments['Jade']         = ['//-', '//-', '//-']
    comments['Stylus']       = ['//', '//', '//']

    return comments[self.view.settings().get('syntax').split('/')[1]]

  #
  # Get file infos.
  #

  def get_file_infos(self):
    full = self.view.file_name().split('/')
    return [full.pop(), '/'.join(full)]

  #
  # Get email
  #

  def get_mail(self):
    return "<" + os.environ['USER'] + "@epitech.net>"

  def get_file_name(self):
    return ntpath.basename(self.view.file_name())

  #
  # Get date epitech-formated (e.g Thu Jan  3 00:22:41 2013)
  #

  def get_date(self):

    loc = locale.getlocale()
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    date = time.strftime("%a %b  ")
    day = time.strftime("%d").lstrip('0');
    date = date + day + time.strftime(" %H:%M:%S %Y")
    locale.setlocale(locale.LC_ALL, loc)
    return date

  #
  # Generate header.
  #

  def generate(self, project):

    # get some infos
    header = ""
    comment = self.get_comment()
    f = self.get_file_infos()

    # generate the header

    header += comment[0] + '\n'
    header += comment[1] + " " + f[0] + " for " + project + " in " + f[1] + '\n'
    header += comment[1] + " \n"
    header += comment[1] + " Made by " + self.fullname + '\n'
    header += comment[1] + " Login   " + self.get_mail() + '\n'
    header += comment[1] + " \n"
    header += comment[1] + " Started on  " + self.get_date()+ " " + self.fullname + '\n'
    header += comment[1] + " Last update " + self.get_date() + " " + self.fullname + '\n'
    header += comment[2] + '\n'

    return header

  def is_already_here(self):
    file_name = self.get_file_name();
    region_c = self.view.find("\/\*\n\*\*[\s\S]+for[\s\S]+in[\s\S]+\n\*\* \n\*\* Made by [\s\S]+\n\*\* Login [\s\S]+<[\s\S]+_[\s\S]@epitech.net>\n\*\* \n\*\* Started on[\s\S]+\n\*\* Last update[\s\S]+?\n\*\/", 0)
    region_make = self.view.find("##\n## Makefile for[\s\S]+in[\s\S]+\n## \n## Made by [\s\S]+\n## Login[\s\S]+<[\s\S]+_[\s\S]@epitech.net>\n## \n## Started on[\s\S]+\n## Last update [\s\S]+?\n##", 0)
    if (file_name.endswith(".c") or file_name.endswith(".h")):
      if (region_c == None or region_c == sublime.Region(-1, -1)) :
        return 0
      else:
        return 1
    else:
      if (file_name == "Makefile"):
        if (region_make == None or region_make == sublime.Region(-1, -1)) :
          return 0
        else:
          return 1
      else:
        return 0

  def new_date(self):
    header = ""
    comment = self.get_comment()
    header += comment[1] + " Last update " + self.get_date() + " " + self.fullname + '\n'
    header += comment[2]
    return header

  def get_region_update_start(self):
    size = len(self.view.full_line(0) + self.view.full_line(1) + self.view.full_line(2) + self.view.full_line(3) + self.view.full_line(4) + self.view.full_line(5) + self.view.full_line(6))
    return size

  def get_region_update_end(self):
    size = len(self.view.full_line(0) + self.view.full_line(1) + self.view.full_line(2) + self.view.full_line(3) + self.view.full_line(4) + self.view.full_line(5) + self.view.full_line(6) + self.new_date())
    return size
  #
  # Run command.
  #

  def run(self, edit, project):
    new = self.is_already_here()
    file_name = self.get_file_name();
    if (new == 0) :
      self.view.insert(edit, 0, self.generate(project))
    else :
      if (file_name.endswith(".c") or file_name.endswith(".h")):
        self.view.replace(edit, self.view.find("\*\* Last update[\s\S]+?\n\*\/", 0), self.new_date())
      else:
        if (file_name == "Makefile"):
          self.view.replace(edit, self.view.find("## Last update[\s\S]+?\n##", 0), self.new_date())
