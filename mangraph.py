"""This script tries to print a graph of related man pages in dot format"""

import re
import subprocess
import sys


def related_tools(root):
    seen = set()

    def related_tools_recursive(parent):
        cmd = f'man 1 {parent} | col -bx | sed -n "/SEE ALSO/{{n;p;}}"'
        related = subprocess.check_output(cmd, shell=True).strip().decode()
        for tool in re.findall('(\w+)\(1\)', related):
            edge = (parent, tool)
            if edge not in seen:
                seen.add(edge)
                related_tools_recursive(tool)
        return seen

    return related_tools_recursive(root)


def main():
    if len(sys.argv) != 2:
        print('usage: python mangraph.py tool | dot')
        sys.exit(1)

    tool = sys.argv[1]

    edges = related_tools(tool)
    print('digraph {')
    print(f'  {tool} [peripheries=2];')
    for a, b in edges:
        print(f'  {a} -> {b};')
    print('}')


if __name__ == '__main__':
    main()
