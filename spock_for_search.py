bl_info = {
    "name": "Spock for Search",
    "author": "Julius Hilker julius@undruck.de",
    "version": (0, 1),
    "blender": (2, 75, 0),
    "location": "Texteditor",
    "description": "A new, advanced way of searching Text. With special Tools for classes and definitions.",
    "warning": "You might encounter some Issues. Please report... also Earth is in danger. Call the Doctor!",
    "wiki_url": "",
    "category": "Development",
    "support": "TESTING",
    "wiki_url":"http://spocktools.blogspot.de/",
    }


import bpy
import os
import re
import random



class spocks_set_line(bpy.types.Operator):
    bl_idname = "object.spocks_set_line"
    bl_label = "Minimal Operator"
    line = bpy.props.IntProperty(name="line")
    def execute(self, context):
        bpy.ops.text.jump(line=self.line)
        bpy.ops.text.select_line()
        return {'FINISHED'}


      
class spocks_search_browser(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Spock for Search"
    bl_idname = "spocks_search_browser"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_context = "scene"
   

    def draw(self, context):
        os.system("cls")
        
        st = context.space_data
        text = st.text
        name = text.name
        txt = bpy.data.texts[name]
        results=0
        cat = context.scene.spock_search_enum
        search = context.scene.spock_advanced_search  
        sub_filter = False   
        
        layout = self.layout
        layout.label(str(random.randint(0,100)))
        box_up = layout.box()
        result_box = layout.box()       
        
        split = box_up.split(percentage=.7)       
        split.prop(context.scene, "spock_advanced_search",icon="VIEWZOOM")
        split.prop(context.scene, "spock_search_enum")
                
        
        search_pattern = {"Alles":search,"Funktionen":'def(.*)(?=:)',"Klassen":'class(.*)(?=:)'}   
         
        if search=="" and cat=="Alles":  
            go = False
            pass
        elif search=="" and cat!="Alles":
            go = True
            pass
        elif search != "" and cat=="Alles":
            go=True
            pass
        elif search != "" and cat!="Alles":
            go=True
            sub_filter=True
            pass
        
        
        
        
        
        
        if go==True:
            
            
            current_line = 1
            for i in txt.lines:               
                filter = re.search(search_pattern[cat],i.body)    
                if str(filter) !="None":
                    show_result=True

                    if sub_filter==True:
                        filter2 = re.search(search,i.body)  
                        if str(filter2)!="None":      
                            show_result=True
                            pass
                        else:
                            show_result=False
                        pass
                    
                    if show_result==True:
                        results+=1
                        eo = result_box.split(percentage=.1)
                        eo.operator("object.spocks_set_line",str(current_line),emboss=True).line=current_line
                        eo.operator("object.spocks_set_line",i.body,emboss=True).line=current_line
                        pass
                    pass
                
                current_line+=1
                  
                
                    
                    
        
        
        
        
        
        
        if results==0 and cat!="Alles":
            result_box.label("No Search Results.")
            pass

            
            





def register():

    bpy.utils.register_class(spocks_set_line)
    bpy.utils.register_class(spocks_search_browser)


    bpy.types.Scene.spock_advanced_search = bpy.props.StringProperty \
      (
        name = "",
        description = "Search a fucntion",
        default = ""
      )
    
    bpy.types.Scene.spock_search_enum = bpy.props.EnumProperty \
      (
        name = "Search:",
        items = [('Alles', 'All', 'all'), 
                 ('Klassen', 'Classes', 'Classes'),
                 ('Funktionen', 'Functions', 'Functions')
                 ],
        
      )
      

      



def unregister():
    bpy.utils.unregister_class(spocks_class_browser)
    bpy.utils.unregister_class(spocks_function_browser)
    bpy.utils.unregister_class(spocks_set_line)
  



if __name__ == "__main__":
    register()
