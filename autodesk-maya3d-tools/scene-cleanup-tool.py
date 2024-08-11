import maya.cmds as cmds

def find_empty_groups():
    empty_groups = []
    all_groups = cmds.ls(type='transform')
    for group in all_groups:
        children = cmds.listRelatives(group, children=True)
        if not children:
            empty_groups.append(group)
    return empty_groups

def find_unused_nodes():
    unused_nodes = []
    all_nodes = cmds.ls()
    for node in all_nodes:
        if not cmds.listConnections(node):
            unused_nodes.append(node)
    return unused_nodes

def find_history():
    history_nodes = []
    all_nodes = cmds.ls()
    for node in all_nodes:
        history = cmds.listHistory(node)
        if history:
            history_nodes.extend(history)
    return list(set(history_nodes))  # Remove duplicates

def find_non_deformer_history():
    non_deformer_history = []
    all_nodes = cmds.ls()
    for node in all_nodes:
        history = cmds.listHistory(node)
        if history:
            for hist_node in history:
                if cmds.nodeType(hist_node) not in ['skinCluster', 'blendShape', 'cluster']:
                    non_deformer_history.append(hist_node)
    return list(set(non_deformer_history))  # Remove duplicates

def find_orphaned_nodes():
    orphaned_nodes = []
    all_nodes = cmds.ls()
    for node in all_nodes:
        if not cmds.listRelatives(node, parent=True):
            orphaned_nodes.append(node)
    return orphaned_nodes

def show_info(info_type):
    if info_type == "Empty Groups":
        info = find_empty_groups()
    elif info_type == "Unused Nodes":
        info = find_unused_nodes()
    elif info_type == "History":
        info = find_history()
    elif info_type == "Non-Deformer History":
        info = find_non_deformer_history()
    elif info_type == "Orphaned Nodes":
        info = find_orphaned_nodes()
    
    cmds.scrollField('infoField', edit=True, text="\n".join(info) if info else "None")

def delete_info(info_type):
    if info_type == "Empty Groups":
        info = find_empty_groups()
    elif info_type == "Unused Nodes":
        info = find_unused_nodes()
    elif info_type == "History":
        info = find_history()
    elif info_type == "Non-Deformer History":
        info = find_non_deformer_history()
    elif info_type == "Orphaned Nodes":
        info = find_orphaned_nodes()
    
    if info:
        cmds.delete(info)
        cmds.scrollField('infoField', edit=True, text=f"{info_type} deleted.")
    else:
        cmds.scrollField('infoField', edit=True, text=f"No {info_type} to delete.")

def show_cleanup_window():
    if cmds.window("cleanupWindow", exists=True):
        cmds.deleteUI("cleanupWindow")
    
    window = cmds.window("cleanupWindow", title="Scene Cleanup Tool", widthHeight=(400, 300))
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    
    # Empty Groups Tab
    empty_groups_tab = cmds.columnLayout(adjustableColumn=True)
    cmds.button(label="Show Empty Groups", command=lambda x: show_info("Empty Groups"))
    cmds.button(label="Delete Empty Groups", command=lambda x: delete_info("Empty Groups"))
    cmds.setParent('..')
    
    # Unused Nodes Tab
    unused_nodes_tab = cmds.columnLayout(adjustableColumn=True)
    cmds.button(label="Show Unused Nodes", command=lambda x: show_info("Unused Nodes"))
    cmds.button(label="Delete Unused Nodes", command=lambda x: delete_info("Unused Nodes"))
    cmds.setParent('..')
    
    # History Tab
    history_tab = cmds.columnLayout(adjustableColumn=True)
    cmds.button(label="Show History", command=lambda x: show_info("History"))
    cmds.button(label="Delete History", command=lambda x: delete_info("History"))
    cmds.setParent('..')
    
    # Non-Deformer History Tab
    non_deformer_history_tab = cmds.columnLayout(adjustableColumn=True)
    cmds.button(label="Show Non-Deformer History", command=lambda x: show_info("Non-Deformer History"))
    cmds.button(label="Delete Non-Deformer History", command=lambda x: delete_info("Non-Deformer History"))
    cmds.setParent('..')
    
    # Orphaned Nodes Tab
    orphaned_nodes_tab = cmds.columnLayout(adjustableColumn=True)
    cmds.button(label="Show Orphaned Nodes", command=lambda x: show_info("Orphaned Nodes"))
    cmds.button(label="Delete Orphaned Nodes", command=lambda x: delete_info("Orphaned Nodes"))
    cmds.setParent('..')
    
    cmds.tabLayout(tabs, edit=True, tabLabel=(
        (empty_groups_tab, 'Empty Groups'),
        (unused_nodes_tab, 'Unused Nodes'),
        (history_tab, 'History'),
        (non_deformer_history_tab, 'Non-Deformer History'),
        (orphaned_nodes_tab, 'Orphaned Nodes')
    ))
    
    cmds.scrollField('infoField', editable=False, wordWrap=True, height=200)
    
    cmds.showWindow(window)

# Run the tool
show_cleanup_window()