# Create new scene based previous in Autodesk Maya 3D

This script provides a custom Maya tool to visualize and manage various types of objects within a Maya scene. The tool categorizes objects into tabs (e.g., Polygons, Curves, Lights) and allows you to select specific objects to export into a new Maya scene.

## How the Code Works

- **UI Creation**: The script creates a custom dialog window (`SimpleSceneVisualizerWindow`) using PySide2. This window displays tabs that categorize different types of objects in the Maya scene (e.g., Polygons, Curves, Lights).
  
- **Object Categorization**: The script scans the scene for objects and categorizes them based on their type (e.g., meshes, curves, lights).

- **Scene Refreshing**: The UI is refreshed to display all objects in their respective categories, allowing you to browse and select them.

- **New Scene Creation**: After selecting objects, you can click a button to export these selected objects into a new Maya scene.

## How to Run the Script

1. **Ensure Dependencies**: The script relies on Maya's `maya.cmds`, `maya.OpenMayaUI`, and the PySide2 library. Ensure these are available in your environment.

2. **Execute the Script**: Copy the script into Maya's script editor or save it as a Python file (`.py`).

3. **Run the Script**: Execute the script within Maya. The `SimpleSceneVisualizerWindow` will appear, allowing you to interact with and manage scene objects.

```python
if __name__ == "__main__":
    show()
