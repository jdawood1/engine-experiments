# Unreal Editor Python tools for batch asset operations.
# Enable plugins: "Editor Scripting Utilities" and "Python Editor Script Plugin".
import unreal, re

def _sanitize_base(name: str) -> str:
    base = re.sub(r'[\s\-]+', '_', name)
    base = re.sub(r'[^A-Za-z0-9_]', '', base)
    return base

def get_selected_assets():
    assets = unreal.EditorUtilityLibrary.get_selected_assets()
    if not assets:
        unreal.log_warning("No assets selected.")
    return assets

def rename_selected_assets(prefix: str = "SM_"):
    assets = get_selected_assets()
    count = 0
    for a in assets:
        try:
            # Only rename Static Meshes
            if not isinstance(a, unreal.StaticMesh):
                unreal.log(f"[rename] skip non-StaticMesh: {a.get_name()}")
                continue

            old_name = a.get_name()                       # e.g., "SM_Chair"
            base = _sanitize_base(old_name)               # "SM_Chair" or "Chair"

            # If it already has the prefix, skip cleanly
            if base.startswith(prefix):
                unreal.log(f"[rename] unchanged: {a.get_path_name()}")
                continue

            new_name = f"{prefix}{base}"                  # "SM_Chair"

            # Object path looks like "/Game/Folder/Asset.Asset"
            obj_path = a.get_path_name()
            package_path = obj_path.rsplit('.', 1)[0]     # "/Game/Folder/Asset"
            folder_path = package_path.rsplit('/', 1)[0]  # "/Game/Folder"
            new_obj_path = f"{folder_path}/{new_name}"    # "/Game/Folder/SM_Chair"

            if unreal.EditorAssetLibrary.rename_asset(obj_path, new_obj_path):
                count += 1
                unreal.log(f"[rename] {obj_path} -> {new_obj_path}")
            else:
                unreal.log_warning(f"[rename] failed: {obj_path}")
        except Exception as e:
            unreal.log_error(f"[rename] error on {a}: {e}")
    unreal.log(f"[rename] total renamed: {count}")

def setup_collision_selected(
        shape=unreal.ScriptingCollisionShapeType.BOX,
        trace=unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE
):
    assets = get_selected_assets()
    updated = 0
    for a in assets:
        try:
            if not isinstance(a, unreal.StaticMesh):
                unreal.log(f"[collision] skip non-StaticMesh: {a.get_name()}")
                continue

            # Set collision complexity on the mesh's BodySetup
            body_setup = a.get_editor_property("body_setup")
            if body_setup:
                body_setup.set_editor_property("collision_trace_flag", trace)
            else:
                unreal.log_warning(f"[collision] no BodySetup on {a.get_name()}")

            # Add simple collision (BOX/SPHERE/CAPSULE…)
            unreal.EditorStaticMeshLibrary.add_simple_collisions(
                static_mesh=a, shape_type=shape
            )

            updated += 1
            unreal.log(f"[collision] updated: {a.get_path_name()}")

        except Exception as e:
            unreal.log_warning(f"[collision] failed on {a.get_name()}: {e}")

    unreal.log(f"[collision] total updated: {updated}")

def save_modified_assets():
    assets = get_selected_assets()
    saved = 0
    eal = unreal.EditorAssetLibrary
    for a in assets:
        try:
            # save_loaded_asset() returns True only if it actually saved something
            if eal.save_loaded_asset(a):
                saved += 1
                unreal.log(f"[save] {a.get_path_name()}")
        except Exception as e:
            unreal.log_error(f"[save] error on {a}: {e}")
    if saved == 0:
        unreal.log("[save] No selected assets saved; saving /Game")
        eal.save_directory("/Game")
    unreal.log(f"[save] total saved: {saved}")
