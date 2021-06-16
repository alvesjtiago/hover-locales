import sublime
import sublime_plugin
import os
import re
import yaml

class HoverLocales(sublime_plugin.EventListener):
  def on_hover(self, view, point, hover_zone):
    settings = sublime.load_settings('Hover Locales.sublime-settings')
    scopes = settings.get("scopes")
    if (hover_zone == sublime.HOVER_TEXT and any(scope in view.scope_name(point) for scope in scopes)):
      hovered_line_text = view.substr(view.line(point)).strip()

      next_double_quote = view.find('"', point).a
      next_single_quote = view.find("'", point).a
      next_parentheses  = view.find(r"\)", point).a

      symbols_dict = { next_double_quote: '"',
                       next_single_quote: "'",
                       next_parentheses: ')' }

      symbols = []
      if next_double_quote != -1:
        symbols.append(next_double_quote)
      if next_single_quote != -1:
        symbols.append(next_single_quote)
      if next_parentheses != -1:
        symbols.append(next_parentheses)

      # Check if symbols exist from the mouse pointer forward
      if len(symbols) == 0:
        return

      closest_symbol = min(symbols)
      symbol = symbols_dict[closest_symbol]

      quote_type = symbol

      regex = r""
      if symbol == "'":
        regex = r"'([^']*)'"
      elif symbol == '"':
        regex = r'"([^"]*)"'
      elif symbol == ")":
        regex = r'\(([^()]*)\)'

      path = re.findall(regex, hovered_line_text)

      # All quotes in view
      if symbol == ")":
        all_quotes = view.find_all(r"\(|\)")
        all_match = [item for item in all_quotes if (item.a == closest_symbol)]
      else:
        all_quotes = view.find_all(quote_type)
        all_match = [item for item in all_quotes if item.a == closest_symbol]

      # If there are no matches return
      if len(all_match) == 0:
        return

      # Get final and initial region of quoted string
      final_region = all_match[0]
      index = all_quotes.index(final_region) - 1
      initial_region = all_quotes[index]

      # String path for file
      path = view.substr(sublime.Region(initial_region.b, final_region.a))
      path = path.strip().split('/')[-1]

      # Get base project folder
      base_folder = os.path.join(sublime.active_window().folders()[0], settings.get("locales_path"))

      if (path and path != "" and os.path.isdir(base_folder)):
        values = {}

        # Check if file is under views in Rails
        if view.file_name():
          if path.startswith("."):
            relative_path = view.file_name().split('views/')[-1].split('.')[0]
            path_split = relative_path.split('/')
            path_split.append(path.split('.')[1])

            # Check each locale file for a match
            for root, dirs, files in os.walk(base_folder):
              for file in files:
                if file.endswith("yml"):
                  file_name = os.path.join(root, file)
                  with open(file_name, "rb") as file:
                    raw_yaml = yaml.load(file.read(), Loader=yaml.FullLoader)
                    locale = list(raw_yaml.keys())[0]

                    file_yaml = raw_yaml[locale]
                    for path_section in path_split:
                      try:
                        file_yaml = file_yaml[path_section]
                      except:
                        break
                    if type(file_yaml) is dict:
                      continue
                    else:
                      values[locale] = {}
                      values[locale]["string"] = file_yaml
                      values[locale]["path"] = file_name

        # Check each locale file for a match
        path_split = path.split('.')
        for root, dirs, files in os.walk(base_folder):
          for file in files:
            if file.endswith("yml"):
              file_name = os.path.join(root, file)
              with open(file_name, "rb") as file:
                raw_yaml = yaml.load(file.read(), Loader=yaml.FullLoader)
                locale = list(raw_yaml.keys())[0]

                file_yaml = raw_yaml[locale]
                for path_section in path_split:
                  try:
                    file_yaml = file_yaml[path_section]
                  except:
                    break
                if file_yaml is None:
                  continue
                elif type(file_yaml) is dict:
                  continue
                else:
                  values[locale] = {}
                  values[locale]["string"] = file_yaml
                  values[locale]["path"] = file_name

        if len(values) == 0:
          return
        html = ""
        should_break = False
        for key, value in values.items():
          if should_break:
            html += "<br>"
          should_break = True

          value_string = '' if value["string"] is None else value["string"]
          value_path = '' if value["path"] is None else value["path"]

          html += '<div><a href="' + value_path + '">'
          html += '<span style="color: #f00">' + key + '</span>' + ': ' + value_string
          html += '</a></div>'

        view.show_popup('<div>' + html + '</div>',
                   flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                   location=point,
                   on_navigate=self.open_locale)
      return
    return

  def open_locale(object, path):
    sublime.active_window().open_file(path)
