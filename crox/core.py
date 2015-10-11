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


def process(fn, state):
    with open(fn) as f:
        for line_no, line in enumerate(f):
            if line.startswith(state['escape']):
                rest = line[len(state['escape']):]
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
                        print('args', args)
                        print(state['functions'])
                        raise ParseException(fn, line_no,
                                'Wrong arity when calling `{}` (given {}, takes {})'.format(
                                    args[0], len(args[1:]), len(func['params'])))

                    #slurm = Template(f.read()).substitute(dict(name=name))
                    temp = Template(func['body'])
                    args = dict(zip(func['params'], args[1:]))
                    args.update(state['globals'])

                    print(temp.substitute(args), end='')

                elif cmd == 'define':
                    if len(args) != 2:
                        raise ParseException(fn, line_no,
                                '`define` takes two arguments')

                    state['globals'][args[0]] = args[1]

                elif cmd == 'include':
                    if len(args) != 1:
                        raise ParseException(fn, line_no,
                                '`include` takes one argument')

                    process(args[0], state)

                else:
                    raise ParseException(fn, line_no, 'Unrecognized command: {}'.format(cmd))

            elif state['in_func']:
                state['cur_func']['body'] += line

            else:
                print(Template(line).substitute(state['globals']), end='')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str, help='Source file')
    parser.add_argument('-e', '--escape', type=str, default=':')
    parser.add_argument('-i', '--input', nargs='+', type=str)
    args = parser.parse_args()

    escape = args.escape

    state = {'functions': {}, 'globals': {}, 'in_func': False, 'escape': escape, 'cur_func': None}

    if args.input:
        for k_v in args.input:
            k, v = k_v.split('=')
            state['globals'][k] = v

    try:
        process(args.source, state)
    except ParseException as e:
        print('ERROR {}:{}'.format(e.filename, e.line + 1), e.message, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
