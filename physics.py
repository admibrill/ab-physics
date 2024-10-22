from PySide6 import *
import math
qapp=QtWidgets.QApplication([])
DYMANIC=0
STATIC=1
class Space(QtWidgets.QWidget):
    def __init__(self,width,height,caption,g):
        super().__init__()
        self.width=width
        self.height=height
        self.caption=caption
        self.objects=[]
        self.g=g
        self.timer = QtCore.QTimer()
    def launch(self):
        self.resize(self.width,self.height)
        self.setWindowTitle(self.caption)
        self.timer.start(5)
        self.timer.timeout.connect(self.moveObjects)
        self.timer.timeout.connect(self.update)
        self.show()
    def moveObjects(self):
        for i in self.objects:
            if i.stype==DYMANIC:
                gravity=Force(self.g,math.pi/2)
                i.forceCompound(gravity)
                i.move()
    def paintEvent(self,event):
        painter = QtGui.QPainter(self)
        for i in self.objects:
            if isinstance(i,Circle):
                painter.setPen(i.pen)
                painter.drawEllipse(i.cpoint,i.r,i.r)
                painter.drawLine(i.cpoint.x(),i.cpoint.y(),i.cpoint.x()+i.r*math.cos(i.direction),i.cpoint.y()+i.r*math.sin(i.direction))
            elif isinstance(i,Segment):
                painter.setPen(i.pen)
                painter.drawLine(i.x1,i.y1,i.x2,i.y2)
    def getObjects(self):
        return self.objects
class Force():
    def __init__(self,size,angle):
        self.size=size
        self.angle=angle
class Object():
    def __init__(self,z,window,color,mass,angle):
        self.z=z
        self.window=window
        self.window.objects.append(self)
        self.color=QtGui.QColor()
        self.color.setRgb(color[0],color[1],color[2])
        self.mass=mass
        self.velocity=0
        self.angle=angle
    def forceCompound(self,add_force):
        cur_force_size=self.velocity
        cur_force_dx=cur_force_size*math.cos(self.angle)+add_force.size*math.cos(add_force.angle)/self.mass
        cur_force_dy=cur_force_size*math.sin(self.angle)+add_force.size*math.sin(add_force.angle)/self.mass
        self.velocity=math.sqrt(cur_force_dx**2+cur_force_dy**2)
        if cur_force_dx>=0:
            self.angle=math.atan(cur_force_dy/cur_force_dx)
        else:
            self.angle=math.atan(cur_force_dy/cur_force_dx)+math.pi
    def destroy(self):
        self.window.objects.remove(self)
        self.window=None
        del self
class Solid(Object):
    def __init__(self,z,window,color,stype,mass,angle,direction):
        super().__init__(z,window,color,mass,angle)
        self.stype=stype
        self.direction=direction
        self.pen = QtGui.QPen(self.color)
        self.pen.setWidth(2)
class Circle(Solid):
    def __init__(self,window,z,x,y,r,direction,stype,mass,angle=0,color=(0,0,255)):
        super().__init__(z,window,color,stype,mass,angle,direction)
        self.cpoint=QtCore.QPointF(x,y)
        self.r=r
    def move(self):
        self.cpoint.setX(self.cpoint.x()+self.velocity*math.cos(self.angle))
        self.cpoint.setY(self.cpoint.y()+self.velocity*math.sin(self.angle))
    def hit(self,c):
        pass
class Segment(Solid):
    def __init__(self,window,z,x1,y1,x2,y2,direction,stype,mass,angle=0,color=(0,0,255)):
        super().__init__(z,window,color,stype,mass,angle,direction)
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
    def move(self):
        self.x1+=self.velocity*math.cos(self.angle)
        self.y1+=self.velocity*math.sin(self.angle)
        self.x2+=self.velocity*math.cos(self.angle)
        self.y2+=self.velocity*math.sin(self.angle)
    def hit(self,c):
        pass
class Liquid(Object):
    def __init__(self):
        pass
class Joint(Object):
    def __init__(self):
        pass
def run():
    qapp.exec()



