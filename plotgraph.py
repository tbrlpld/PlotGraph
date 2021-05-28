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
import tempfile

from PlotGraph.plotvectors.common import extract_numbers

# To return the content of a selection as a string:
# view.substr(view.sel()[0])
#
# view.sel() returns the selected area as tuples.
# Each tuple gives the beginning and end of a sublime.Region

# Call per window.run_command("plot_graph")
class PlotGraphCommand(sublime_plugin.WindowCommand):
    def settings(self):
        return sublime.load_settings('PlotGraph.sublime-settings')

    def run_plot_script(self, script_name, option, argument):
        # Get setting for python executable.
        python_exec = self.settings().get('python_exec')
        # Get optional setting for library path.
        ld_library_path = self.settings().get('ld_library_path')
        if ld_library_path:
            python_exec = 'LD_LIBRARY_PATH={0} '.format(ld_library_path) + '"'+python_exec+'"'
            # print(python_exec)
        else:
            python_exec = '"'+python_exec+'"'

        self.window.run_command("exec", {"shell_cmd" : \
            '{0} "{1}/PlotGraph/plotvectors/{2}" {3}="{4}"'.format(
                python_exec,
                sublime.packages_path(),
                script_name,
                option,
                argument)})
        # Suppress the panel showing
        if self.settings().get("show_output_panel") == "False":
            self.window.run_command("hide_panel", {"panel": "output.exec"})

    def run(self):
        view = self.window.active_view()
        selections = view.sel()
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
                    self.run_plot_script("plotfile.py", "--file", temp_file.name)

                else:
                    # split selection at new lines
                    lines_in_selection = selection_str.split("\n")
                    # print(lines_in_selection)
                    vectors = extract_numbers(lines_in_selection)
                    if len(vectors) > 0:
                        self.run_plot_script("plotvectors.py", "-list_str", vectors)
        return None
