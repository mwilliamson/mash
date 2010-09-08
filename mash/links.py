def find_path_in_tree(tree, path, id=[0]):
    if path == tree["url"]:
        return id
    if "children" not in tree:
        return None
    for index, child_tree in enumerate(tree["children"]):
        result = find_path_in_tree(child_tree, path, id + [index])
        if result is not None:
            return result

def prune_to_id(tree, id, current_id=[0]):
    if "children" in tree:
        if current_id == id[:len(current_id)]:
            for index, child_tree in enumerate(tree["children"]):
                prune_to_id(child_tree, id, current_id + [index])
        else:
            del tree["children"]

def prune(tree, path):
    id = find_path_in_tree(tree, path)
    prune_to_id(tree, id)
