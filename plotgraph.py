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
import tempfile

import sublime
import sublime_plugin
import Default.exec

from PlotGraph.plotvectors.common import extract_numbers


class PlotGraphExecCommand(Default.exec.ExecCommand):
    def on_finished(self, proc):
        super(PlotGraphExecCommand, self).on_finished(proc)
        exit_code = proc.exit_code()
        if exit_code != 0 and exit_code is not None:
            panel_view = self.window.find_output_panel("exec")
            output_panel_is_visible = panel_view != None and panel_view.window() != None
            if not output_panel_is_visible:
                self.window.run_command("show_panel", {"panel": "output.exec"})
                # we popped up a panel the user might have never seen before,
                # so give her a hint how to close it
                self.window.find_output_panel("exec").run_command("append", {
                        "panel": "output.exec",
                        "characters": "\n<press Esc to close this panel>\n"
                    })

# Call per window.run_command("plot_graph")
class PlotGraphCommand(sublime_plugin.WindowCommand):
    def settings(self):
        return sublime.load_settings('PlotGraph.sublime-settings')

    def is_column_selection(self, view, selections):
        # In sublime, a column selection is a set of typically rectangular
        # selection areas that are created using commands like
        # Ctrl-Alt-Up/Down followed by Shift-Left/Right
        # Shift-Right-Mouse-Drag (select first area)
        # Ctrl-Shift-Right-Mouse-Drag (add more areas)
        # Ctrl-Shift-L (make a column selection from a regular one)
        #
        # The characteristical property of a column selection
        # is that each subselection spans only a single line.
        # Since these single lines would not make a good graph each by its own,
        # we can join them all together for a single drawing.
        # The selections are sorted top down and left-right, so joining is easy.
        #
        # With the multi-rectangular selection, the user can do things
        # not possible otherwise, for example select some of the columns
        # of a table of numbers, sparsely. The sparseness may be both vertical
        # as well as horizontal, i.e. both some rows or columns may be ommitted.
        # You may have diagonally shifted selections or rectangular subareas
        # of variable width to cover different number length.
        #
        # If a column selection is recognized, even if it is a sparse one
        # (for example, two separated sets of adjacent rows),
        # still all data is presented in a single diagram. This way, by turning
        # two normal selections into column selections using Ctrl-Shift-L,
        # the user can enforce to get a single diagram.

        if len(selections) < 2:
            return False

        for selection in selections:
            if selection.size() == 0:
                # Empty selections are ignored (you get them if you use
                # Ctrl-Shift-Right-Mouse-Drag for the first selection)
                continue

            # A selection is a region, the begin/end of a region is a point (an int),
            # a rowcol is a tuple of two integers, row and col.
            (r0, _) = view.rowcol(selection.begin())
            (r1, _) = view.rowcol(selection.end())

            if r0 != r1:
                return False

        return True # all single-line selections

    def join_column_selections_to_string(self, view, selections):
        selection_str = ""
        row = None
        for selection in selections:
            (r0, _) = view.rowcol(selection.begin())
            if r0 != row:
                if row != None:
                    selection_str += "\n"
                row = r0
            else:
                selection_str += " "
            selection_str += view.substr(selection)
        selection_str += "\n"
        return selection_str


    def run_plot_script(self, script_name, option, argument):
        panel_view = self.window.find_output_panel("exec")
        output_panel_was_visible = panel_view != None and panel_view.window() != None

        python_exec = self.settings().get('python_exec')
        # library path setting is optional.
        ld_library_path = self.settings().get('ld_library_path')
        if ld_library_path:
            python_exec = 'LD_LIBRARY_PATH={0} '.format(ld_library_path) + '"'+python_exec+'"'
        else:
            python_exec = '"'+python_exec+'"'

        self.window.run_command("plot_graph_exec", {"shell_cmd" : \
            '{0} "{1}/PlotGraph/plotvectors/{2}" {3}="{4}"'.format(
                python_exec,
                sublime.packages_path(),
                script_name,
                option,
                argument), "quiet" : True})

        # Prevent the panel showing plugin printouts from popping up
        if not output_panel_was_visible and self.settings().get("show_output_panel") == "False":
            self.window.run_command("hide_panel", {"panel": "output.exec"})

    def run(self):

        # To return the content of a selection as a string:
        # view.substr(view.sel()[0])
        #
        # view.sel() returns the selected area as tuples.
        # Each tuple gives the beginning and end of a sublime.Region

        view = self.window.active_view()
        selections = view.sel()
        if selections:
            if self.is_column_selection(view, selections):
                selection_strings = [self.join_column_selections_to_string(view, selections)]
            else:
                selection_strings = (view.substr(selection) for selection in selections)

            for selection_str in selection_strings:
                vectors = []

                # Windows cmd.exe has a command line limit of 8192 characters.
                # We save the selected data to a file (instead of passing it via
                # the command line) if there is more of it, with a safety margin
                # to cover formatting overhead and other command line elements.
                if len(selection_str) > 4096:
                    temp_file = tempfile.NamedTemporaryFile(suffix=".tmp", prefix="plotgraph.", delete=False)
                    temp_file.write(bytes(selection_str+"\n", 'UTF-8'))
                    temp_file.close()
                    self.run_plot_script("plotvectors.py", "--file", temp_file.name)

                else:
                    lines_in_selection = selection_str.split("\n")
                    vectors = extract_numbers(lines_in_selection)
                    self.run_plot_script("plotvectors.py", "--list_str", vectors)
        return None
