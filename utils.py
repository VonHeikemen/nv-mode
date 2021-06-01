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
    middle = (len(visible_lines) // 2) - 1
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

class NvPasteAfter(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.run_command('move', {"by": "characters", "forward": True})
    self.view.run_command('paste')

class NvOpenTabList(sublime_plugin.WindowCommand):
  def run(self):
    window = sublime.active_window()
    group = window.views_in_group(window.active_group())
    active_view_id = window.active_view().id()

    result_list = [None]
    groups = [None]

    for (i, view) in enumerate(group, start=1):
      if active_view_id == view.id():
        groups[0] = i - 1
        result_list[0] = self.get_file_info(view, i, True)
      else:
        groups.append(i - 1)
        result_list.append(self.get_file_info(view, i, False))

    def preview(index):
      highlighted = groups[index]
      filename = group[highlighted].file_name()

      if filename:
        window.open_file(filename, sublime.TRANSIENT)
      else:
        window.focus_view(group[highlighted])

    def on_done(index):
      if index == -1:
        current = groups[0]
        window.focus_view(group[current])
      else:
        chosen = groups[index]
        filename = group[chosen].file_name()

        if filename:
          window.open_file(filename, sublime.REPLACE_MRU)
        else:
          window.focus_view(group[chosen])


    window.show_quick_panel(result_list, on_done, on_highlight=preview)

  def get_file_info(self, view, index, current):
    path = view.file_name()

    if path:
      parent, name = self.filepath(path)
    else:
      parent = ''
      name = view.name() or 'untitled'

    if view.is_dirty():
      mark = '+'
    else:
      mark = '-'

    if current:
      name = '[%] {} {}'.format(mark, name)
    else:
      name = '[{}] {} {}'.format(index, mark, name)

    return [name, parent]

  def filepath(self, path):
    folders = sublime.active_window().folders()
    parent, name = os.path.split(path)
    res = []

    if len(folders) > 1:
      for dir in folders:
        if dir not in parent:
          continue

        base, root = os.path.split(dir)
        res.append(os.path.join('/', parent.replace(base, "")))
    else:
        res.append(os.path.join('/', parent.replace(folders[0], "")))

    parent = "\n".join(res)[1:]
    return (parent, name)

