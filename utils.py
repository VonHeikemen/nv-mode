import os

import sublime
import sublime_plugin

def get_visible_lines(view):
  current_view = view.visible_region()
  return view.lines(current_view)

def goto_line(view, line,**kwargs):
  extend = kwargs.get('extend', False)
  col = kwargs.get('col', 0)

  selection = view.sel()[0]
  row, _ = view.rowcol(line.a)
  point = view.text_point(row, col)
  destination = sublime.Region(point)

  view.sel().clear()

  if extend:
    new_region = sublime.Region(selection.a, destination.end())
    view.sel().add(new_region)
  else:
    view.sel().add(destination)
    view.show(destination, False)

class NvMoveToBottomCommand(sublime_plugin.TextCommand):
  def run(self, edit, **kwargs):
    extend=kwargs.get('extend', False)
    visible_lines = get_visible_lines(self.view)
    last_line = visible_lines[-1]

    goto_line(self.view, last_line, extend=extend)

class NvMoveToTopCommand(sublime_plugin.TextCommand):
  def run(self, edit, **kwargs):
    extend=kwargs.get('extend', False)
    visible_lines = get_visible_lines(self.view)
    first_line = visible_lines[0]

    goto_line(self.view, first_line, extend=extend)

class NvMoveToMiddleCommand(sublime_plugin.TextCommand):
  def run(self, edit, **kwargs):
    extend=kwargs.get('extend', False)
    visible_lines = get_visible_lines(self.view)
    middle = (len(visible_lines) // 2)
    middle_line = visible_lines[middle]

    goto_line(self.view, middle_line, extend=extend)

class NvMoveHalfPageUp(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.run_command('nv_move_to_top')
    self.view.run_command('show_at_center')

class NvMoveHalfPageDown(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.run_command('nv_move_to_bottom')
    self.view.run_command('show_at_center')

class NvMoveToFirstCharInLine(sublime_plugin.TextCommand):
  def run(self, edit, **kwargs):
    extend=kwargs.get('extend', False)
    current_line = self.view.line(self.view.sel()[0])
    line_str = self.view.substr(current_line)
    diff = len(line_str) - len(line_str.lstrip())

    goto_line(self.view, current_line, col=diff, extend=extend)

class NvMoveToLastCharInLine(sublime_plugin.TextCommand):
  def run(self, edit, **kwargs):
    extend=kwargs.get('extend', False)
    current_line = self.view.line(self.view.sel()[0])
    line_str = self.view.substr(current_line)
    diff = len(line_str) - len(line_str.rstrip())
    _, column = self.view.rowcol(current_line.b - diff)

    goto_line(self.view, current_line, col=column, extend=extend)

class NvPasteAfter(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.run_command('move', {"by": "characters", "forward": True})
    self.view.run_command('paste')

class NvOpenTabList(sublime_plugin.WindowCommand):
  def run(self):
    window = sublime.active_window()
    group = window.views_in_group(window.active_group())
    active_view_id = window.active_view().id()
    result_list = [self.get_file_info(view, active_view_id, i) for (i, view) in enumerate(group, start=1)]

    def on_done(index):
      if index == -1:
        return

      window.focus_view(group[index])

    window.show_quick_panel(result_list, on_done)

  def get_file_info(self, view, current_view, index):
    path = view.file_name()

    if path:
      parent, name = os.path.split(path)
      parent = os.path.basename(parent)
    else:
      parent = ''
      name = view.name() or 'untitled'

    if view.id() == current_view:
      name = '~ {}'.format(name)
    else:
      name = '[{}] - {}'.format(index, name)

    if view.is_dirty():
      name += ' *'

    return [name, parent]
