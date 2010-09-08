from nose.tools import assert_equals

from mash.links import prune, find_path_in_tree

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
