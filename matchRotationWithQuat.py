
#######
# Script example rotate one object to the other using quaternion 
#######
'''
Create two simple polyplane with polyPlane subd W and H both setting to 2
For both planes, we are assuming vertex id 1 is locate at object pivot, and vertex id 7 in on object z axis
You can swap z axis vector and pivot vector for acutal usage.
'''


import maya.api.OpenMaya as om
import maya.cmds as cmds

#Assuming pivot point vertex id = 1
n_id = 1

#Assuming vertex id =7 is on source pivot z axis
z_id = 7

sel = cmds.ls( sl=True, l=True )
msel = om.MSelectionList()
msel.add( sel[0] )
msel.add( sel[1] )
tar = om.MFnMesh( msel.getDagPath(0) )
src = om.MFnMesh( msel.getDagPath(1) )
mesh = om.MFnTransform( msel.getDagPath(1) )

#get pivot position
t0 = om.MVector( tar.getPoint( n_id , om.MSpace.kWorld ) ) 
s0 = om.MVector( src.getPoint( n_id , om.MSpace.kWorld ) ) 

#get z vector position
t1 = om.MVector( tar.getPoint( z_id , om.MSpace.kWorld ) )
s1 = om.MVector( src.getPoint( z_id , om.MSpace.kWorld ) )

#offset z vector to origin
ss = s1 - s0
tt = t1 - t0

#first rotate 
q1 = ss.rotateTo(tt)
mesh.rotateBy(q1, om.MSpace.kWorld)


#sendcond rotate based on normal 
t2 = tar.getVertexNormal( n_id, True, om.MSpace.kWorld )
s2 = src.getVertexNormal( n_id, True, om.MSpace.kWorld )
q2 = s2.rotateTo(t2)
mesh.rotateBy(q2, om.MSpace.kWorld)


#move src to target pivot
cmds.xform( sel[1], ws=True, t=t0 )
