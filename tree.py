from collections import defaultdict

def tree():
    return defaultdict(tree)

def print_tree(tree):
    def _print_tree(tree, buf, prefix):
        for k, v in tree.iteritems():
            buf.append(prefix + '+- ' + k)
            if v:
                _print_tree(tree[k], buf, '|   ' + prefix)
    buf = []
    _print_tree(tree, buf, '')
    print('\n'.join(buf))

taxonomy = tree()
taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Felidae']['Felis']['cat']
taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Felidae']['Panthera']['lion']
taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Canidae']['Canis']['dog']
taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Canidae']['Canis']['coyote']
taxonomy['Plantae']['Solanales']['Solanaceae']['Solanum']['tomato']
taxonomy['Plantae']['Solanales']['Solanaceae']['Solanum']['potato']
taxonomy['Plantae']['Solanales']['Convolvulaceae']['Ipomoea']['sweet potato']

print_tree(taxonomy)


