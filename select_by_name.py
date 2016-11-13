import bpy
from bpy.props import *

bl_info = {
    "name": "Select by name",
    "description": "Selects all objects with a given name",
    "author": "Sean Kelley",
    "version": (0, 0, 1),
    "blender": (2, 75, 0),
    "location": "View3D",
    "warning": "",
    "wiki_url": "",
    "category": "Object" }
 
theBool = False
theString = "Name..."
scene = bpy.context.scene
 
class DialogOperator(bpy.types.Operator):
    bl_idname = "object.dialog_operator"
    bl_label = "Select by name"
    
    mesh = BoolProperty(name="Mesh")
    curve = BoolProperty(name="Curve")
    my_string = StringProperty(name="Object name")
 
    def execute(self, context):

        for ob in scene.objects:
            if self.mesh == 1 and ob.type == 'MESH' and ob.name.startswith(self.my_string):
                ob.select = True
            if self.curve == 1 and ob.type == 'CURVE' and ob.name.startswith(self.my_string):
                ob.select = True
            else: 
                pass
        
        # Debugging 
        message = "%d, %d, '%s'" % (self.mesh, self.curve, self.my_string)
        self.report({'INFO'}, message)
        print(message)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        global theFloat, theBool, theString, theEnum
        self.mesh = theBool
        self.curve = theBool
        self.my_string = theString
        return context.window_manager.invoke_props_dialog(self)
 
 
bpy.utils.register_class(DialogOperator)
 
# Invoke the dialog when loading
bpy.ops.object.dialog_operator('INVOKE_DEFAULT')
 
#
#    Panel in tools region
#
class DialogPanel(bpy.types.Panel):
    bl_label = "Selection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
 
    def draw(self, context):
        global theFloat, theBool, theString, theEnum
        theBool = True
        theString = "Name..."
        self.layout.operator("object.dialog_operator")
 
#
#	Registration
bpy.utils.register_module(__name__)