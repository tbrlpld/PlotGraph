# PlotGraph - Package for Sublime Text 3 to plot selected number colums as graph.
# Copyright (C) 2017 Tibor Leupold
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import sublime
import sublime_plugin
import re
import tempfile


# http://stackoverflow.com/questions/354038/ \
# how-do-i-check-if-a-string-is-a-number-float-in-python
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_index(l, index):
    try:
        l[index]
        return True
    except IndexError:
        return False

# To return the content of a selection as a string:
# view.substr(view.sel()[0])
#
# view.sel() returns the selected area as tuples.
# Each tuple gives the beginning and end of a sublime.Region

# Call per window.run_command("plot_graph")
class PlotGraphCommand(sublime_plugin.WindowCommand):
    def settings(self):
        return sublime.load_settings('PlotGraph.sublime-settings')

    def run(self):
        window = self.window
        view = window.active_view()
        selections = view.sel()
        print(selections)
        if selections:
            for selection in selections:
                vectors = []
                # print the selections
                # print(selection)
                # print the region of the current selection as string
                # print(view.substr(selection))
                # Selection as string
                selection_str = view.substr(selection)

                # Windows cmd.exe has a command line limit of 8192 characters.
                # We save the selected data to a file (instead of passing it via
                # the command line) if there is more of it, with a safety margin
                # to cover formatting overhead and other command line elements.
                if len(selection_str) > 4096:
                    temp_file = tempfile.NamedTemporaryFile(suffix=".tmp", prefix="plotgraph.", delete=False)
                    temp_file.write(bytes(selection_str+"\n", 'UTF-8'))
                    temp_file.close()
                    # Get setting for python executable.
                    python_exec = self.settings().get('python_exec')
                    # Get optional setting for library path.
                    ld_library_path = self.settings().get('ld_library_path')
                    if ld_library_path:
                        python_exec = 'LD_LIBRARY_PATH={0} '.format(ld_library_path) + '"'+python_exec+'"'
                        # print(python_exec)
                    else:
                        python_exec = '"'+python_exec+'"'
                    window.run_command("exec", {"shell_cmd" : \
                        '{0} "{1}/PlotGraph/plotvectors/plotfile.py" --file="{2}"'.format(
                            python_exec,
                            sublime.packages_path(),
                            temp_file.name)})
                    # Suppress the panel showing
                    if self.settings().get("show_output_panel") == "False":
                        window.run_command("hide_panel", {"panel": "output.exec"})
                    return None

                # split selection at new lines
                lines_in_selection = selection_str.split("\n")
                # print(lines_in_selection)
                for line in lines_in_selection:
                    numbers_in_line = []
                    # Only keeping lines that are not empty.
                    if line:
                        # Split the line into "words".
                        # http://stackoverflow.com/a/23720594/6771403
                        # print("line = {0}".format(line))
                        words_in_line = re.split("[, !?:;$#]+", line)
                        # print("words = {0}".format(words_in_line))
                        # Check if the word is a number.
                        # Write numbers to line dependend numbers variable.
                        for word in words_in_line:
                            if is_number(word):
                                numbers_in_line = numbers_in_line + \
                                                    [float(word)]
                        # print("numbers_in_line = {0}".format(numbers_in_line))
                        if numbers_in_line:
                            # Take the i-th number in the line and put it into
                            # the i-th vector/list in vectors.
                            # If there is no i-th vector yet, create it before.
                            for i in range(0,len(numbers_in_line),1):
                                if not is_index(vectors, i):
                                    vectors.append([])
                                vectors[i].append(numbers_in_line[i])
                                # print("vectors = {0}".format(vectors))
                if vectors:
                    # Get setting for python executable.
                    python_exec = self.settings().get('python_exec')
                    # Get optional setting for library path.
                    ld_library_path = self.settings().get('ld_library_path')
                    if ld_library_path:
                        python_exec = 'LD_LIBRARY_PATH={0} '.format(ld_library_path) + '"'+python_exec+'"'
                        # print(python_exec)
                    else:
                        python_exec = '"'+python_exec+'"'
                    window.run_command("exec", {"shell_cmd" : \
                        '{0} "{1}/PlotGraph/plotvectors/plotvectors.py" -list_str="{2}"'.format(
                            python_exec,
                            sublime.packages_path(),
                            vectors)})
                    # Suppress the panel showing
                    if self.settings().get("show_output_panel") == "False":
                        window.run_command("hide_panel", {"panel": "output.exec"})
        return None
