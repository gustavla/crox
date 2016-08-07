from __future__ import division, print_function, absolute_import
import argparse
from string import Template
import sys


class ParseException(Exception):
    def __init__(self, filename, line, message):
        super(ParseException, self).__init__(message)
        self.message = message
        self.filename = filename
        self.line = line


def init_state(escape):
    return {'functions': {}, 'defines': {}, 'in_func': False, 'escape': escape, 'cur_func': None}


import ast
import operator as op

# supported operators
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.FloorDiv: op.floordiv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}


def eval_expr(expr):
    """
    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0
    """
    return eval_(ast.parse(expr, mode='eval').body)


def eval_(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)


def process(fn, state, output=True):
    def maybe_print(*args, **kwargs):
        if output:
            print(*args, **kwargs)

    with open(fn) as f:
        for line_no, line in enumerate(f):
            if state['in_func']:
                if line.startswith(state['escape']) and line[len(state['escape']):].strip() == 'end':
                    state['functions'][state['cur_func']['name']] = state['cur_func']
                    state['in_func'] = False
                else:
                    state['cur_func']['body'] += line

            elif line.startswith(state['escape']):
                parsed_line = Template(line).substitute(state['defines'])
                rest = parsed_line[len(state['escape']):]
                v = rest.split()
                cmd = v[0]
                args = v[1:]
                #cmd, *args = rest.split()

                if cmd == 'begin':
                    state['in_func'] = True
                    state['cur_func'] = {'params': args[1:], 'name': args[0], 'body': ''}

                elif cmd == 'end':
                    if not state['in_func']:
                        raise ParseException(fn, line_no,
                                'Cannot call `end` without opening a function first')

                    state['functions'][state['cur_func']['name']] = state['cur_func']
                    state['in_func'] = False

                elif cmd == 'call':
                    func = state['functions'].get(args[0])
                    if not func:
                        raise ParseException(fn, line_no,
                                'Calling undefined function: {}'.format(args[0]))

                    if len(args[1:]) != len(func['params']):
                        print(state['functions'])
                        raise ParseException(fn, line_no,
                                'Wrong arity when calling `{}` (given {}, takes {})'.format(
                                    args[0], len(args[1:]), len(func['params'])))

                    #slurm = Template(f.read()).substitute(dict(name=name))
                    temp = Template(func['body'])
                    args = dict(zip(func['params'], args[1:]))
                    args.update(state['defines'])

                    maybe_print(temp.substitute(args), end='')

                elif cmd == 'define':
                    if len(args) < 2:
                        raise ParseException(fn, line_no,
                                '`define` takes two arguments')

                    state['defines'][args[0]] = ''.join(args[1:])

                elif cmd == 'define-eval':
                    if len(args) < 2:
                        raise ParseException(fn, line_no,
                                '`define` takes two arguments')

                    state['defines'][args[0]] = eval_expr(''.join(args[1:]))

                elif cmd == 'include':
                    if len(args) != 1:
                        raise ParseException(fn, line_no,
                                '`include` takes one argument')

                    process(args[0], state)

                else:
                    raise ParseException(fn, line_no, 'Unrecognized command: {}'.format(cmd))

            else:
                try:
                    parsed_line = Template(line).substitute(state['defines'])
                except KeyError as e:
                    print(e)
                    print('Error')
                    return

                maybe_print(parsed_line, end='')


# Python API
def defines(fn, escape=':'):
    """
    Use from Python to load defines from a crox file.
    """
    state = init_state(escape)
    process(fn, state, output=False)
    return state['defines']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str, help='Source file')
    parser.add_argument('-e', '--escape', type=str, default=':')
    parser.add_argument('-i', '--input', nargs='+', type=str)
    args = parser.parse_args()

    escape = args.escape
    state = init_state(escape)


    if args.input:
        for k_v in args.input:
            k, v = k_v.split('=')
            state['defines'][k] = v

    try:
        process(args.source, state)
    except ParseException as e:
        print('ERROR {}:{}'.format(e.filename, e.line + 1), e.message, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
