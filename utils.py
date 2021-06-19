import os

import sublime
import sublime_plugin

def get_visible_lines(view):
  current_view = view.visible_region()
  return view.lines(current_view)

def move_to(view, **kwargs):
  line = kwargs.get('line')
  sel = kwargs.get('selection')
  extend = kwargs.get('extend', False)
  col = kwargs.get('col', 0)

  row, _ = view.rowcol(line.a)
  point = view.text_point(row, col)
  destination = sublime.Region(point)

  if extend:
    new_region = sublime.Region(sel.a, destination.end())
    return new_region
  else:
    return destination


def goto_line(view, line, **kwargs):
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
    middle = len(visible_lines) // 2
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
    newones = []

    for sel in self.view.sel():
      cursor_pos = sel.b
      current_line = self.view.line(sublime.Region(cursor_pos, cursor_pos))
      line_str = self.view.substr(current_line)
      diff = len(line_str) - len(line_str.lstrip())

      new_region = move_to(self.view, selection=sel, line=current_line, col=diff, extend=extend)
      newones.append(new_region)

    self.view.sel().clear()
    self.view.sel().add_all(newones)

    # Make sublime choose which cursor will show
    self.view.run_command("move", {"by": "characters", "forward": False})
    # Go back to the original position
    self.view.run_command("move", {"by": "characters", "forward": True})


class NvMoveToLastCharInLine(sublime_plugin.TextCommand):
  def run(self, edit, **kwargs):
    extend=kwargs.get('extend', False)
    newones = []

    for sel in self.view.sel():
      cursor_pos = sel.b
      current_line = self.view.line(sublime.Region(cursor_pos, cursor_pos))
      line_str = self.view.substr(current_line)
      diff = len(line_str) - len(line_str.rstrip())
      _, column = self.view.rowcol(current_line.b - diff)

      new_region = move_to(self.view, selection=sel, line=current_line, col=column, extend=extend)
      newones.append(new_region)

    self.view.sel().clear()
    self.view.sel().add_all(newones)

    # Make sublime choose which cursor will show
    self.view.run_command("move", {"by": "characters", "forward": False})
    # Go back to the original position
    self.view.run_command("move", {"by": "characters", "forward": True})


class NvPasteAfter(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.run_command('move', {"by": "characters", "forward": True})
    self.view.run_command('paste')

