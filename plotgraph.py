import sublime
import sublime_plugin


# The command class "ExampleCommand" can be called by view.run_command("example").
# The "example" is the name of the class "ExampleCommand", stripped by the 
# "Command" and converted to lower case.
class ExampleCommand(sublime_plugin.TextCommand): 
    def run(self, edit):
        self.view.insert(edit, 0, "Hello, World!")

# Just like "ExampleCommand" this class can be called by view.run_command("my_first").
class MyFirstCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "This is my test")


# To return the content of a selection as a string:
# view.substr(view.sel()[0])
#
# view.sel() returns the selected area as tuples.
# Each tuple gives the beginning and end of a sublime.Region

class ReturnSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("ReturnSelection is run.")
        view = self.view
        selections = view.sel()
        print(selections)
        lines = []
        if selections:
            # print the selections
            for selection in selections:
                print(selection)
                # print the region of the current selection as string
                print(view.substr(selection))
                # selection as string
                selection_str = view.substr(selection) 
                # split selection at new lines
                lines_in_selection = selection_str.split("\n")
                print(lines_in_selection)
                lines = lines + lines_in_selection
        print(lines)


        

#test change for no res.