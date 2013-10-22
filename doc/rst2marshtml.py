import sys
import os
import textwrap
from docutils import core

def createHeader(relPath):
    out = '''\
             <!DOCTYPE html>
             <html>
               <head>
                 <title>MARS Simulator</title>
                 <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
                 <meta name="description" content="MARS is a flexible physics simulator.">
                 <meta name="author" content="MARS Project">
                 <meta name="keywords" content="MARS, simulation, physics, robotics">
                 <link rel="stylesheet" type="text/css" href="{relPath}/css/mars_default.css" media="all" />
               </head>
             <body>
               <div class="nav-box">
                 <h2>Navigation</h2>
                 <nav>
                   <ol>
                     <li><a href="{relPath}/index.html">Home</a></li>
                   </ol>
                 </nav>
               </div>
               <div id="content">
               <header>
                 <a href="{relPath}/index.html"><img src="{relPath}/images/logo_v2_wob.png" alt="MARS" /></a>
               </header>
       '''.format(relPath = relPath)
    return textwrap.dedent(out)

def createFooter():
    out = '''\
          <footer>
            <a href="http://validator.w3.org/check?uri=referer" target="_blank">
              <img src="http://www.w3.org/Icons/valid-html401"
                   alt="Valid HTML 4.01 Transitional"/>
            </a>
            <a href="http://jigsaw.w3.org/css-validator/check/referer" target="_blank">
              <img src="http://jigsaw.w3.org/css-validator/images/vcss"
                   alt="Valid CSS!"/>
            </a>
          </footer>
        </div>
      </body>
    </html>
          '''
    return textwrap.dedent(out)

def convertRstToHtml(filePath, fileName):
    outPath = "." + filePath[2:].replace("/doc", "")
    relPath = constructRelativePath(outPath)
    headerString = createHeader(relPath)
    footerString = createFooter()
    inFile = open(filePath + "/" + fileName, "r")
    bodyString = inFile.read()
    inFile.close()
    bodyString = core.publish_parts(bodyString, writer_name='html') ['html_body']
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    outFile = open(outPath+ "/" + fileName[:-4]+".html", "w")
    outFile.write("<!-- DO NOT EDIT THIS FILE! IT IS AUTOMATICALLY GENERATED BY rst2marshtml //-->\n")
    outFile.write(headerString)
    outFile.write(bodyString)
    outFile.write(footerString)
    outFile.close()
    print "Converted " + filePath + "/" + fileName + " to " + outPath + "/" + fileName
    
def constructRelativePath(filePath):
    n = filePath.count("/")
    if n == 0:
        return "."
    else:
        relPath = ".."
        for i in range(n-1):
            relPath+="/.."
        return relPath

if __name__ == '__main__':

    #the following code browses through all directories and automatically converts all .rst files
    n = 0
    for root, dirs, files in os.walk("../"):
        for f in files:
            if f[-4:] == ".rst":
                convertRstToHtml(root, f)
                n+=1
    print "In total,", n, "files were converted."


