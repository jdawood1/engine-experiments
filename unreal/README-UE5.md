# Unreal (UE5) Editor Automation
Enable **Editor Scripting Utilities** + **Python Editor Script Plugin**.
Open UE5 → Python window and run:

```py
import sys
sys.path.append(r"/absolute/path/to/unreal/EngineExperimentsUE5/Python")
import asset_tools as at
at.rename_selected_assets(prefix="SM_")
at.setup_collision_selected()
at.save_modified_assets()
```
Select some Static Mesh assets in Content Browser before running.
