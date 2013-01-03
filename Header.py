
#
# Imports some modules.
#

import sublime, sublime_plugin, os, time, locale

#
# Simple class to ask project name.
#

class PromptHeaderCommand(sublime_plugin.WindowCommand):

  def run(self):
    label = "Type project name: "
    self.window.show_input_panel(label, "", self.on_done, None, None)
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

  fullname = "jeremie taboada-alvarez"

  #
  # Get comment type according language.
  #

  def get_comment(self):
    comments = {}

    comments['Default']      = ['  ', '  ', '  ']
    comments['JavaScript']   = ['/**', ' *', ' */']
    comments['CSS']          = ['/**', ' *', ' */']
    comments['C++']          = ['/*', '**', '*/']
    comments['Python']       = ['#', '#', '#']
    comments['CoffeeScript'] = ['#', '#', '#']
    comments['Ruby']         = ['#', '#', '#']
    comments['Makefile']     = ['##', '##', '##']
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

  #
  # Get date epitech-formated (e.g Thu Jan  3 00:22:41 2013)
  #

  def get_date(self):

    # TODO:
    # - replace 03 by  3
    # - get day and month in english

    return time.strftime("%a %b  %d %H:%M:%S %Y")

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
    header += comment[1] + '\n'
    header += comment[1] + " Made by " + self.fullname + '\n'
    header += comment[1] + " Login   " + self.get_mail() + '\n'
    header += comment[1] + '\n'
    header += comment[1] + " Started on  " + self.get_date() + " " + self.fullname + '\n'
    header += comment[1] + " Last update " + self.get_date() + " " + self.fullname + '\n'
    header += comment[2] + '\n'

    return header

  #
  # Run command.
  #

  def run(self, edit, project):
    self.view.insert(edit, 0, self.generate(project))
