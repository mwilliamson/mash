import os
import os.path
import sys
import mash.rst
import shutil
import re
import mash.links
import simplejson as json

def mkdir_p(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def generate(template_path, source_dir, static_dir, target_dir):
    shutil.copytree(static_dir, target_dir)
    
    template_file = open(template_path)
    template = template_file.read()
    template_file.close()

    for root, dirs, filenames in os.walk(source_dir):
        for filename in filenames:
            source_file = open(os.path.join(root, filename), "r")
            source = source_file.read()
            source_file.close()
            
            if filename.endswith(".html"):
                contents = source
            elif filename.endswith(".rst"):
                contents = mash.rst.rst_to_html_fragment(source)
            else:
                raise RuntimeError("Unrecognised file type: %s" % (filename,))
            full_contents = template.replace("<!-- CONTENT -->", contents)
            nav_placeholder = "<!-- NAVIGATION -->"
            if nav_placeholder in full_contents:
                nav_tree = json.loads(open("navigation.links").read())
                # FIXME: should prune to current path
                mash.links.prune(nav_tree, "/")
                nav_str = mash.links.tree_to_html(nav_tree)
                full_contents = full_contents.replace(nav_placeholder, nav_str)
            target_path = os.path.join(target_dir, root[len(source_dir)+1:], re.sub(r".[^.]+$", ".html", filename))
            print target_path
            mkdir_p(os.path.dirname(target_path))
            target = open(target_path, "w")
            target.write(full_contents)
            target.close()
        

