import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import tempfile
import os

def get_maya_main_window():
    """Get the Maya main window as a QtWidgets.QWidget instance."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class SimpleSceneVisualizerWindow(QtWidgets.QDialog):
    """A window to visualize different types of objects in a Maya scene."""
    
    def __init__(self, parent=get_maya_main_window()):
        super(SimpleSceneVisualizerWindow, self).__init__(parent)
        self.setWindowTitle("Create new scene based on previous")
        self.setMinimumSize(600, 500)
        self._setup_ui()
        self.refresh_scene()

    def _setup_ui(self):
        """Setup the UI components."""
        layout = QtWidgets.QVBoxLayout(self)
        self.tab_widget = QtWidgets.QTabWidget()
        layout.addWidget(self.tab_widget)

        self.list_widgets = {
            "Polygons": QtWidgets.QListWidget(),
            "Curves": QtWidgets.QListWidget(),
            "Lights": QtWidgets.QListWidget(),
            "Cameras": QtWidgets.QListWidget(),
            "Joints": QtWidgets.QListWidget(),
            "IK Handles": QtWidgets.QListWidget(),
            "Deformers": QtWidgets.QListWidget(),
            "Others": QtWidgets.QListWidget()
        }

        for category, widget in self.list_widgets.items():
            self.tab_widget.addTab(widget, category)

        # Add a button to create a new scene with selected items
        self.create_scene_button = QtWidgets.QPushButton("Create New Scene with Selected")
        self.create_scene_button.clicked.connect(self.create_new_scene_with_selected)
        layout.addWidget(self.create_scene_button)

    def refresh_scene(self):
        """Refresh the scene and update the list widgets."""
        for widget in self.list_widgets.values():
            widget.clear()

        categorized_objects = self._categorize_objects()
        for category, objects in categorized_objects.items():
            for obj in objects:
                obj_name = obj.split("|")[-1]
                item = QtWidgets.QListWidgetItem(f"{obj_name} ({cmds.objectType(obj)})")
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Unchecked)
                item.setData(QtCore.Qt.UserRole, obj)  # Store the full path
                self.list_widgets[category].addItem(item)

    def _categorize_objects(self):
        """Categorize objects in the scene."""
        categories = {
            "Polygons": [],
            "Curves": [],
            "Lights": [],
            "Cameras": [],
            "Joints": [],
            "IK Handles": [],
            "Deformers": [],
            "Others": []
        }

        type_to_category = {
            "mesh": "Polygons",
            "nurbsSurface": "Polygons",
            "subdiv": "Polygons",
            "nurbsCurve": "Curves",
            "light": "Lights",
            "ambientLight": "Lights",
            "directionalLight": "Lights",
            "pointLight": "Lights",
            "spotLight": "Lights",
            "areaLight": "Lights",
            "volumeLight": "Lights",
            "camera": "Cameras",
            "joint": "Joints",
            "ikHandle": "IK Handles",
            "deformer": "Deformers",
            "skinCluster": "Deformers",
            "blendShape": "Deformers",
            "cluster": "Deformers",
            "lattice": "Deformers",
            "nonLinear": "Deformers"
        }

        all_objects = cmds.ls(dag=True, long=True)
        for obj in all_objects:
            obj_type = cmds.objectType(obj)
            category = type_to_category.get(obj_type, "Others")
            categories[category].append(obj)

        return categories

    def create_new_scene_with_selected(self):
        """Create a new scene with the selected objects."""
        selected_objects = []
        for widget in self.list_widgets.values():
            for index in range(widget.count()):
                item = widget.item(index)
                if item.checkState() == QtCore.Qt.Checked:
                    selected_objects.append(item.data(QtCore.Qt.UserRole))

        if not selected_objects:
            QtWidgets.QMessageBox.warning(self, "Warning", "No objects selected.")
            return

        # Create a temporary file to store the selected objects
        temp_file = tempfile.NamedTemporaryFile(suffix='.mb', delete=False)
        temp_file.close()

        try:
            # Export selected objects to the temporary file
            cmds.select(selected_objects, replace=True)
            cmds.file(temp_file.name, force=True, options="v=0;", typ="mayaBinary", pr=True, es=True)

            # Create a new scene
            cmds.file(new=True, force=True)

            # Import objects from the temporary file
            cmds.file(temp_file.name, i=True, type="mayaBinary", ignoreVersion=True, ra=True, mergeNamespacesOnClash=False, namespace=":", options="v=0;", pr=True)

            QtWidgets.QMessageBox.information(self, "Success", "New scene created with selected objects.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to create new scene: {str(e)}")
        finally:
            # Clean up the temporary file
            os.unlink(temp_file.name)

        # Refresh the UI to reflect the new scene
        self.refresh_scene()

def show():
    """Show the SimpleSceneVisualizerWindow."""
    global simple_scene_visualizer
    try:
        simple_scene_visualizer.close()
        simple_scene_visualizer.deleteLater()
    except NameError:
        pass
    
    simple_scene_visualizer = SimpleSceneVisualizerWindow()
    simple_scene_visualizer.show()

if __name__ == "__main__":
    show()