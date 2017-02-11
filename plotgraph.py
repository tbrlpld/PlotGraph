import sublime
import sublime_plugin
import re


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

# view.run_command("return_selection")
class ReturnSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("ReturnSelection is run.")
        view = self.view
        selections = view.sel()
        print(selections)
        lines = []
        vectors = []
        if selections:
            for selection in selections:
                # print the selections
                print(selection)
                # print the region of the current selection as string
                print(view.substr(selection))
                # selection as string
                selection_str = view.substr(selection) 
                # split selection at new lines
                lines_in_selection = selection_str.split("\n")
                print(lines_in_selection)
                for line in lines_in_selection:
                    numbers_in_line = []
                    # Only keeping lines that are not empty.
                    if line:
                        lines = lines + [line]
                        # Split the line into "words". (http://stackoverflow.com/a/23720594/6771403)
                        print("line = {0}".format(line))
                        words_in_line = re.split("[, \-!?:]+", line)
                        print("words = {0}".format(words_in_line))
                        # Check if the word is a number. Only keep numbers. At least in the vector variable.
                        for word in words_in_line:
                            if is_number(word):
                                numbers_in_line = numbers_in_line + [float(word)]
                        print("numbers_in_line = {0}".format(numbers_in_line))
                        if numbers_in_line:
                            # Take the i-th number in the line and put it into 
                            # the i-th vector/list in vectors. 
                            # If there is no i-th vector yet, create it before.
                            for i in range(0,len(numbers_in_line),1):
                                if not is_index(vectors, i): 
                                    vectors.append([])
                                vectors[i].append(numbers_in_line[i])
                                print("vectors = {0}".format(vectors))
                                