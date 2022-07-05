# perl-subroutine-wrapper

A Python wrapper for Perl subroutines.

This module makes it easy to call your Perl subroutines from Python. It is perfect for recycling old Perl code that you are not going to translate to Python.

It makes it possible to comunicate objects between the two languages through JSON object representations.

Valid Python objects passed as parameters are: dict, list, str, int, float, True, False, None.

Valid Perl objects returned are: SCALAR, ARRAY, HASH.

## Installation

You can install this module from Pypi:

```
pip install perlwrapper
```

## Requirements

In order to use this python module you will need to install jinja2, which will help us with generate the Perl intermediary wrapper dinamically when calling subroutines:
```
pip install jinja2
```
You also need Perl installed in your computer. You can check if it is installed and the version with the command:
```
perl -v
```

## Example of usage

*`example.py`* and *`example.pm`* show us how to use the module.
In *`example.pm`* we have a Perl subroutine such as `join` that we want to use in our Python script.

```perl
sub join { 
     my ($list1, $list2)=@_; 
     my @list3; 
     push @list3, @$list1; 
     push @list3, @$list2; 
     print "Joined :)"; 
     return @list3;
}
```

To wrap this subroutine and use it in Python we have to import the module, create a new `Module` instance passing the path of the Perl module, and call the `call` function passing the name of the subroutine, the parameters and the expected Perl object returned like I did in *`example.py`*. `parameters` and `returned_type` can be None.

```python
from perlwrapper import Module


example = Module('example.pm')

join = example.call(
  subroutine='join', 
  parameters=[[2, 3], [1, 1]], 
  return_type='array'
)
print(join)
```

```
Output:

PerlCallResult(returned=[2, 3, 1, 1], stdout='Joined :)', error=None)
```
