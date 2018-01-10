import maya.cmds as cmds

'''
    transferObjMatrixToCam.py

    This script will transfre selected object to a duplicated camera.It's useful for stablize obj.
    Select obj and then camera. Choose one frame as reset frame, and run the script.

    You can then duplicate obj without animation at rest frame, and view from new camera, 
    It should looks identical in viewport comparing to the original camera and moving obj
'''

#require select select obj and camera,
#The script will also use current frame as rest position
sel = cmds.ls(sl=True, l=True)
mat1 = cmds.createNode('multMatrix')
mat2 = cmds.createNode('multMatrix')
mat3 = cmds.createNode('composeMatrix')
mat4 = cmds.createNode('decomposeMatrix')
nCam  = cmds.duplicate(sel[1], rr=True)

cmds.connectAttr('%s.worldMatrix[0]'%sel[1], '%s.matrixIn[0]'%mat1)
cmds.connectAttr('%s.inverseMatrix'%sel[0], '%s.matrixIn[1]'%mat1)

cmds.connectAttr('%s.translate'%sel[0], '%s.inputTranslate'%mat3)
cmds.connectAttr('%s.rotate'%sel[0], '%s.inputRotate'%mat3)
cmds.connectAttr('%s.scale'%sel[0], '%s.inputScale'%mat3)

cmds.connectAttr('%s.matrixSum'%mat1, '%s.matrixIn[0]'%mat2)
cmds.connectAttr('%s.outputMatrix'%mat3, '%s.matrixIn[1]'%mat2)

cmds.connectAttr('%s.matrixSum'%mat2, '%s.inputMatrix'%mat4)

cmds.connectAttr('%s.outputTranslate'%mat4, '%s.translate'%nCam[0])
cmds.connectAttr('%s.outputRotate'%mat4, '%s.rotate'%nCam[0])
cmds.connectAttr('%s.outputScale'%mat4, '%s.scale'%nCam[0])

cmds.setAttr("%s.frozen"%mat3, 1)
