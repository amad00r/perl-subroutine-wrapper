from perl_subroutine_wrapper.perl_subroutine_wrapper import Module


example = Module('example.pm')

print(
    example.call(
        subroutine='conv_hexstring_to_string',
        parameters=['77 6F 72 6B 69 6E 67 20 66 69 6E 65'],
        return_type='scalar',
    )
)

print(example.call(subroutine='join', parameters=[[2, 3], [1, 1]], return_type='array'))

print(
    example.call(
        subroutine='parse_parameters',
        parameters=['-hello', '03456007345622', '-ip', '127.0.0.1'],
        return_type='hash',
    )
)

print(example.call(subroutine='error', parameters=None, return_type=None))
