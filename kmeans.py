###
# Returns the centroids of a set of points and draws lines from each point to its respoective centroid
###

import bpy
import bmesh
import numpy as np
from scipy.cluster.vq import vq, kmeans2, whiten
from collections import defaultdict


###
# Initial variables
###

# number of centroids

n = 4

# frame range

start = 1

end = 61


###
# Duplicate object
###

def duplicateObject(scene, name, copyfrom):

    copyobj = bpy.data.objects[copyfrom]

    # Create new mesh
    mesh = bpy.data.meshes.new(name)

    # Get material data

    mat = copyobj.active_material
    mat_i = copyobj.active_material_index

    # Create new object associated with the mesh
    ob_new = bpy.data.objects.new(name, mesh)

    # Copy data block from the old object into the new object
    ob_new.data = copyobj.data.copy()
    ob_new.scale = copyobj.scale
    ob_new.location = copyobj.location
    ob_new.material_slots[mat_i].material = mat

    # Link new object to the given scene and select it
    scene.objects.link(ob_new)

    bpy.context.scene.objects.active = ob_new

    return ob_new

###
# Delete object
###

def deleteObject(name):

    # Select object
    bpy.data.objects[name].select = True

    # Delete the object
    bpy.ops.object.delete()

###
# Render loop
###

for step in range(start, end):

    duplicateObject(bpy.context.scene, 'Copy', 'Points')

    # get active mesh

    mesh = bpy.context.active_object.data

    bpy.ops.object.mode_set(mode='EDIT')

    bm = bmesh.from_edit_mesh(mesh)

    verts = [vert.co for vert in bm.verts]

    # calculate centroids and code

    vertices = np.array(verts)

    step_length = int(len(verts)/n)

    s = (n,3)

    initial_points = np.zeros(s)

    for i in range(n):
        initial_points[i] = vertices[i]

    codebook, distortion = kmeans2(vertices, initial_points, step + 1)

    centroids = codebook.tolist()

    code = vq(vertices, codebook)[0].tolist()

    # create list of vertices and edges

    vertexList = verts + centroids

    edgeList = []

    for index, item in enumerate(code):
        edgeList.append([index, int(len(verts)+item)])

    # delete old vertices

    bm.verts.ensure_lookup_table()

    vert_list = [v for v in bm.verts]

    bmesh.ops.delete(bm, geom=vert_list, context=1)

    # add new vertices and edges

    for v in verts:
        bm.verts.new(v)

    for c in centroids:
        bm.verts.new(c)

    bm.verts.ensure_lookup_table()

    for i in edgeList:
        bm.edges.new((bm.verts[i[0]], bm.verts[i[1]]))

    bmesh.update_edit_mesh(mesh, True)

    bpy.ops.object.mode_set(mode='OBJECT')

    # Render frame

    bpy.context.scene.frame_set(step)

    bpy.data.scenes["Scene"].render.filepath = '/Users/sean/Desktop/Frames/frame_%d.png' % step
    bpy.ops.render.render( write_still=True )

    # Delete duplicate

    deleteObject('Copy')
