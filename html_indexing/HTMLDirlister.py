import os, commands
import sys, optparse

usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)
parser.add_option("-i", "--plot_dir",  dest="plot_dir")
(options, args) = parser.parse_args()
os.system('cp -r '+options.plot_dir+'/bbDMP* .')

dirpath= commands.getoutput('pwd')
dirname = str(os.path.basename(dirpath)).replace('_',' ')

f=open("index.html",'w')
f.write("<html>\n")
f.write('<head>\n')
f.write('<title>'+dirname+'| Praveen Chandra Tiwari</title>\n')
f.write('<style>img {display: inline;}</style>\n')
f.write('</head>\n')
f.write('<body>\n')
f.write('<center><h1><u><b>'+dirname+'</b></u></h1></center>\n')
f.write('<div class="row">\n')
#f.write('<center>\n')
for dr in sorted(os.listdir("./bbDMPng")):
    if not os.path.isfile(dr):
        f.write("<h1>"+dr+" Control Region </h1>\n")
        for fl in sorted(os.listdir("bbDMPng/"+dr)):
            if fl.endswith(".png"):
                f.write('  <a href="bbDMPdf/'+dr+'/'+fl.split(".")[0]+'.pdf"><img src="bbDMPng/'+dr+'/'+fl+'"WIDTH=525 HEIGHT=450></a>\n')
f.write("</div>\n")
#f.write('</center>\n')
f.write('</body>\n') 
f.write("<a href='../index.html'>BACK</a><br>\n</h2></html>")
f.write("</html>\n")
f.close()
