# NvMode - Not VIM Mode

An aggresive keymap configuration inspired by VIM.

## What this plugin is not

It is not meant to be a complete VIM emulation layer. You will not get composable commands, fancy text objects, macros, a vimrc... none of that.

I also will not be implementing more custom commands for this plugin.

## What this plugin is meant to do

Take advantage of the `command_mode` setting to enable a basic modal editing experience. `command_mode` is a built-in feature of sublime, while is active it disables the default key bindings of every key that inserts text in the file. This way we can reuse these keys to execute commands that make it easier to navigate throught the code.

But of course `command_mode` will be useless if we don't have any commands, so I took inspiration from VIM and setup some bindings based on their approach. The idea is to have some VIM inspired shortcuts bound to built-in commands from sublime text (with a few exceptions).

## Getting Started

### Installation
#### Recommended

Install `NvMode` via Package Control.

1. Open the Command Palette via <kbd>Ctrl</kbd>/<kbd>⌘</kbd>+<kbd>Shift</kbd>+<kbd>p</kbd>
2. Select *Package Control: Add Repository*
3. Copy the link of this repository on the input
4. Open the Command Palette again, then select *Package Control: Install Package*
5. Search for `NvMode` and press <kbd>↲ Enter</kbd>

#### Manual

1. Clone or download this repository, (re)name the folder to `NvMode` if necessary.
2. Move the folder inside your sublime `/Packages`. (*Preferences > Browse Packages...*)

## Configuration

There are a few features which are optional so I offer some configuration settings so you can enable them at will.

* `nv_mode_enable_ctrl_w`

The default is `false`. This one enables "window commands" that begin with `ctrl+w`. Since `ctrl+w` is bound to a common task (closing a tab) you need to set this variable to `true` in order to change the default behavior and enable the rest of the commands.

* `nv_change_caret_style_in_command_mode`

The default value is `true`. This sets the cursor shape to `block` when `command_mode` is enabled and changes it to a "beam" when entering insert mode.

* `nv_toggle_hightlight_line_on_command_mode`

The default value is `false`. When set to `true` will highlight the line where the cursor is only in `command_mode`, and will stop when you enter insert mode. 

## Key Bindings

### Switch between modes

| Key | Command |
| --- |   ---   |
| `escape` | Go to normal mode |
| `i` | Insert text before the cursor |
| `a` | Insert text after the cursor |
| `o` | Insert a new line and insert text |
| `v` | Start visual mode |

### Cursor motions

The keys marked with an `*` are bound to a command I implemented in this plugin. Everything else uses sublime's built-in features and commands.

| Key | Command | Extends selection on visual mode |
| --- |   ---   | --- |
| `h` | Move cursor to the left | yes |
| `l` | Move cursor to the right | yes |
| `k` | Move cursor up | yes |
| `j` | Move cursor down | yes |
| `H`\* | Move cursor to the top of the screen | yes |
| `L`\* | Move cursor to the bottom of the screen | yes |
| `M`\* | Move cursor to the middle of the screen | yes |
| `gg` | Move cursor to the first of line of the file | yes |
| `G` | Move cursor to the last of line of the file | yes |
| `%` | Move cursor to the matching pair (think in stuff like brackets and parenthesis). | yes |
| `0` | Move cursor to the beginning of the line | yes |
| `$` | Move cursor to the end of the line | yes |
| `^`\* | Move cursor to the first non-blank character of the line | yes |
| `g_`\* | Move cursor to the last non-blank character of the line | yes |
| `w` | Move cursor to the beginning of the next word | yes |
| `b` | Move cursor to the beginning of the previous word | yes |
| `e` | Move cursor to the end of the next word | yes |
| `ge` | Move cursor to the end of the previous word | yes |
| `ctrl+i` | Move cursor to the most recent known position in your edit history | no |
| `ctrl+o` | Move cursor to the most last known position in your edit history | no |
| `ctrl+f` | Scroll one "page" forward | yes |
| `ctrl+b` | Scroll one "page" backwards | yes |
| `ctrl+u`\* | Scroll half a page forward | no |
| `ctrl+d`\* | Scroll half a page backwards | no |
| `ctrl+y` | Scroll 3 lines forward  | no |
| `ctrl+e` | Scroll 3 lines backwards  | no |
| `zz` | Center cursor on screen  | no |
| `n` | Move cursor to the next match of the current search | no |
| `N` | Move cursor to the previous match of the search | no |
| `*` | Start a search using the word under the cursor and move to the closes match | no |
| `#` | Start a "reverse" search using the word under the cursor and move to the closes match | no |
| `g]` | Go to definition of the symbol under the cursor |

### Window commands

| Key | Command |
| --- |   ---   |
| `gt` | Focus next tab |
| `gT` | Focus previous tab |
| `ctrl+w m` | Create a new pane |
| `ctrl+w q` | Destroy the current pane |
| `ctrl+w c` | Close a tab in the current pane |
| `ctrl+w s` | Set a layout with two panes divided horizontally |
| `ctrl+w v` | Set a layout with two panes divided vertically |
| `ctrl+w n` | Change focus to the next pane |
| `ctrl+w p` | Change focus to the previous pane |
| `ctrl+w N` | Swap places with the next pane |
| `ctrl+w P` | Swap places with the previous pane |

### Other commands

| Key | Command |
| --- |   ---   |
| `J` | Join lines |
| `<` | Undindent line/selected text |
| `>` | Indent line/selected text |
| `=` | Re-indent line/selected text |
| `u` | Undo |
| `ctrl+r` | Redo |
| `.` | Repeat |
| `y` | Copy |
| `p` | Paste text before cursor |
| `P` | Paste text after cursor |
| `x` | Delete character under the cursor |
| `dd` | Cut line |
| `~` | Swap case of characters of the word under the cursor or the selected text |
| `gu` | Switch the word under the cursor or the selected text to lowercase |
| `gU` | Switch the word under the cursor or the selected text to uppercase |
| `gc` | Toggle comments in the line under the cursor or the lines with selected text |
| `/` | Show search input |
| `?` | Show search input. Starts a "reverse" search |
| `zc` | Fold a code block |
| `zo` | Unfold a block of code |
| `zO` | Unfold all |

## Using your own keymap

Thanks to the sublime keymaps work you can extend this with your own shortcuts. First you'll need to go your "user folder" which is in the packages folder under the name `User`. Next create an `NvMode` folder, and in it create a `Default.sublime-keymap`. In other words, this:

```
$packages/User/NvMode/Default.sublime-keymap
```

`Default.sublime-keymap` needs to be have an array of keymaps, which may look something like this.

```json
[
  {
    "keys": ["[", "t"],
    "command": "prev_view",
    "context": [
      {"key": "setting.command_mode", "operand": true}
    ]
  },
  {
    "keys": ["]", "t"],
    "command": "next_view",
    "context": [
      {"key": "setting.command_mode", "operand": true}
    ]
  }
]
```

In here I'm remapping `]t` to the `next_view` command and `[t` to `prev_view` (they are the equivalent of `gt` and `gT`). And the context object tells sublime that they should valid whenever `command_mode` is enabled. Meaning this will work on command mode and also visual mode.

If you want a key binding that only works on command mode but not in visual mode you'll need this context:

```json
[
  {"key": "setting.command_mode", "operand": true}
  {"key": "setting.visual_mode", "operand": false}
]
```

To target only visual mode, just set both of those options to `true`.

```json
[
  {"key": "setting.command_mode", "operand": true}
  {"key": "setting.visual_mode", "operand": true}
]
```

And finally if you set `setting.command_mode` to `false`, that means "insert mode".

```json
[
  {"key": "setting.command_mode", "operand": false}
]
```

If you want to see a non-trivial example, check out my own configuration: [here](https://github.com/VonHeikemen/dotfiles/tree/84d6cbb91c242d533ff324a5fdeeae331d286478/.config/sublime-text-3/Packages/User/NvMode).

## Support

If you find this tool useful and want to support my efforts, [buy me a coffee ☕](https://www.buymeacoffee.com/vonheikemen).

[![buy me a coffee](https://res.cloudinary.com/vonheikemen/image/upload/v1618466522/buy-me-coffee_ah0uzh.png)](https://www.buymeacoffee.com/vonheikemen)

