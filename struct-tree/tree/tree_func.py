from collections import defaultdict


def tree():
    return defaultdict(tree)

def print_tree(tree):
    def _print_tree(tree, buf, prefix):
        for k, v in tree.items():
            buf.append(prefix + '+- ' + k)
            if v:
                _print_tree(tree[k], buf, '|   ' + prefix)
    buf = []
    _print_tree(tree, buf, '')
    print('\n'.join(buf))

def traversal_tree(tree, func=None):
    def _traversal_tree(tree, func):
        for k, v in tree.items():
            if func and callable(func):
                func(k)
            if v:
                _traversal_tree(tree[k], func)
    _traversal_tree(tree, func)

