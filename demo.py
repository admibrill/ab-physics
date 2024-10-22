import physics

window1=physics.Space(1000,600,'123',9.8)
window1.launch()
circle1=physics.Circle(window1,0,100,100,40,0,physics.DYMANIC,1000)
force1=physics.Force(1000,0)
circle1.forceCompound(force1)
segment1=physics.Segment(window1,0,50,550,950,550,0,physics.STATIC,1000)
physics.run()




