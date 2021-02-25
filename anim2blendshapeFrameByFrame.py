import maya.api.OpenMaya as om
import maya.cmds as cmds

init_frame = 330
end_frame = 350

sel = cmds.ls(sl=True, l=True)[0]
cmds.currentTime( init_frame )
base_shape = cmds.duplicate( sel, n='base#' )[0]
msel = om.MSelectionList()
msel.add( sel )
mesh = om.MFnMesh( msel.getDagPath(0) )
ori_pnt = mesh.getPoints( om.MSpace.kWorld )

tar_mesh = []
tar_name = 'frameBlend'
cmds.select( cl=True )
#jnt = cmds.joint(p=[0,0,0], n='root_{}'.format(tar_name) )
#cmds.skinCluster(jnt, base_shape, tsb=True, ibp=True, mi=1 ) 
bls = cmds.blendShape(base_shape, frontOfChain=True, n='bs_{}'.format(tar_name), o='world')[0]
idx = 0
attr_count = end_frame - init_frame
for s in range(init_frame+1, end_frame+1):
    msel = om.MSelectionList( )
    msel.add( sel )
    mesh = om.MFnMesh( msel.getDagPath(0) )
    o_pnt = mesh.getPoints( om.MSpace.kWorld )
    
    cmds.currentTime( s )
    
    next_shape = cmds.duplicate( sel ,  n='{}{}'.format(tar_name, s) )[0]
    msel = om.MSelectionList( )
    msel.add( next_shape )
    mesh = om.MFnMesh( msel.getDagPath(0) )
    n_pnt = mesh.getPoints( om.MSpace.kWorld )
    
    new_pnt = []
    for i in range(len(ori_pnt)):
        o_pos = n_pnt[i] - o_pnt[i]
        n_pos = ori_pnt[i] + o_pos
        new_pnt.append( n_pos )
        
    mesh.setPoints(new_pnt, om.MSpace.kWorld )
    tar_mesh.append( next_shape )
    

    cmds.blendShape( bls, e=True, target=(base_shape, attr_count - idx , next_shape, 1.0) )
    cmds.setKeyframe( '{}.{}'.format( bls, '{}{}'.format(tar_name, s) ), itt='linear', ott='linear', v=0, t=( s-1,s-1 ) )
    cmds.setKeyframe( '{}.{}'.format( bls, '{}{}'.format(tar_name, s) ), itt='linear', ott='linear', v=1, t=( s,s ) )
    cmds.delete( next_shape )
    idx += 1
