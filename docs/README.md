## Unity demo
![Unity demo](docs/unity-demo.gif)

### UE5: Batch Collision Setup (Python)

**Before** (no simple collision; Project Default)  
![Before](docs/before-settings.png)

**Automation Output**  
![Output Log](docs/outputlog-automation.png)

**After** (simple collision added; Use Complex As Simple)  
![After](docs/after-settings.png)

Run in UE5 Python:
```py
import asset_tools as at
at.setup_collision_selected()
at.save_modified_assets()
