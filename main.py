import svgwrite


def wire(ctx, el):
  for e in el:
    start = e.get("x1"), e.get("y1")
    end = e.get("x2"), e.get("y2")
    ctx.add(dwg.line(start, end, stroke=svgwrite.rgb(10, 10, 16, '%'), stroke_width=e.get("width")))
    
def via(ctx, el):
  for e in el:
    center = e.get("x"), e.get("y")
    ctx.add(dwg.circle(center=center, r=float(e.get("diameter"))/2, fill='blue', stroke_width=0))
   
def pad(ctx, el):
   for e in el:
    center = float(e.get("x")) - float(e.get("diameter"))/2, float(e.get("y")) - float(e.get("diameter"))/2
    size = e.get("diameter"), e.get("diameter")
    ctx.add(dwg.rect(insert=center, size=size, fill='red'))

def smd(ctx, el):
   for e in el:
    #center = 0, 0
    roundness_x = (float(e.get("roundness", "0")) / 100) * float(e.get("dx")) / 2
    roundness_y = (float(e.get("roundness", "0")) / 100) * float(e.get("dy")) / 2
 
    center = float(e.get("x")) - float(e.get("dx"))/2 , float(e.get("y"))-float(e.get("dy"))/2
    size = e.get("dx"), e.get("dy")
    #print(e.get("rot"))
    rot = e.get("rot","R0")[1:]
    #g = svgwrite.container.Group(transform='rotate('+str(rot)+') translate('+e.get("x")+','+e.get("y")+')')
    g = svgwrite.container.Group(transform='rotate('+str(rot)+')')
    g.add(dwg.rect(insert=center, size=size, rx=roundness_x, ry=roundness_y, fill='red'))
    ctx.add(g)
         

def package(ctx, el):
  for e in el:
    ws = e.findall("wire")
    wire(ctx, ws)
    pads = e.findall("pad")
    pad(ctx, pads)
    smds = e.findall("smd")
    smd(ctx, smds)

    
dwg = svgwrite.Drawing('test.svg', profile='tiny', viewBox=('-20 -20 40 40'),size=('170mm', '130mm'))

dwg.stroke(linecap='round')

#import xml.etree.ElementTree as etree    
from lxml import etree
tree = etree.parse('bc-cloony.brd')  
root = tree.getroot()                    

el = tree.xpath("//signal/wire[@layer=1]")
wire(dwg, el)

el = tree.xpath("//signal/via")
via(dwg, el)

#elements
el = tree.xpath("//elements/element")
for e in el:
  print (e.get("package"))
  rot = e.get("rot", "R0")[1:]
  print(rot)
  g = svgwrite.container.Group(transform='translate('+str(e.get('x'))+','+str(e.get('y'))+') rotate('+rot+')')
  #g = svgwrite.container.Group()
  el = tree.xpath("//package[@name='"+e.get("package")+"']")
  package(g, el)
  dwg.add(g)

#board
el = tree.xpath("//board/plain/wire")
wire(dwg, el)
  
#g = svgwrite.container.Group(transform='translate(4,3)')
#g.add(dwg.circle(center=(0,0), r=2, stroke='red', stroke_width=0.1))
#dwg.add(g)
  
dwg.save()