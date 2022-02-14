import sys
from tree.tree_func import tree, print_tree
from tree.tree_class import Tree

# Create a tree
if sys.argv[1] == 'func':
    taxonomy = tree()
elif sys.argv[1] == 'class':
    taxonomy = Tree()
else:
    sys.exit(1)

# Set a tree
taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Felidae']['Felis']['cat']
taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Felidae']['Panthera']['lion']
taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Canidae']['Canis']['dog']
taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Canidae']['Canis']['coyote']
taxonomy['Plantae']['Solanales']['Solanaceae']['Solanum']['tomato']
taxonomy['Plantae']['Solanales']['Solanaceae']['Solanum']['potato']
taxonomy['Plantae']['Solanales']['Convolvulaceae']['Ipomoea']['sweet potato']

# Print a tree
if sys.argv[1] == 'func':
    print_tree(taxonomy)
elif sys.argv[1] == 'class':
    print(taxonomy)
else:
    pass
