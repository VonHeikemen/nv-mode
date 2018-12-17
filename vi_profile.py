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

def clear_selection(view):
  selection = view.sel()[0].end() - 1
  new_region = sublime.Region(selection, selection)
  view.sel().clear()
  view.sel().add(new_region)

class NvEnterInsertMode(sublime_plugin.TextCommand):
  def run(self, edit, **kwargs):
    insert_newline = kwargs.get('below', False)
    insert_after = kwargs.get('after', False)
    toggle_highlight_line = self.view.settings().get(
      'nv_toggle_hightlight_line_on_command_mode'
    )

    if insert_newline:
      self.view.run_command('move_to', {"to": "eol"})
      self.view.run_command('insert', {"characters": "\n"})

    if insert_after:
      self.view.run_command('move', {"by": "characters", "forward": True})
    
    self.view.settings().set('command_mode', False)
    self.view.settings().set('visual_mode', False)
    self.view.settings().set('inverse_caret_state', False)
    self.view.set_status('mode', 'INSERT MODE')

    if toggle_highlight_line:
      self.view.settings().set('highlight_line', False)

class NvEnterNormalMode(sublime_plugin.TextCommand):
  def run(self, edit):
    if self.view.has_non_empty_selection_region():
      clear_selection(self.view)

    normal_mode(self.view)

class NvEnterVisualMode(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.settings().set('visual_mode', True)
    self.view.set_status('mode', 'VISUAL MODE')

class NvInputStateTracker(sublime_plugin.EventListener):
  def __init__(self):
    for w in sublime.windows():
      for v in w.views():
        normal_mode(v)

  def on_load(self, view):
    normal_mode(view)

  def on_new(self, view):
    self.on_load(view)

  def on_clone(self, view):
    self.on_load(view)

  def on_selection_modified(self, view):
    is_command_mode = view.settings().get('command_mode')

    if is_command_mode and view.has_non_empty_selection_region():
      view.run_command('nv_enter_visual_mode')


# Called when the plugin is unloaded (e.g., perhaps it just got added to
# ignored_packages). Ensure files aren't left in command mode.
def unload_handler():
  for w in sublime.windows():
    for v in w.views():
      v.settings().set('command_mode', False)
      v.settings().set('visual_mode', False)
      v.settings().set('inverse_caret_state', False) 
      v.erase_status('mode')
