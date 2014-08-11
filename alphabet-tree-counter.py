'''
Alphabet tree counter.

Takes input as a filename argument, or requests from keyboard if no
filename is provided. Outputs the number of connected trees and any
problems with the input.

For use in testing answers to

http://codegolf.stackexchange.com/questions/36034/how-many-trees-in-the-alphabet-forest
'''

import string

CONNECTIONS = dict(A = [3, 4],
                   C = [2, 4],
                   E = [2, 4],
                   F = [2, 3],
                   G = [2],
                   H = [1, 2, 3, 4],
                   I = [1, 2, 3, 4],
                   J = [1, 3],
                   K = [1, 2, 3, 4],
                   L = [1, 4],
                   M = [3, 4],
                   N = [2, 3],
                   P = [3],
                   Q = [4],
                   R = [3, 4],
                   S = [2, 3],
                   T = [1, 2],
                   U = [1, 2],
                   V = [1, 2],
                   W = [1, 2],
                   X = [1, 2, 3, 4],
                   Y = [1, 2],
                   Z = [1, 4]
                   )

VALID_LETTERS = set(string.ascii_uppercase) - set('BDO')
VALID_CHARACTERS = VALID_LETTERS | set(' ')


class Node():
    
    def __init__(self, character, location, all_nodes=[]):
        self.location = location
        self.connections = CONNECTIONS[character]
        self.all_nodes = all_nodes
        self.all_nodes.append(self)
        
    def attachees(self):
        attached_to_self = []
        for direction in range(1, 5):
            if direction in self.connections:
                reverse_direction = 5 - direction
                x, y = self.location
                other_location = (x+1-(direction%2)*2,y+1-(direction<3)*2)
                other = self.node_at(other_location)
                if other and (reverse_direction in other.connections):
                    attached_to_self.append(other)
        return attached_to_self
                       
    def node_at(self, location):
        if (location in self.occupied_locations()):
            return [node for node in self.all_nodes
                    if node.location == location
                    ][0]
        else:
            return None
        
    def occupied_locations(self, location_list=[]):
        if not location_list:
            location_list = [node.location for node in self.all_nodes]
        return location_list
        
        
def verify(source):
    '''Print report of whether source matches question requirements.'''
    grumbles = ''
    line_count = 0
    lines = []
    for line in source:
        line_count += 1
        if line_count > 79:
            grumbles += 'PROBLEM: more than 79 lines.\n'
            break
        length = len(line)
        if length > 79:     # length excludes newline
            grumbles += ('PROBLEM: more than 79 characters in line {}'
                         .format(line_count) +
                         ' (excluding newline).\n'
                         )
        invalid_characters = set(line) - VALID_CHARACTERS
        if invalid_characters:
            grumbles += ('PROBLEM: Invalid characters in line {}:\n'
                         .format(line_count)
                         )
            while invalid_characters:
                grumbles += invalid_characters.pop()
            grumbles += '\n'
        lines.append(line)
##    present_letters = ''.join(''.join(line.split()) for line in lines)
##    represented_letters = set(present_letters)
    nodes = set()
    for line_number in range(len(lines)):
        line = lines[line_number]
        for character_number in range(len(line)):
            character = line[character_number]
            location = (character_number, line_number)
            if character in VALID_LETTERS:
                nodes.add(Node(character, location))
    trees = []
    for node in nodes:
        if not any(node in tree for tree in trees):
            trees.append(home_tree(node, nodes))
    distinct_parts = len(trees)
    print('Number of connected trees: {}\n'.format(distinct_parts))
    if grumbles:
        print(grumbles)
        print('Therefore output is undefined.')
        
    
def home_tree(node, nodes):
    current_tree = {node}
    while True:
        expanded_tree = tree_expansion(current_tree, nodes)
        if len(expanded_tree) == len(current_tree):
            break
        current_tree = expanded_tree
    return current_tree

    
def tree_expansion(tree, nodes):
    expanded_tree = tree.copy()
    for node in tree:
        expanded_tree.update(node.attachees())
    return expanded_tree

    
def from_file(filename):
    with open(filename) as f:
        for line in f:
            if line:
                neat_line = line.replace('\n', '')
                yield neat_line
            else:
                break
                
            
def from_keyboard():
    print('Enter your tree with an additional newline to terminate')
    while True:
        line = input()
        if line:
            yield line
        else:
            break

            
if __name__=='__main__':
    import sys
    arguments = sys.argv[1:]
    if arguments:
        source = from_file(arguments[0])
    else:
        source = from_keyboard()
    verify(source)

