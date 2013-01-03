
import sublime, sublime_plugin, os, time, locale

class HeaderCommand(sublime_plugin.TextCommand):

  #
  # /!\ Find how to get this!
  #

  fullname = "jeremie taboada-alvarez"

  #
  # Get comment type according language.
  #

  def get_comment(self):
    comments = {}

    comments['Default']      = ['  ', '  ', '  ']
    comments['JavaScript']   = ['/**', ' *', ' */']
    comments['C++']          = ['/*', '**', '*/']
    comments['Python']       = ['#', '#', '#']
    comments['CoffeeScript'] = ['#', '#', '#']

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

  def get_date(self4):
    return time.strftime("%a %b  %d %H:%M:%S %Y") # find how to get en_US datetime

  #
  # Generate header.
  #

  def generate(self):
    header = ""
    comment = self.get_comment()
    f = self.get_file_infos()
    project = "" # from input

    print self.get_date()

    header += comment[0] + '\n'
    header += comment[1] + " " + f[0] + " for " + project + " in " + f[1] + '\n'
    header += comment[1] + '\n'
    header += comment[1] + " Made by " + self.fullname + '\n'
    header += comment[1] + " Login   " + self.get_mail() + '\n'
    header += comment[1] + '\n'
    header += comment[1] + " Started on  " + self.get_date() + " " + self.fullname + '\n'
    header += comment[1] + " Last update " + self.get_date() + " " + self.fullname + '\n'
    header += comment[2] + '\n'
    header += '\n'

    return header

  #
  # Run command.
  #

  def run(self, edit):
    self.view.insert(edit, 0, self.generate())
