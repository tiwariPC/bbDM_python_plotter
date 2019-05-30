import os

f=open("index.html",'w')
f.write("<html>\n")
f.write('<head>\n')
f.write('<title>bbDM Analysis Plots | Praveen Chandra Tiwari</title>\n')
f.write('<style>img {display: inline;}</style>\n')
f.write('</head>\n')
f.write('<body>\n')
f.write('<center><h1><u><b>bbDM Analysis Plots</b></u></h1></center>\n')
f.write('<div class="row">\n')
f.write('<center>\n')
for dr in sorted(os.listdir("."),key=os.path.getmtime)):
    if not os.path.isfile(dr):
        f.write("<a href = "+dr+"> "+dr+"</a><br>\n")
f.write("</div>\n")
f.write('</center>\n')
f.write('</body>\n') 
f.write("<a href='../index.html'>BACK</a><br>\n</h2></html>")
f.write("</html>\n")
f.close()
