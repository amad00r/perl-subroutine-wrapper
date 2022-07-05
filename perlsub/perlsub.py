"""Python wrapper for Perl subroutines.

This module makes it easy to call your Perl subroutines from Python. It is perfect
for recycling old Perl code that you are not going to translate to Python.

It makes it possible to comunicate objects between the two languages through JSON
object representations.

Valid Python objects passed as parameters are: dict, list, str, int, float, True,
False, None.

Valid Perl objects returned are: SCALAR, ARRAY, HASH.

"""

from subprocess import Popen, PIPE
from pathlib import Path
from tempfile import TemporaryDirectory
from shutil import which
from json import loads, dumps
from collections import namedtuple
from types import NoneType
from typing import Union
from jinja2 import Environment, FileSystemLoader


class Module:
    """Represents the specified Perl module for later usage.

    Args:
        path (str): It takes either a relative or absolute path to the Perl module.

    Attributes:
        module_path (pathlib.Path): Path to the perl module.
        tmpdir (tempfile.TemporaryDirectory): Temporary directory where the dinamically
            created wrapper and the stdout file are going to be located.
        tmp_wrapper_path (pathlib.Path): Path to the dinamically created wrapper.
        tmp_stdout_path (pathlib.Path): Path to the temporal stdout file.
        wrapper_template (jinja2.environment.Template): On memory wrapper template that will
            be used to create the wrapper.

    """

    def __init__(self, path: str) -> None:
        if which('perl') is None:
            raise Exception('Perl is not installed.')

        self.module_path = Path(path)
        if not self.module_path.resolve().is_file():
            raise Exception(f"Perl module '{self.module_path.name}' not found.")

        self.tmpdir = TemporaryDirectory()
        tmpdir_path = Path(self.tmpdir.name)

        self.tmp_wrapper_path = tmpdir_path / 'wrapper.pl'
        self.tmp_stdout_path = tmpdir_path / 'stdout.tmp'

        self.wrapper_template = Environment(
            loader=FileSystemLoader(Path(__file__).parent.absolute())
        ).get_template('wrapper_template.pl')

    def generate_wrapper(
        self, subroutine: str, parameters: list, return_type: Union[str, None]
    ) -> None:
        """Generates the specified subroutine wrapper.

        Args:
            subroutine (str): Name of the Perl subroutine that will be called.
            parameters (list): List of parameters that will be passed to the specified
                subroutine.
            return_type: Expected returned Perl object type. Valid return_type values
                are: 'scalar', 'array', 'hash'.

        """

        if return_type in ('scalar', 'array', 'hash', None):
            symbols = {
                'scalar': ('$', '$'),
                'array': ('@', r'\@'),
                'hash': ('%', r'\%'),
                None: None,
            }
        else:
            raise Exception("return_type must be either 'scalar', 'array', 'hash' or None.")

        template_parameters = {
            'directory': self.module_path.parent.resolve(),
            'module': self.module_path.stem,
            'print_path': self.tmp_stdout_path.as_posix(),
            'json_params': None if parameters is None else dumps(parameters),
            'symbol': symbols[return_type],
            'subroutine': subroutine,
        }

        wrapper_content = self.wrapper_template.render(template_parameters)

        with open(self.tmp_wrapper_path, 'w', encoding='utf8') as wrapper:
            wrapper.write(wrapper_content)

    def call(self, subroutine: str, parameters: list, return_type: Union[str, None]) -> dict:
        """Generates the specified subroutine wrapper.

        Args:
            subroutine (str): Name of the Perl subroutine that will be called.
            parameters (list): List of parameters that will be passed to the specified
                subroutine.
            return_type: Expected returned Perl object type. Valid return_type values
                are: 'scalar', 'array', 'hash'.

        Returns:
            A `PerlCallResult` namedtuple containing 'returned', 'stdout' and 'error' attributes
            collected from the execution of the Perl subroutine.
            'returned' can be dict, list, str, int, float, True, False, None.
            'stdout' can be str, None.
            'error' can be str, None.

            For example:

            PerlCallResult(returned=[2, 3, 1, 1], stdout='Joined :)', error=None)

        """

        if not isinstance(parameters, (list, NoneType)):
            raise Exception('Parameters must be passed within a list.')

        self.generate_wrapper(subroutine, parameters, return_type)

        with Popen(['perl', self.tmp_wrapper_path], stdout=PIPE, stderr=PIPE) as wrapper_call:
            result = wrapper_call.stdout.read()

            returned = None if result is None or not result else loads(result.decode('utf8'))

            if Path(self.tmp_stdout_path).is_file():
                with open(self.tmp_stdout_path, 'r', encoding='utf8') as file:
                    stdout = file.read()
            else:
                stdout = None

            error = wrapper_call.stderr.read().decode('utf8')

        PerlCallResult = namedtuple('PerlCallResult', ['returned', 'stdout', 'error'])

        return PerlCallResult(returned, stdout if stdout else None, error if error else None)
