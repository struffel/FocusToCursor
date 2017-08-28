bl_info = {
    "name": "Focus to cursor",
    "category": "Object",
    "author": "StruffelProductions (Lennart Demes)"
}

import bpy
import math
from mathutils import Vector

class FocusToCursor(bpy.types.Operator):
    """Camera Focus to 3d cursor"""
    bl_idname = "object.focus_to_cursor"
    bl_label = "Camera Focus to Cursor"
    bl_options ={'REGISTER', 'UNDO'}
    
    
    def execute(self, context):
        
        scene = context.scene  
        
        debug = False
        
        #camera
        obj_camera = bpy.context.scene.camera
        if obj_camera is None or obj_camera.type != 'CAMERA' :
            self.report({'ERROR'}, 'No active camera to set focus for!')
            return {'CANCELLED'}
        
        
        cameraLocation= obj_camera.location
        
        #3dcursor
        cursorLocation= bpy.context.scene.cursor_location
        
        #Camera plane
        
        cameraPlaneNormal = obj_camera.matrix_world.to_quaternion() * Vector((0.0, 0.0, -1.0))
        
        #printing
        if debug:
            print("VectorCamera:")
            print(cameraPlaneNormal[0])
            print(cameraPlaneNormal[1])
            print(cameraPlaneNormal[2])
            print("LocationCamera:")
            print(cameraLocation.x)
            print(cameraLocation.y)
            print(cameraLocation.z)
            print("LocationCursor:")
            print(cursorLocation.x)
            print(cursorLocation.y)
            print(cursorLocation.z)
        
        #Find d
        d = (cameraPlaneNormal[0]*cameraLocation.x + cameraPlaneNormal[1]*cameraLocation.y + cameraPlaneNormal[2]*cameraLocation.z)
        
        #Distance
        distance = (cameraPlaneNormal[0]*cursorLocation.x + cameraPlaneNormal[1]*cursorLocation.y + cameraPlaneNormal[2]*cursorLocation.z - d) / math.sqrt(cameraPlaneNormal[0]**2 + cameraPlaneNormal[1]**2 + cameraPlaneNormal[2]**2)
        
        #Set distance in camera
        obj_camera.data.dof_distance = distance

            
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(FocusToCursor.bl_idname) 
 
 

def register():
    bpy.utils.register_class(FocusToCursor)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    

    
def unregister():
    bpy.utils.unregister_class(FocusToCursor)
    
if __name__ == "__main__":
    register()