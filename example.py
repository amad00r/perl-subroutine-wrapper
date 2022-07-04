from perl_subroutine_wrapper.perl_subroutine_wrapper import Module


example = Module('example.pm')


conv_hexstring_to_string = example.call(
    subroutine='conv_hexstring_to_string',
    parameters=['77 6F 72 6B 69 6E 67 20 66 69 6E 65'],
    return_type='scalar',
)
print(conv_hexstring_to_string)


join = example.call(subroutine='join', parameters=[[2, 3], [1, 1]], return_type='array')
print(join)


parse_parameters = example.call(
    subroutine='parse_parameters',
    parameters=['-hello', '03456007345622', '-ip', '127.0.0.1'],
    return_type='hash',
)
print(parse_parameters.returned)


error = example.call(subroutine='error', parameters=None, return_type=None)
print(error.error)
