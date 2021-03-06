# Author: Carl M. Kobel 2019
# Description: Nodes for building a trie. Supports visualization with graphviz.
from graphviz import Digraph
from itertools import chain

class trienode:
    """ A trie node. """
    def __init__(self, in_edge_label = None, string_label = None, children = [], parent = None, start_index = -1, index = (None, None)):
        self.in_edge_label = in_edge_label # The edge into this node. 
        self.string_label = string_label # The sum of upstream in_edge_labels.
        self.children = [i for i in children]
        #self.parent = parent
        self.start_index = start_index # the position in S where this string_label occurs. -1 for not given.

    def __str__(self):
        """ The .string_label is used more often, I guess? """
        return self.string_label

    def __iter__(self):
        yield self
        for node in chain(*map(iter, self.children)):
            yield node

    # for sorting
    def __lt__(self, other):
        return self.string_label < other.string_label

    

    def __next__(self):
        yield self


    def __repr__(self):
        return str(self)

    def adopt(self, child):
        """ Adopts a child """
        self.children.append(child)
        #child.parent = self

    
    def split(self, split_pos, start_index = -1):
        #def __init__(self, in_edge_label = None, string_label = None, children = [], parent = None, start_index = -1, index = (None, None)):
        """ Depending on the split_pos, the self node will be split into 2, around this position. 
        Note, that it is only possible to split on the in edge label. """

        # If the split_pos is 0, nothing happens.
        if split_pos == 0:
            # Then nothing happens.
            # How to set this as current parent? 
            return
        

        # Input validation.
        if split_pos > len(self.in_edge_label) or split_pos < 0:
            err = ValueError(f'Split position: split_pos ({split_pos}) can\'t be higher than the length of self.in_edge_label ({len(self.in_edge_label)}) or below zero.\n\tNot splitting when trying to split node with string_label: {self.string_label}.')
            raise err


        second_node = trienode(self.in_edge_label[split_pos:], self.string_label, children = self.children, start_index = self.start_index)

        self.string_label = self.string_label[:- len(self.in_edge_label) + split_pos]
        self.in_edge_label = self.in_edge_label[:split_pos]
        #self.children = children = [second_node] #??? why is 'children' there?
        self.children = [second_node] #???


        #return second_node # returns, for controlling the curr_node variable (because I don't want to use the parent pointer.). Update: apparently, it is detrimental to proper performance to set the curr_node to this one.
        # How do we control what parent is left on the top of the stack after splitting, is that the popping procedure, that guarantees that? I guess so.
        # Split skal efterlade den initielle node som toppen af stakken.

        




    def visualize(self, filename = 'empty'):
        """ Draws a graph with graphviz. 

        Builds a tree in the gv-format and exports it to a pdf-file."""

        dot = Digraph(comment = 'Suffix tree')
        #dot.engine = 'circo'

        def node_format(node):
            """ Helper function to format the content of the nodes. """
            node_content = node.in_edge_label + '|' + node.string_label # all nodes must have a unique name, thus the concatenation of the two parts.
            edge_content =  node.string_label
            return node_content, edge_content


        def accept_node(node):
            """ Adds children recursively. """
            dot.node(*node_format(node))
            for child in node.children: # 
                accept_node(child) # Recursive call
                dot.edge(node_format(node)[0],
                         node_format(child)[0],
                         label = child.in_edge_label) # peg fra parent til child.


        accept_node(self)

        dot.render(f'test-output/{filename}.gv')
