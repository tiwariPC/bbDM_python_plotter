import os

f=open("index.html",'w')
f.write("<html>\n")
f.write('<head>\n')
f.write('<title>2016 bbDM updated plots | Praveen Chandra Tiwari</title>\n')
f.write('<style>img {display: inline;}</style>\n')
f.write('</head>\n')
f.write('<body>\n')
f.write('<center><h1><u><b>2016 bbDM updated plots 29092019</b></u></h1></center>\n')
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
