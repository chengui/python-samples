from collections import defaultdict


class Tree(defaultdict):
    def __init__(self):
        super().__init__(Tree)

    def __str__(self):
        def _str(tree, buf, prefix):
            for k, v in tree.items():
                buf.append(prefix + '+- ' + k)
                if v:
                    _str(tree[k], buf, '|   ' + prefix)
        buf = []
        _str(self, buf, '')
        return '\n'.join(buf)
