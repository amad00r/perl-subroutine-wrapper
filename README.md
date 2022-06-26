# perl-subroutine-wrapper

A Python wrapper for Perl subroutines.

This module makes it easy to call your Perl subroutines from Python. It is perfect for recycling old Perl code that you are not going to translate to Python.

It makes it possible to comunicate objects between the two languages through JSON object representations.

Valid Python objects passed as parameters are: dict, list, str, int, float, True, False, None.

Valid Perl objects returned are: SCALAR, ARRAY, HASH.


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
In *`example.pm`* we have a subroutine such as `parse_parameters` that we want to use in our Python script.

https://github.com/amad00r/perl-subroutine-wrapper/blob/902349470c2f82a4a45ad30c7c13d5dca6fb3517/example.pm#L30-L46

To wrap this subroutine and use it in Python we have to import the module, create a new `Module` instance passing the path of the Perl module, and call the `call` function passing the name of the subroutine, the parameters and the expected Perl object returned like I did in *`example.py`*. `parameters` and `returned_type` can be None.

https://github.com/amad00r/perl-subroutine-wrapper/blob/902349470c2f82a4a45ad30c7c13d5dca6fb3517/example.py#L16-L22

```
Output:

{'returned': {'hello': '03456007345622', 'ip': '127.0.0.1'}, 'stdout': None, 'error': None}
```
