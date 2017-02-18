PlotGraph - A Sublime Text 3 Package
====================================

Plot a column of numbers as a graph, or create a quick curve comparison based on multiple number columns.

##Installation

### Requirements

 - You need a [python](https://www.python.org/downloads/release/python-360/) installation on your computer. The sublime-internal python is not sufficient.
 - That python environment needs to have to module [matplotlib](http://matplotlib.org/) installed.
 - To test if your python installation has matplotlib installed, you can do the following:
 	- Open a terminal.
 	- Start python, e.g. by entering `python` and hit [Enter].
 	- In the started python console, enter: `import matplotlib`.
 	- If this command finished without an error message you are all set.

### Install Using PackageControl 

 -  *not available yet*

### Manual Installation

 1. Download the [zip archive](https://github.com/tibsel/PlotGraph/archive/master.zip).
 2. Rename the zip archive to ```PlotGraph.sublime-package```
 3. Copy the renamed package into the ```Installed Packages``` directory.
	- If you are not sure where to find that directory, go to Sublime Text 3 ```Menu > Preferences > Browse Packages...```.
      This should open a directory in you browser. 
      Navigate one folder up, and there you should find the ```Installed Packages``` directory.
	- For example, in Ubuntu (or other Linux distributions) you should find the ```Installed Packages``` directory under the following path: ```/home/<username>/.config/sublime-text-3/Installed Packages/```.
 4. Restart Sublime Text 3.


## Setup



## Usage


Select the numbers you want to see plotted (with one selection). 
If other content is also selected, that's ok, 
because the selection will be filtered for numbers.
Once the selection is made, hit [F3] to create a matplotlib window.
If you select one column of numbers, they will be printed over their index.

	0.0
 	4.0
 	3.0
 	5.0
 	5.0
 	5.0
 	4.0
 	0.0 


If you select two columns, the first one will be used as the values on the 
abscissa/x-axis and the second column as the values on the ordinate/y-axis.

 	1.0 0.0 
 	2.0 4.0 
 	3.0 3.0 
 	4.0 5.0 
 	5.0 5.0 
 	6.0 5.0 
 	7.0 4.0 
 	8.0 0.0 
	

If more than two columns are selected, the first one will be used as the values 
on the abscissa/x-axis. The other columns will be printed as values on the 
ordinate/y-axis for different curves.

 	1.0 0.0 11.1
 	2.0 4.0 11.2
 	3.0 3.0 11.3
 	4.0 5.0 11.4
 	5.0 5.0 11.5
 	6.0 5.0 -11.6
 	7.0 4.0 -11.7
 	8.0 0.0 -11.8
	
	
