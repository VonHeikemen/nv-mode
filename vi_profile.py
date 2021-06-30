import sublime
import sublime_plugin

def normal_mode(view):
  view.settings().set('command_mode', True)
  view.settings().set('visual_mode', False)
  view.set_status('mode', 'COMMAND MODE')

  change_caret = view.settings().get('nv_change_caret_style_in_command_mode')
  highlight_line = view.settings().get('nv_toggle_hightlight_line_on_command_mode')

  if change_caret:
    view.settings().set('inverse_caret_state', True)

  if highlight_line:
    view.settings().set('highlight_line', True)

def exit_normal_mode(view):
  view.settings().set('command_mode', False)
  view.settings().set('visual_mode', False)
  view.settings().set('inverse_caret_state', False)

  disable_highlight = view.settings().get(
    'nv_toggle_hightlight_line_on_command_mode'
  )

  if disable_highlight:
    view.settings().set('highlight_line', False)

def clear_selection(view):
  for sel in view.sel():
    new_region = sublime.Region(sel.b, sel.b)
    view.sel().subtract(sel)
    view.sel().add(new_region)

class NvEnterInsertMode(sublime_plugin.TextCommand):
  def run(self, edit, **kwargs):
    insert_newline = kwargs.get('below', False)
    insert_after = kwargs.get('after', False)

    if insert_newline:
      self.view.run_command('move_to', {"to": "eol"})
      self.view.run_command('insert', {"characters": "\n"})

    if insert_after:
      self.view.run_command('move', {"by": "characters", "forward": True})

    self.view.set_status('mode', 'INSERT MODE')
    exit_normal_mode(self.view)

class NvEnterNormalMode(sublime_plugin.TextCommand):
  def run(self, edit):
    if self.view.has_non_empty_selection_region():
      clear_selection(self.view)

    normal_mode(self.view)

class NvEnterVisualMode(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.settings().set('visual_mode', True)
    self.view.set_status('mode', 'VISUAL MODE')

class NvDisableAndExit(sublime_plugin.ApplicationCommand):
  def run(self):
    name = 'NvMode'
    settings = sublime.load_settings('Preferences.sublime-settings')
    ignored_packages = settings.get('ignored_packages', [])

    ignored_packages.append(name)
    ignored_packages.sort()
    settings.set('ignored_packages', ignored_packages)
    sublime.save_settings('Preferences.sublime-settings')
    sublime.status_message('{} Package disabled'.format(name))

    plugin_unloaded()
    sublime.active_window().run_command('exit')

class NvStateTracker(sublime_plugin.EventListener):
  def on_load(self, view):
    normal_mode(view)

  def on_new(self, view):
    self.on_load(view)

  def on_clone(self, view):
    self.on_load(view)


def plugin_loaded():
  for w in sublime.windows():
    for v in w.views():
      normal_mode(v)

def plugin_unloaded():
  for w in sublime.windows():
    for v in w.views():
      exit_normal_mode(v)
      v.erase_status('mode')

