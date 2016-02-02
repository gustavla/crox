# crox

**crox** is a light-weight general-purpose ma**cro** e**x**pander. 

It is a streaming parser that processes each line only once. This means that functions and variables need to be defined before they are used.

## Install

Install through PyPI:

    pip install crox
    
This will install the command line tool `crox`. Can also be called using `python -m crox`.
    
## Commands

Each command is prefixed by `:`. This can be changed using the `-e` option.

### Define variable

Variables can be defined and re-defined at any time:

    :define <variable name> <value>
    
Ex:

    :define ABC 100
    
### Reference variable

    $<variable name>
    ${<variable name>}
    
Ex:

    Variable $ABC or ${ABC}.

### Define function

Functions can be defined and re-defined at any time:

    :begin <function name> <arg name 1> <arg name 2> ...
    <contents>
    :end
    
Ex:

    :begin foo x
    Calling foo with x=$x.
    :end
    
### Call function

    :call <function name> <arg 1> <arg 2> ...
  
Ex:
  
    :call foo 100
    
### Include file

Includes another file in-place that uses and can modify the same state machine (equivalent of copy-pasting in the other file at this location):

    :include <filename>
    
Ex:

    :include inc.crox
    
## Example

Imagine a source file `test.crox.txt`:

    :define abc 100
    :begin foo x y
    Calling foo with $x and $y, using global $abc.
    :end
    This is an example
    
    :call foo 10 test
    :define abc 200
    :call foo 20 abc
    
Now call:

    crox test.crox.txt
    
Will produce the following to standard output:

    This is an example

    Calling foo with 10 and test, using global 100.
    Calling foo with 20 and abc, using global 200.
