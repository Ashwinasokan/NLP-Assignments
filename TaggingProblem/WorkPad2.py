inside = open('gene.test.txt', 'r')
outside = open('gene.test.smooth2.txt', 'a')
outside.write("<pre>\t<pre>\n")
outside.write("<start>\t<start>\n")
for currentLine in inside:
    words = currentLine.split()
    if not words:
        outside.write("<stop>\t<stop>\n")
        outside.write("<post>\t<post>\n")
        outside.write("<pre>\t<pre>\n")
        outside.write("<start>\t<start>\n")
    else:
        outside.write(currentLine)
outside.write("<stop>\t<stop>\n")
outside.write("<post>\t<post>\n")
outside.close()