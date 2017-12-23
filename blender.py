import bpy
import bmesh

obj = bpy.context.object;
if obj.mode == 'EDIT':
    bm = bmesh.from_edit_mesh(obj.data);
    # with open(save_path + "/blender_output.txt", "w") as f:
    #     f.write('Selected vertices index =' + '\r')
    cnt=0
    for v in bm.verts:
        if v.select:
            # print("v.index=",v.index)
            # f.write(str(v.index)+'\r')
            cnt =cnt + 1
    print("all selected vertices num="+str(cnt))