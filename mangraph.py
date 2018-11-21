"""This script tries to print a graph of related man pages in dot format"""

import re
import subprocess
import sys


def related_tools(parent, seen):
    cmd = f'man 1 {parent} | col -bx | sed -n "/SEE ALSO/{{n;p;}}"'
    related = subprocess.check_output(cmd, shell=True).strip().decode()
    for tool in re.findall('(\w+)\(1\)', related):
        edge = f'{parent} -> {tool}'
        if edge not in seen:
            seen.add(edge)
            related_tools(tool, seen)
    return seen


def main():
    if len(sys.argv) != 2:
        print('usage: python mangraph.py tool | dot')
        sys.exit(1)

    tool = sys.argv[1]

    edges = related_tools(tool, set())
    print('digraph {')
    print(f'    {tool} [peripheries=2];')
    for edge in edges:
        print(f'    {edge};')
    print('}')


if __name__ == '__main__':
    main()
