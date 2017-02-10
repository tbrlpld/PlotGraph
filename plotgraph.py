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

class ReturnSelection(sublime_plugin.TextCommand):
    def run(self):
        print("ReturnSelection is run.")
        