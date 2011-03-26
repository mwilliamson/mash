import cgi

def find_path_in_tree(tree, path, id=[0]):
    if path == tree["url"] or (path.endswith("/index.html") and path[:-len("index.html")] == tree["url"]):
        return id
    if "children" not in tree:
        return None
    for index, child_tree in enumerate(tree["children"]):
        result = find_path_in_tree(child_tree, path, id + [index])
        if result is not None:
            return result

def prune_to_id(tree, id, current_id=[0]):
    if "children" not in tree:
        return
    if id is None:
        for child_tree in tree["children"]:
            if "children" in child_tree:
                del child_tree["children"]
    else:
        if current_id == id[:len(current_id)]:
            for index, child_tree in enumerate(tree["children"]):
                prune_to_id(child_tree, id, current_id + [index])
        else:
            del tree["children"]

def prune(tree, path):
    id = find_path_in_tree(tree, path)
    prune_to_id(tree, id)

def html_escape(text):
    return cgi.escape(text, True)

def tree_to_html_builder(tree, html):
    if "url" in tree:
        html.append('<a href="%s">%s</a>' % (html_escape(tree["url"]), html_escape(tree["label"])))
    if "children" in tree:
        html.append("<ul>")
        for child_tree in tree["children"]:
            html.append("<li>")
            tree_to_html_builder(child_tree, html)
            html.append("</li>")
        html.append("</ul>")

def tree_to_html(tree):
    html = []
    tree_to_html_builder(tree, html)
    return '\n'.join(html)
