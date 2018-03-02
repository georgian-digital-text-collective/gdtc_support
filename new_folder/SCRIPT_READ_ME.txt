Documentation for xmlParser, written by Michael Blume
This program uses an interior specified file path and walks/reads through all of the c.xml files
within that file path (ignoring subfolders). It then creates a php file with HTML5 code inside
for use within the GDTC website.

This program is not intended as a replacement for a validator,
but if the program doesn't work on the given xml file then
that file probably isn't validated. Please validate your file
and correct any errors before sending it through the script.

pre conditions:
1) must have a Python 3.6 editor on the computer/server, most recent version of Anaconda recommended
2) must have the following modules installed (recommended to use command prompt/bash shell and type pip install ___ where ___ is the module name,
after Anaconda has been installed): 
	a) os (should already be installed)
	b) re (should already be installed)
	c) BeautifulSoup (ex. pip install beautifulsoup4)
	d) lxml (ex. pip install lxml)
	e) sys (should already be installed)
	f) datetime (should already be installed)
these modules are for, respectively:
	a) looking through a specified folder for xml files to convert
	b) altering text through searching (look up regular expressions if you'd like to know more)
	c) looking through a given xml file hierarchy
	d) creating trees from XML
	e) error reporting doesn't crash the program
	f) recording when the output and input took place for what files
3) xml files in the given folder should be validated to TEI Lite spec and written according to our schema, otherwise the conversion might fail
4) xml files in the given folder should have at least 1 line or paragraph tag in the Georgian and English containers denoting the actual text (the parser reads for both)
4) xml files in the given folder must have file names ending in _c.xml or whatever the in program specified modifier is, where c stands for completed, otherwise they will not be read
5) file path inside the script must be changed according to the relative path of where the xml files are stored

post conditions:
Creates a new PHP and HTML5 file from the XML hierarchies according to the HTML layout included in the script and named with the title of the text, placing 
the new file in the same folder as the parser is in. Also creates a new txt file from the list of inputs containing the time the script ran and a list of the files outputted from the script. These files require all support files (JavaScript, and mostly Bootstrap files) listed in their headers, which are included in this folder. These files are expected to go into the folder titled YOURCOMPLETEDFILESGOHERE before you read them in a web browser.

If at any time an exception is raised because the file has not been formatted correctly, the exception will be printed in the python console window and the html creation for that xml file will be aborted. The rest of the files 
in the folder will however continue to be converted, so it is up to the client to ensure that their file conversions were all successful 
by checking the console window for error messages.