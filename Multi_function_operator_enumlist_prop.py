bl_info = {
    "name": "Test Addon",
    "author": "Your Name Here",
    "version": (0, 0, 1),
    "blender": (2, 92, 0),
    "location": "View3D > UI > Test Panel",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "category": "Development",
    "support": "TESTING"
}

import bpy


class TEST_PG(bpy.types.PropertyGroup):
    proplist: bpy.props.EnumProperty(
        items=(
            ("MESH_PLANE", "Plane", "primitive_plane_add"),
            ("MESH_CUBE", "Cube", "primitive_cube_add"),
            ("MESH_CIRCLE", "Circle", "primitive_circle_add"),
            ("MESH_UVSPHERE", "UV Sphere", "primitive_uv_sphere_add"),
            ("MESH_ICOSPHERE", "Ico Sphere", "primitive_ico_sphere_add"),
            ("MESH_CYLINDER", "Cylinder", "primitive_cylinder_add"),
            ("MESH_CONE", "Cone", "primitive_cone_add"),
            ("MESH_TORUS", "Torus", "primitive_torus_add"),
            ("MESH_MONKEY", "Monkey", "primitive_monkey_add"),
            ),
        name="proplist",
        description="Selectable properties to add",
        default="MESH_PLANE",
        )


class PROPLIST_OT_next(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "property.next"
    bl_label = "Move to next item in property list"

    def execute(self, context):
        props = context.scene.MyPropertyGroup
        print('-- PROPLIST_OT_next pressed --')
        try:
            idx = props['proplist']
        except KeyError:
            props.proplist = props.proplist
            idx = props['proplist']
        list_len = len(props.bl_rna.properties['proplist'].enum_items)
        idx += 1
        if idx == list_len:
            idx = 0
        props['proplist'] = idx
        return {'FINISHED'}


class PROPLIST_OT_prev(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "property.previous"
    bl_label = "Move to previous item in property list"

    def execute(self, context):
        props = context.scene.MyPropertyGroup
        print('-- PROPLIST_OT_prev pressed --')
        try:
            idx = props['proplist']
        except KeyError:
            props.proplist = props.proplist
            idx = props['proplist']
        list_len = len(props.bl_rna.properties['proplist'].enum_items)
        idx -= 1
        if idx < 0:
            idx = list_len-1
        props['proplist'] = idx
        return {'FINISHED'}


class MESH_OT_add_item(bpy.types.Operator):
    """add selected mesh"""
    bl_idname = "mesh.add_item"
    bl_label = "Add mesh"
    bl_options = {'REGISTER', 'UNDO'}

    item_type: bpy.props.StringProperty(
        name="Mesh Primitive",
        description="Type of mesh primitive to add",
        default="primitive_plane_add",
    )

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        cmd = f"bpy.ops.mesh.{self.item_type}()"
        print(cmd)
        eval(cmd)
        return {'FINISHED'}


class VIEW3D_PT_test():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Test Panel"


class TEST_PT_sub_01(VIEW3D_PT_test, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_test_panel_1"
    bl_label = "Test Panel 1"

    def draw(self, context):
        props = context.scene.MyPropertyGroup
        items = props.bl_rna.properties['proplist'].enum_items
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)
        col.prop(props, "proplist")
        enum = items[props.proplist]
        col.label(text=f"Identifier: {enum.identifier}", icon=enum.identifier)
        col.label(text=f"Name: {enum.name}")
        col.label(text=f"Description: {enum.description}")
        row = col.row()
        row.operator("property.previous", icon='TRIA_LEFT', text="")
        add_op = row.operator(
            'mesh.add_item',
            text=enum.name,
            icon=enum.identifier,
            )
        add_op.item_type = enum.description
        row.operator("property.next", icon='TRIA_RIGHT', text="")


classes = [
    TEST_PG,
    PROPLIST_OT_prev,
    PROPLIST_OT_next,
    MESH_OT_add_item,
    TEST_PT_sub_01,
    ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.MyPropertyGroup = bpy.props.PointerProperty(
            type=TEST_PG)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.MyPropertyGroup

if __name__ == "__main__":
    register()
