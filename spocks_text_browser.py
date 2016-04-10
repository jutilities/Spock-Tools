bl_info = {
    "name": "Spocks Text Browser",
    "author": "Julius Hilker julius@undruck.de",
    "version": (0, 2),
    "blender": (2, 75, 0),
    "location": "Texteditor",
    "description": "A simple Browser for internal Textfiles in the Properties Panel of the text editor",
    "warning": "Earth is in danger. Call the Doctor!",
    "wiki_url": "",
    "category": "Development",
    }


import bpy
import os



class spocks_file_operator(bpy.types.Operator):
    """Spocks Operator for files, delete, new ... stuff like that."""
    bl_idname = "object.spocks_file_operator"
    bl_label = "Spocks File Operator"
    action = bpy.props.StringProperty(name="action")
    file = bpy.props.StringProperty(name="file")
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if self.action=="ask":
            bpy.context.scene.spocks_question=True
            pass
        elif self.action=="no":
            bpy.context.scene.spocks_question=False
            pass
        elif self.action=="yes":
            bpy.ops.text.unlink()
            #print("delete",self.action)
            bpy.context.scene.spocks_question=False
            pass
        elif self.action=="new":
            bpy.ops.text.new()
            pass
        elif self.action[0]=="l":
            a = self.action

            
            context.space_data.text = bpy.data.texts[self.action[2:]]
        return {'FINISHED'}


class spocks_text_navigator(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Spocks Text Browser"
    bl_idname = "spocks_text_navigator"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_context = "scene"
   

    def draw(self, context):
        layout = self.layout
        st = context.space_data
        text = st.text
        x = bpy.data.texts
        
        a=0
        
        
        if bpy.context.scene.spocks_question==False:
            
            
            
            toolbox = layout.box()
            
            cmd = toolbox.row()

            search = context.scene.spock_search_file
            

            cmd.operator("text.new","",icon="NEW")
            cmd.operator("text.open","",icon="FILESEL")
            cmd.operator("text.save_as","",icon="SAVE_AS")
            cmd.operator("text.save","",icon="FILE_TICK")
            cmd.operator("text.make_internal","",icon="APPEND_BLEND")
            cmd.operator("text.reload","",icon="FILE_REFRESH")
            cmd.operator("text.run_script","",icon="PLAY")
            cmd.prop(context.scene, "spock_search_file",icon="VIEWZOOM")
            box = layout.box()
            
            row={}
            results=0
            for i in x:
                
                
                result = i.name[0:len(search)]
                
                
                
                label = i.name
                    
                row[a] = box.split(percentage=.9,align=True)
                row[a].scale_y=1.0
                
                if result == search:
                    results+=1
                    if i.name == text.name:
                        #row[a].prop(context.scene, "spock_fname",icon="SPACE2")
                        row[a].operator("object.spocks_file_operator",i.name,icon="SPACE2",emboss=False).action="l "+i.name
                        row[a].operator("object.spocks_file_operator","",icon="X_VEC",emboss=False).action="ask"
                    
                        pass
                    else:
                        row[a].operator("object.spocks_file_operator",i.name,icon="SPACE3",emboss=False).action="l "+i.name
                    
                    
                    
                    a+=1
                    pass
                
            if results==0:
                row[a].label("Nothing Found here",i.name,icon="SPACE3")
                pass
                    
            pass
        
        else:
            layout.label("You are about to delete the file: "+text.name)

            layout.label("Are you sure?")
            rowq=layout.row()
            rowq.operator("object.spocks_file_operator","Yes").action="yes"
            rowq.operator("object.spocks_file_operator","No").action="no"
           
        #for i in x.lines:
            #print(i.body)
        
        #scene = context.scene

        # Create a simple row.
        #layout.template_list("MATERIAL_UL_matslots_example", "", obj, "material_slots", obj, "active_material_index")

        


def register():
    bpy.utils.register_class(spocks_text_navigator)

    bpy.utils.register_class(spocks_file_operator)


    
    bpy.types.Scene.spocks_question = bpy.props.BoolProperty \
    (
        name = "save_question",
        description = "Are you sure?",
        default = False
    )
    
    bpy.types.Scene.spock_fname = bpy.props.StringProperty \
      (
        name = "",
        description = "My description",
        default = "None"
      )
      
      
          
    bpy.types.Scene.spock_search_file = bpy.props.StringProperty \
      (
        name = "",
        description = "Filter your Textblocks",
        default = ""
      )
    


def unregister():
    bpy.utils.unregister_class(spocks_text_navigator)
    bpy.utils.unregister_class(spocks_file_operator)



if __name__ == "__main__":
    register()
