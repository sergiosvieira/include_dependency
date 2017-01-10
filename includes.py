# find . -iname "*.h" -print0 | xargs -0 grep -e "^#include" | sed 's/://' | sed 's/^\.//' > includes.txt
#!/usr/bin/python

import ntpath
import sys, getopt

def is_valid(text):
    _aux = text.replace('"', '')
    # return _aux not in ("vector", "set", "functional", "array", "spinctrl.h", "stack", "algorithm", "map", "scrolwin.h", "string", "statline.h", "fstream", "treectrl.h", "cstdint", "checklst.h", "cstdlib", "memory", "iostream", "string.h")
    return _aux in ("glpk.h")

def normalize(text):
    result = text.replace('<', '')
    result = result.replace('>', '')
    # result = result.replace('\\', '')
    # result = result.replace('/', '')
    result = result.replace('"', '')
    result = ntpath.basename(result)
    result = '"' + result + '"'
    return result;


class Node:
    def __init__(self, title):
        self.title = normalize(title)
        self.child = []
        self.include_counter = 0

    def add_child(self, child):
        counter = child.include_counter
        counter = counter + 1
        child.include_counter = counter
        self.child.append(child)

    def __str__(self):
        result = ""
        counter = 0
        for node in self.child:
            if is_valid(self.title) == False:
                continue
            if node.include_counter >= 5:
                result += "node [color=red]"
            else:
                result += "node [color=black]"
            result += self.title + " -> " + node.title + '\n'
            counter = counter + 1
            # if counter == 5:
            #     break
        return result


class Graph:
    def __init__(self):
        self.data = {}

    def add_node(self, node):
        self.data[normalize(node.title)] = node

    def find(self, title):
        normal_title = normalize(title)
        for key, value in self.data.items():
            if key == normal_title:
                return value
        return None

    def __str__(self):
        result = ""
        for key, value in self.data.items():
            result += value.__str__()
            result += '\n'
        return result

def main(argv):
    g = Graph()
    input_file = "resop.txt"
    with open(input_file) as f:
        for line in f:
            array = line.split("#include")
            child_title = array[0].strip()
            parent_title = array[1].strip()
            parent = g.find(parent_title)
            if parent == None:
                node = Node(array[1].strip())
                parent = node
            child = g.find(child_title)
            if child == None:
                node = Node(child_title)
                child = node
            g.add_node(parent)
            parent.add_child(child)
    print("digraph g{")
    print(g)
    print("}")

if __name__ == "__main__":
    main(sys.argv[:1])
