from nose.tools import assert_equals

from mash.links import prune, find_path_in_tree, tree_to_html

def test_find_path_in_tree_returns_singleton_of_zero_for_root_path():
    tree = {
        "url": "/",
        "children": [
            {
                "url": "/projects/",
                "children": [
                    {"url": "/projects/funk/"},
                    {"url": "/projects/zuice/"}
                ]
            },
            {"url": "/blog/"}
        ]
    }
    assert_equals([0], find_path_in_tree(tree, "/"))
    
def test_find_path_in_tree_returns_none_if_path_not_in_tree():
    tree = {
        "url": "/",
        "children": [
            {
                "url": "/projects/",
                "children": [
                    {"url": "/projects/funk/"},
                    {"url": "/projects/zuice/"}
                ]
            },
            {"url": "/blog/"}
        ]
    }
    assert_equals(None, find_path_in_tree(tree, "/contact/"))

def test_find_path_in_tree_returns_list_of_indices_to_path():
    tree = {
        "url": "/",
        "children": [
            {
                "url": "/projects/",
                "children": [
                    {"url": "/projects/funk/"},
                    {"url": "/projects/zuice/"}
                ]
            },
            {"url": "/blog/"}
        ]
    }
    assert_equals([0, 0, 1], find_path_in_tree(tree, "/projects/zuice/"))
    
def test_find_path_in_tree_will_convert_path_ending_in_index_html_to_directory():
    tree = {
        "url": "/",
        "children": [
            {
                "url": "/projects/",
                "children": [
                    {"url": "/projects/funk/"},
                    {"url": "/projects/zuice/"}
                ]
            },
            {"url": "/blog/"}
        ]
    }
    assert_equals([0, 0, 1], find_path_in_tree(tree, "/projects/zuice/index.html"))

def test_pruning_links_leaves_only_direct_children_of_elements_on_current_path():
    tree = {
        "url": "/",
        "children": [
            {
                "url": "/projects/",
                "children": [
                    {
                        "url": "/projects/funk/",
                        "children": [
                            {"url": "/projects/funk/docs/"},
                            {"url": "/projects/funk/licence/"}
                        ]
                    },
                    {
                        "url": "/projects/zuice/",
                        "children": [
                            {"url": "/projects/zuice/docs/"},
                            {"url": "/projects/zuice/licence/"}
                        ]
                    }
                ]
            },
            {
                "url": "/blog/",
                "children": [
                    {"url": "/blog/archives/"},
                    {"url": "/blog/feed/"}
                ]
            }
        ]
    }
    
    prune(tree, "/projects/")
    expected_pruned_tree = {
        "url": "/",
        "children": [
            {
                "url": "/projects/",
                "children": [
                    {
                        "url": "/projects/funk/",
                    },
                    {
                        "url": "/projects/zuice/",
                    }
                ]
            },
            {
                "url": "/blog/",
            }
        ]
    }
    assert_equals(tree, expected_pruned_tree)
    
def test_pruning_links_leaves_only_root_and_its_children_if_path_is_not_found():
    tree = {
        "url": "/",
        "children": [
            {
                "url": "/projects/",
                "children": [
                    {"url": "/projects/funk/"},
                    {"url": "/projects/zuice/"}
                ]
            },
            {"url": "/blog/"}
        ]
    }
    
    prune(tree, "/projects/hebe/")
    expected_pruned_tree = {
        "url": "/",
        "children": [
            {"url": "/projects/"},
            {"url": "/blog/"}
        ]
    }
    assert_equals(tree, expected_pruned_tree)

def test_tree_to_html_converts_tree_with_no_children_to_its_name_only():
    assert_equals('<a href="/">zwobble.org</a>', tree_to_html({"url": "/", "label": "zwobble.org"}))

def test_tree_to_html_escapes_labels():
    assert_equals('<a href="/">P &lt;&gt; NP</a>', tree_to_html({"url": "/", "label": "P <> NP"}))

def test_tree_to_html_escapes_urls():
    assert_equals('<a href="http://www.example.com/src?project=funk&amp;repo=master">Source</a>',
                  tree_to_html({"url": "http://www.example.com/src?project=funk&repo=master", "label": "Source"}))

def test_tree_to_html_converts_tree_to_nested_lists():
    tree = {
        "url": "/", "label": "zwobble.org",
        "children": [
            {
                "url": "/projects/", "label": "Projects",
                "children": [
                    {"url": "/projects/funk/", "label": "Funk"},
                    {"url": "/projects/zuice/", "label": "Zuice"}
                ]
            },
            {"url": "/blog/", "label": "Blog"}
        ]
    }
    expected_tree_html =\
"""<a href="/">zwobble.org</a>
<ul>
<li>
<a href="/projects/">Projects</a>
<ul>
<li>
<a href="/projects/funk/">Funk</a>
</li>
<li>
<a href="/projects/zuice/">Zuice</a>
</li>
</ul>
</li>
<li>
<a href="/blog/">Blog</a>
</li>
</ul>"""
    assert_equals(expected_tree_html, tree_to_html(tree))
    
def test_tree_to_html_does_not_create_link_for_root_if_it_has_no_url():
    tree = {
        "children": [
            {"url": "/projects/", "label": "Projects"},
            {"url": "/blog/", "label": "Blog"}
        ]
    }
    expected_tree_html =\
"""<ul>
<li>
<a href="/projects/">Projects</a>
</li>
<li>
<a href="/blog/">Blog</a>
</li>
</ul>"""
    assert_equals(expected_tree_html, tree_to_html(tree))
