# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 11:59:36 2017

@author: Michael Blume (mcb18)
intended use: Georgian Digital Text Collective HTML automation
Summary:
Generates an HTML file from a TEI GDTC file given the old layout, does not fill
out all of the table metadata

This program is not intended as a replacement for a validator,
but if the program doesn't work on the given xml file then
that file probably isn't validated. Please validate your file
and correct any errors before sending it through here.
"""
#built on Python 3.6, please download the latest version of Anaconda or another Python 3.6 script manipulator to use
import os #used to scan the folder specified by path
import re # regrex AKA regular expressions, used to split up text
from bs4 import BeautifulSoup # for parsing the xml
import sys
from datetime import datetime

date_object = datetime.now()
start_time = date_object.strftime('%m/%d/%Y %H:%M:%S')

#relative paths would be better, but for now absolute paths (just make sure to 
#specify the folder where the xml files are, and place the parser wherever you want the html files to go)
path = 'xml/'
#specify the folder where the support files will be (all of the Bootstrap etc.)
supDir = '../gdtc_support/'

#the common portion of all of the headers on the site, ussually inputed via PHP
common = '''<!DOCTYPE html> 
<html lang = "en">
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
		<title>{1}</title>
		<!-- Bootstrap -->
		<link href="{0}bootstrap-3.3.7-dist/css/bootstrap.min.css" rel="stylesheet">

		<!-- HTML5 shiv and Respond.js for IE8 support of HTML5 elements and media queries -->
		<!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
		<!--[if lt IE 9]>
		  <script src="{0}html5shiv.min.js"></script>
		  <script src="{0}respond.min.js"></script>
		<![endif]-->
		<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
		<script src="{0}jquery.min.js"></script>
		<!-- Include all compiled plugins (below), or include individual files as needed -->
		<script src="{0}bootstrap-3.3.7-dist/js/bootstrap.min.js"></script>

		<!--ah, the wonders of bootstrap-->
		<link href="{0}style.css" type="text/css" rel="stylesheet" media="screen" />
      <script src= "{0}georgian.js"></script>

		<link rel="shortcut icon" href="{0}favicon.ico" type="image/x-icon" />
		<meta name="viewport" content="width=device-width, initial-scale=1">

		<script src="{0}backgrounds.js" type="text/javascript"></script>
	</head>
	<body>
		<article id="containerText">
			<article id="title">
				<a href="http://depts.washington.edu/ndth"><img class= "logo" src="http://courses.washington.edu/dtcg/design/nbdt_logo_216px.png" alt="NDTH logo" /></a>
				<div id="top_right">
					<a href="http://www.facebook.com/pages/Georgian-Digial-Text-Collective/294984984002923"><img class= "logo" src="{0}facebook_small.gif" alt="Facebook" /></a>
					<!--<img class= "logo" src="{0}twitter_small.gif" alt="Twitter" /> -->
				</div>'''
#the top of the HTML document, minus the parts normally inputed by the common PHP file
htmlHeader = '''				<h1>Georgian Digital Text Collective</h1>
				<h1 class="get">{0}</h1>
			</article>
		</article>
		<article>
			<div class = "row" id = "row">
				<div class="col-lg-8 col-lg-offset-2">      
					<table class="table table-condensed table-hover">
						<thead>
						<tr>
						<th>Category:</th>
						<th>Descriptor:</th>
    					</tr>
						</thead>
						<tbody>
							<tr>
								<td>Author:</td>
								<td>{1}</td>
							</tr>
							<tr>
								<td>Publisher:</td>
								<td></td>
							</tr>
							<tr>
								<td>City:</td>
								<td></td>
							</tr>
							<tr>
								<td>Editor:</td>
								<td></td>
							</tr>
							<tr>
								<td>Translator:</td>
								<td>{2}</td>
							</tr>
							<tr>
								<td>Edition:</td>
								<td>Electronic Version</td>
							</tr>
							<tr>
								<td>Responsibility:</td>
								<td></td>
							</tr>
							<tr>
								<td>Date:</td>
								<td>{3}</td>
							</tr>
							<tr>
								<td>Copyright:</td>
								<td>{4}</td>
							</tr>
							<tr>
								<td>Notes:</td>
								<td><ol>{5}</ol></td>
							</tr>
							<tr>
								<td>Text ID:</td>
								<td></td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>
		</article>    
		<article>
			<div class = "row">
				<div class="col-lg-4 georgian col-lg-offset-2">
                \t<h2>{6}</h2>
				</div>
				<div class="col-lg-4 english">
					<h2>{8}</h2>
				</div>
			</div>
			<div class = "row">
				<div class="col-lg-4 georgian col-lg-offset-2">
					<h1>{7}</h1>
				</div>
				<div class="col-lg-4 english">
					<h1>{9}</h1>
				</div>
			</div>'''
#the top of the php document
header = '''<?php
	include("''' + supDir + '''common.php");
	$title = "{0}";
	top($title); ?>
				<h1><?= $title ?></h1>
				<h1 class="get">{0}</h1>
			</article>
		</article>
		<article>
			<div class = "row" id = "row">
				<div class="col-lg-8 col-lg-offset-2">      
					<table class="table table-condensed table-hover">
						<thead>
						<tr>
						<th>Category:</th>
						<th>Descriptor:</th>
    					</tr>
						</thead>
						<tbody>
							<tr>
								<td>Author:</td>
								<td>{1}</td>
							</tr>
							<tr>
								<td>Publisher:</td>
								<td></td>
							</tr>
							<tr>
								<td>City:</td>
								<td></td>
							</tr>
							<tr>
								<td>Editor:</td>
								<td></td>
							</tr>
							<tr>
								<td>Translator:</td>
								<td>{2}</td>
							</tr>
							<tr>
								<td>Edition:</td>
								<td>Electronic Version</td>
							</tr>
							<tr>
								<td>Responsibility:</td>
								<td></td>
							</tr>
							<tr>
								<td>Date:</td>
								<td>{3}</td>
							</tr>
							<tr>
								<td>Copyright:</td>
								<td>{4}</td>
							</tr>
							<tr>
								<td>Notes:</td>
								<td><ol>{5}</ol></td>
							</tr>
							<tr>
								<td>Text ID:</td>
								<td></td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>
		</article>    
		<article>
			<div class = "row">
				<div class="col-lg-4 georgian col-lg-offset-2">
                \t<h2>{6}</h2>
				</div>
				<div class="col-lg-4 english">
					<h2>{8}</h2>
				</div>
			</div>
			<div class = "row">
				<div class="col-lg-4 georgian col-lg-offset-2">
					<h1>{7}</h1>
				</div>
				<div class="col-lg-4 english">
					<h1>{9}</h1>
				</div>
			</div>'''
#the repeated body of the php document
textForm= '''
            <div class = "row">
				<div class="col-lg-4 georgian col-lg-offset-2">
					{0}
				</div>
				<div class="col-lg-4 english">
					{1}
				</div>
			</div>'''
#the bottom of the html document, ussually placed via PHP
htmlBottom = '''
		</article>
	</body>
</html>'''
#the bottom of the php document
bottom = '''
		<?php
	bottom();
?>'''
#function to check for if a given string is a number, for when creating the body
def is_number(s):
    try:
        float(s)
        return True
    except Exception:
        return False

#holds the georgian and english body
body = []
modifier = "_c.xml" #if there is a keyphrase in the file name for completed texts, this can be updated. This just opens .xml files presently
print("Detected Files: \n[\n")
paths = [os.path.join(path,fn) for fn in next(os.walk(path))[2]] #walk the folder
for path in paths:
    print(path)
    #print(os.fspath(path)) check to make sure the path is the file path
    print("\n")
print("]\n")
fNames = []
for path in range(len(paths)): #get every file in the folder and check if it's identical to the given modifier's type
    #print((paths)[path][(len(paths[path]) - len(modifier)):]) make sure the file extensions are correct
    if ((paths)[path][(len(paths[path]) - len(modifier)):] == modifier):
        try:
            markup = open(paths[path], encoding = "utf-8")
            soup = BeautifulSoup(markup, "xml", from_encoding="utf-8") #begin the process of reading through all of the xml
            #print(soup.getText()) #spits out all of the text without tags
            #print(soup.prettify()) #broad view of document, with tags
            text = ""
            containers = [soup.body.find_all("div", recursive = False)[0].find_all("div", recursive = False)[0], soup.body.find_all("div", recursive = False)[0].find_all("div", recursive = False)[1]]
            #the 1st index displays the English container. The 0th index is the Georgian container. If we had a 2nd index it would be the Russian?
            
            #parse the author and name fields, currently latinfirstname_etc_lastname, georgianfirstname_etc 
            author = re.split(',', soup.author.get_text())
            name = re.split(',', soup.title.get_text())
            i = 0
            while (i < len(author)):
                author[i] = author[i].replace("_", " ")
                i += 1
            i = 0
            while (i < len(name)):
                name[i] = name[i].replace("_", " ")
                i += 1
            if (len(author) > 1):
                gAuthor = author[1]
                author = author[0]
            elif (len(author) == 1):
                gAuthor = author[0]
                author = author[0]
            else:
                print("Something is wrong with the author scheme of " + path)
            if (len(name) > 1):
                gName = name[1]
                name = name[0]
            elif (len(name) == 1):
                gName = name[0]
                name = name[0]
            else:
                print("Something is wrong with the title scheme of " + path)
            fName = ''.join(e for e in author if e.isalnum()) + '_' + ''.join(e for e in name if e.isalnum())
            tl = re.split('\n', soup.respStmt.get_text())[2]
            cRight = soup.availability.get_text()
            body = []
            note = "";
            date = soup.date.get_text()
            form = ''
            #put in the supporting file directory +
            #get all of the HTML form metadata into one thing
            htmlMeta = common.format(supDir, name)+ "\n" + htmlHeader
            first = True;
            for container in containers: #iterates through the containers in the given xml file, based on the above containers list
                descendants = container.descendants
                lastChild = container
                form = ""
                unclosed = False
                for child in descendants: #iterates through the children/descendants of the given container
                    if (child.name == "l"):
                        if (is_number(child.string)): #format #1: if there is a number on its own line, recognize it as a new paragraph unles it's first
                            if (first):
                                form += "<p>\n" + child.string + "\n"
                            else:
                                form += "</p>"
                                body += [form]
                                form = "<p>\n" + child.string + "\n"
                                unclosed = True
                        elif (child.string == None): #format #3: if there is a blank line, recognize it as the start of a new paragraph
                            if (not first):
                                if (unclosed):
                                    form += "</p>"
                                    body += [form]
                                form = "\n<p>\n"
                                unclosed = True
                        elif (child.parent is not lastChild.parent): #format #2: if there is a new parent, recognize it as a new paragraph
                            if (not first):
                                form += "</p>"
                                body += [form]
                            form = "<p>\n"
                            form += child.string + "\n"
                            unclosed = True
                        else:
                            form += "\n" + child.string + "\n"
                            unclosed = False
                        first = False;
                        lastChild = child;
                    elif (child.name == "p"):
                        if (unclosed):
                            form += "\n</p>"
                            body += [form]
                            form = ""
                        form += "<p>\n" + child.string + "</p>"
                        body += [form]
                        form = "" 
                        unclosed = False
                        first = False;
                        lastChild = child;
                    elif (child.name == "pb"):
                        if (unclosed):
                            form += "\n</p>"
                            body += [form]
                            form = "" 
                        form += "<p class = \"pb\">\nPage: " + str(int(child['n'])) + "\n</p>"
                        body += [form]
                        form = ""
                        unclosed = False
                    elif (child.name == "note"):
                        note += "<li>" + child.get_text() + "</li>";                 
                if (unclosed):
                    form += "</p>"
                    body += [form]
                    form = ""
                first = True
            newHead = ''
            print(fName)
            fNames.append(fName)
            print("\n")
            #generate php
            with open(fName + '.php', 'w', encoding = 'utf-8') as phpFile: #finally, actually write a new php file with the name as its name
                newHead = (header + '.')[:-1] #store a copy of header, inefficient but necessary because pointers
                newHead = newHead.format(name + " , " + gName, author + " , " + gAuthor, tl, date, cRight.replace('\n', '\n\t\t\t\t\t\t\t\t'), note.replace('\n', '\n\t\t\t\t\t\t\t\t'), gAuthor, gName, author, name)
                #the number of tab escape sequences to put in each line to align the code was calculated by trial and error
                phpFile.write(newHead)
                for iterer in range(0, (round(len(body)/2))):
                    text = (textForm + '.')[:-1] #store a copy of textForm, inefficient but necessary because pointers
                    text = text.format(body[iterer].replace('\n', '\n\t\t\t\t\t'), body[iterer + round(len(body)/2)].replace('\n', '\n\t\t\t\t\t'))
                    phpFile.write(text) #set this copy to have all of the linegroups in it, and write the copy to the file
                phpFile.write(bottom)
                phpFile.close()
            #generate html5
            with open(fName + '.html', 'w', encoding = 'utf-8') as htmlFile: #finally, actually write a new html file with the name as its name
                newHead = (htmlMeta + '.')[:-1] #store a copy of header, inefficient but necessary because pointers
                newHead = newHead.format(name + " , " + gName, author + " , " + gAuthor, tl, date, cRight.replace('\n', '\n\t\t\t\t\t\t\t\t'), note.replace('\n', '\n\t\t\t\t\t\t\t\t'), gAuthor, gName, author, name)
                #the number of tab escape sequences to put in each line to align the code was calculated by trial and error
                htmlFile.write(newHead)
                for iterer in range(0, (round(len(body)/2))):
                    text = (textForm + '.')[:-1] #store a copy of textForm, inefficient but necessary because pointers
                    text = text.format(body[iterer].replace('\n', '\n\t\t\t\t\t'), body[iterer + round(len(body)/2)].replace('\n', '\n\t\t\t\t\t'))
                    htmlFile.write(text) #set this copy to have all of the linegroups in it, and write the copy to the file
                htmlFile.write(htmlBottom)
                htmlFile.close()
            markup.close()
            containers.clear()
            #break #for testing purposes
        except Exception as e:
            print("\nAn error " + str(e) + " occured on line" + str(sys.exc_info()[-1].tb_lineno) + " for " + paths[path].replace('\\', '/') + "!" + "\n Please make sure that your XML validates")
print("\n")

end_time = date_object.strftime('%m/%d/%Y %H:%M:%S')
indexName = re.split(" ",start_time)[0].replace("/", "_") + "_index.txt"
print("Printing directory to txt file " + indexName)
fNames.sort() #alphabetize the file names

indexBody = "Start time: " + start_time + "\nEnd time: " + end_time + "\n\n"
for name in fNames:
    indexBody += name + ".html\n"
indexBody = indexBody[:-1]

with open(indexName, 'w', encoding = 'utf-8') as indexFile: #now write a new txt file that chronicles all the filenames for clerical purposes
    indexFile.write(indexBody)
    indexFile.close()

'''</div>
			<div class = "row" id = "row">
				<div class="col-lg-4 georgian col-lg-offset-2">
					<p>{0}</p>
				</div>
				<div class="col-lg-4 english">
					<p>{1}</p>
				</div>
			</div>'''
    #    lastIter = iter    
    
    ##I need to create a new paragraph/row
    

'''
talk to Mary again about what is possessed and actually write it down

#goes at the end of the for loop when I actually create the file
if not os.path.exists(directory):
    os.makedirs(directory)
with open(index, "w") as text_file:
    print(multilineText, file=text_file)
    print(soup.head, file=text_file) for example, although what I'll probably do is create multiline strings for this
'''
