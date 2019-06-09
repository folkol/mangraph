"""This script tries to print a graph of related man pages in dot format"""

import re
import subprocess
import sys


BUILTINS = [
    'builtin',
    '!',
    '%',
    '.',
    ':',
    '@',
    '{',
    '}',
    'alias',
    'alloc',
    'bg',
    'bind',
    'bindkey',
    'break',
    'breaksw',
    'builtins',
    'case',
    'cd',
    'chdir',
    'command',
    'complete',
    'continue',
    'default',
    'dirs',
    'do',
    'done',
    'echo',
    'echotc',
    'elif',
    'else',
    'end',
    'endif',
    'endsw',
    'esac',
    'eval',
    'exec',
    'exit',
    'export',
    'false',
    'fc',
    'fg',
    'filetest',
    'fi',
    'for',
    'foreach',
    'getopts',
    'glob',
    'goto',
    'hash',
    'hashstat',
    'history',
    'hup',
    'if',
    'jobid',
    'jobs',
    'kill',
    'limit',
    'local',
    'log',
    'login',
    'logout',
    'ls-F',
    'nice',
    'nohup',
    'notify',
    'onintr',
    'popd',
    'printenv',
    'pushd',
    'pwd',
    'read',
    'readonly',
    'rehash',
    'repeat',
    'return',
    'sched',
    'set',
    'setenv',
    'settc',
    'setty',
    'setvar',
    'shift',
    'source',
    'stop',
    'suspend',
    'switch',
    'telltc',
    'test',
    'then',
    'time',
    'times',
    'trap',
    'true',
    'type',
    'ulimit',
    'umask',
    'unalias',
    'uncomplete',
    'unhash',
    'unlimit',
    'unset',
    'unsetenv',
    'until',
    'wait',
    'where',
    'which',
    'while'
]


def related_tools(roots):
    seen = set()

    def related_tools_recursive(parent):
        cmd = f'man 1 {parent} | col -bx | sed -n "/SEE ALSO/{{n;p;}}"'
        related = subprocess.check_output(cmd, shell=True).strip().decode()
        for tool in re.findall('(\w+)\(1\)', related):
            if tool in BUILTINS:
                continue
            edge = (parent, tool)
            if edge not in seen:
                print(f'Following {edge[0]} -> {edge[1]}', file=sys.stderr)
                seen.add(edge)
                related_tools_recursive(tool)
        return seen

    for root in roots:
        related_tools_recursive(root)
    return seen


def main():
    if len(sys.argv) < 2:
        print('usage: python mangraph.py tools... | dot')
        sys.exit(1)

    tools = sys.argv[1:]

    edges = related_tools(tools)
    print('digraph {')
    #for tool in tools:
        #print(f'  {tool} [peripheries=2];')
    for a, b in edges:
        print(f'  "{a}" -> "{b}";')
    print('}')


if __name__ == '__main__':
    main()
