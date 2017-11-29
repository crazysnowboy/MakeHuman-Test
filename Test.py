# -*- coding: utf-8 -*
import sys
syspath = ["./", "./lib", "./apps", "./shared", "./apps/gui", "./core"]
syspath.extend(sys.path)
sys.path = syspath

import numpy as np
import math as M
from mayavi import mlab

from distutils.core import setup, Extension
import os.path
import module3d
import numpy as np
import log
import wavefront
from getpath import isSubPath, getPath


def WriteOBJ( path, vertexs, vertex_normals =0,triangles=0, texture_coordinate=0, vertex_color=0, tri_index_offset=0):
    print "write obj = ", path
    c_i = 0  # vertex color index
    with open(path, 'w') as test_txt:

        if hasattr(texture_coordinate, 'shape'):
            # line = 'mtllib texture_file.mtl\n'
            # line = 'mtllib 3DMM.mtl\n'
            # test_txt.write(line)
            for r in range(0, texture_coordinate.shape[0]):
                line = 'vt {} {}\n'.format(texture_coordinate[r, 0], texture_coordinate[r, 1])
                test_txt.write(line)
        if hasattr(vertexs, 'shape'):
            # vertexs = vertexs.astype('int32')

            for r in range(0, vertexs.shape[0]):
                if hasattr(vertex_color, 'shape'):
                    # With RGBA
                    line = 'v {} {} {} {} {} {} {}\n'.format(vertexs[r, 0], vertexs[r, 1], vertexs[r, 2],
                                                             vertex_color[c_i, 2], vertex_color[c_i, 1],
                                                             vertex_color[c_i, 0], 255)
                    c_i = c_i + 1
                else:
                    # Without RGBA
                    line = 'v {} {} {}\n'.format(vertexs[r, 0], vertexs[r, 1], vertexs[r, 2])

                if hasattr(vertex_normals, 'shape'):
                    line = line + 'vn {} {} {}\n'.format(vertex_normals[r, 0], vertex_normals[r, 1], vertex_normals[r, 2])

                test_txt.write(line)
        if hasattr(triangles, 'shape'):
            triangles = triangles.astype('int32')
            for r in range(0, triangles.shape[0]):
                triangles[r, :] = triangles[r, :] + tri_index_offset
                line = 'f {}//{} {}//{} {}//{}\n'.format(triangles[r, 0], triangles[r, 0],
                                                      triangles[r, 1], triangles[r, 1],
                                                      triangles[r, 2], triangles[r, 2])  # if with texture coordinate
                test_txt.write(line)
                line = 'f {}//{} {}//{} {}//{}\n'.format(triangles[r, 0], triangles[r, 0],
                                                      triangles[r, 2], triangles[r, 2],
                                                      triangles[r, 3], triangles[r, 3])  # if with texture coordinate
                test_txt.write(line)

                # line = 'f {} {} {}\n'.format(triangles[r,0],triangles[r,1],triangles[r,2])
                # test_txt.write(line)
                # line = 'f {} {} {}\n'.format(triangles[r,0],triangles[r,2],triangles[r,3])
                # test_txt.write(line)

def ReadOBJ(file_path):
    OFF_file = open(file_path, 'r')
    lines = OFF_file.readlines()  # 读取全部内容
    total_lines_num = len(lines)
    # print "total_lines_num = ",total_lines_num

    vertexs = np.empty(0)
    vertexs_colors = np.empty(0)
    triangles = np.empty(0)
    texture_coor = np.empty(0)
    vertexs_normals = np.empty(0)

    if total_lines_num > 0:

        for index in range(0, total_lines_num, 1):
            line = lines[index].split()
            if len(line) >2:
                if line[0] == 'v':
                    x = float(line[1])
                    y = float(line[2])
                    z = float(line[3])
                    vertexs = np.append(vertexs, np.array([x, y, z]))
                    if len(line) >4:
                        r = float(line[6])
                        g = float(line[5])
                        b = float(line[4])
                        vertexs_colors = np.append(vertexs_colors, np.array([r, g, b]))


                if line[0] == 'vn':
                    nx = float(line[1])
                    ny = float(line[2])
                    nz = float(line[3])
                    vertexs_normals = np.append(vertexs_normals, np.array([nx, ny, nz]))

                if line[0] == 'f':
                    tri_1 = int(line[1].split('/')[0])
                    tri_2 = int(line[2].split('/')[0])
                    tri_3 = int(line[3].split('/')[0])
                    triangles = np.append(triangles, np.array([tri_1, tri_2, tri_3]))

                if line[0] == 'vt':
                    coor_1 = float(line[1])
                    coor_2 = float(line[2])
                    texture_coor = np.append(texture_coor, np.array([coor_1, coor_2]))

        vertexs = vertexs.reshape(vertexs.shape[0] / 3, 3)

        if vertexs_colors.shape[0]>3:
            vertexs_colors = vertexs_colors.reshape(vertexs_colors.shape[0] / 3, 3)
        if vertexs_normals.shape[0]>3:
            vertexs_normals = vertexs_normals.reshape(vertexs_normals.shape[0] / 3, 3)

        triangles = triangles.reshape(triangles.shape[0] / 3, 3).astype('int32') - 1

        texture_coor = texture_coor.reshape(texture_coor.shape[0] / 2, 2)
        return vertexs, triangles, texture_coor,vertexs_normals,vertexs_colors

def unpackStringList(text, index):
    strings = []
    last = None
    for i in index:
        if last is not None:
            name = text[last:i].tostring()
            strings.append(name)
        last = i
    if last is not None:
        name = text[last:].tostring()
        strings.append(name)

    return strings

def loadBinaryMeshTest(path):


    npzfile = np.load(path)

    if 'MAX_FACES' in npzfile:
        # Set pole count if stored
        MAX_FACES = int(npzfile['MAX_FACES'][0])
        print "MAX_FACES = ",MAX_FACES

    #log.debug('loadBinaryMesh: loading arrays')
    coord = npzfile['coord']

    texco = npzfile['texco']

    fvert = npzfile['fvert']
    fuvs = npzfile['fuvs'] if 'fuvs' in npzfile.files else None
    group = npzfile['group']

    vface = npzfile['vface'][:,:MAX_FACES]
    nfaces = npzfile['nfaces']

    #log.debug('loadBinaryMesh: loaded arrays')

    fgstr = npzfile['fgstr']
    fgidx = npzfile['fgidx']
    for name in unpackStringList(fgstr, fgidx):
        print "name of face group= ",name

def loadBinaryMesh(obj, path):
    log.debug("Loading binary mesh %s.", path)
    #log.debug('loadBinaryMesh: np.load()')

    npzfile = np.load(path)

    if 'MAX_FACES' in npzfile:
        # Set pole count if stored
        obj.MAX_FACES = int(npzfile['MAX_FACES'][0])

    #log.debug('loadBinaryMesh: loading arrays')
    coord = npzfile['coord']
    obj.setCoords(coord)

    texco = npzfile['texco']
    obj.setUVs(texco)

    fvert = npzfile['fvert']
    fuvs = npzfile['fuvs'] if 'fuvs' in npzfile.files else None
    group = npzfile['group']
    obj.setFaces(fvert, fuvs, group, skipUpdate=True)

    obj.vface[:,:] = npzfile['vface'][:,:obj.MAX_FACES]
    obj.nfaces = npzfile['nfaces']

    #log.debug('loadBinaryMesh: loaded arrays')

    fgstr = npzfile['fgstr']
    fgidx = npzfile['fgidx']
    for name in unpackStringList(fgstr, fgidx):
        obj.createFaceGroup(name)
    # del fgstr, fgidx

    #log.debug('loadBinaryMesh: unpacked facegroups')

    obj.calcNormals()
    #log.debug('loadBinaryMesh: calculated normals')

    obj.updateIndexBuffer()
    #log.debug('loadBinaryMesh: built index buffer for rendering')

    return npzfile
def ReadFileTest():
    obj = module3d.Object3D("base.npz")
    npzfile = loadBinaryMesh(obj,"/home/collin/Documents/MyProjects/FromGithub/makehuman/full-version/makehuman/data/3dobjs/base.npz")
    print "obj = ",obj
    print "obj.coord.shape = ", obj.coord.shape
    print "obj.vnorm.shape = ", obj.vnorm.shape
    print "obj.vtang.shape = ", obj.vtang.shape
    print "obj.color.shape = ", obj.color.shape
    print "obj.vface.shape = ", obj.vface.shape
    print "obj.nfaces.shape = ", obj.nfaces.shape


    print "obj.texco.shape = ", obj.texco.shape
    print "obj.utexc.shape = ", obj.utexc


    print "obj.fvert.shape = ", obj.fvert.shape
    print "obj.fnorm.shape = ", obj.fnorm.shape
    print "obj.fuvs.shape = ", obj.fuvs.shape
    print "obj.group.shape = ", obj.group.shape
    print "obj.face_mask.shape = ", obj.face_mask.shape


    print "obj.group = ", obj.group

    group_1 = obj.group[obj.group==1]

    print "group_1.shape = ", group_1.shape


    false_mask_false = obj.face_mask[obj.face_mask==False]
    if hasattr(false_mask_false,"shape"):
        print "false_mask_false = ", false_mask_false.shape

    false_mask_true = obj.face_mask[obj.face_mask == True]
    if hasattr(false_mask_true, "shape"):
        print "false_mask_true = ", false_mask_true.shape

    False_Group = obj.group[obj.face_mask == False]
    Group_id = np.unique(False_Group)
    print "false group id = ",Group_id

    True_Group = obj.group[obj.face_mask == True]
    Group_id = np.unique(False_Group)
    print "true group id = ",Group_id

    obj.face_mask=True
    # print "npzfile files =",npzfile.files
    #
    # for file_name in npzfile.files:
    #     print file_name,"=",npzfile[file_name]
    #
    # print "length  = ",len(npzfile["fgstr"])

def ReadFileSaveObj():
    obj = module3d.Object3D("base.npz")
    npzfile = loadBinaryMesh(obj,"/home/collin/Documents/MyProjects/FromGithub/makehuman/full-version/makehuman/data/3dobjs/base.npz")
    print "obj = ",obj
    print "obj.coord.shape = ", obj.coord.shape
    print "obj.vnorm.shape = ", obj.vnorm.shape
    print "obj.vtang.shape = ", obj.vtang.shape
    print "obj.color.shape = ", obj.color.shape
    print "obj.vface.shape = ", obj.vface.shape
    print "obj.nfaces.shape = ", obj.nfaces.shape


    print "obj.texco.shape = ", obj.texco.shape
    print "obj.utexc.shape = ", obj.utexc


    print "obj.fvert.shape = ", obj.fvert.shape
    print "obj.fnorm.shape = ", obj.fnorm.shape
    print "obj.fuvs.shape = ", obj.fuvs.shape
    print "obj.group.shape = ", obj.group.shape
    print "obj.face_mask.shape = ", obj.face_mask.shape

    vertices = obj.coord
    vertices_normals = obj.vnorm
    uvs = obj.texco
    colors = obj.color

    triangles = obj.fvert[obj.group==0,:]

    print "triangles.shape = ",triangles.shape

    WriteOBJ("crazy_data/human.obj",vertices,vertices_normals,triangles,tri_index_offset=1)



def Test1():
    if "good" in "bad boy is never been a good man":
        print "yes"


if __name__ == '__main__':
    ReadFileSaveObj()

