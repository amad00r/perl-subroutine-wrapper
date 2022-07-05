use lib '{{ directory }}';
require {{ module }};
use JSON;

open(OLDOUT, ">&", STDOUT);
open(STDOUT, ">", "{{ print_path }}");

{% if json_params is none %}

{% if symbol is not none %}{{ symbol[0] }}returned = {% endif %}{{ module }}::{{ subroutine }}();

{% else %}

@param_array = @{ decode_json '{{ json_params }}' };
{% if symbol is not none %}{{ symbol[0] }}returned = {% endif %}{{ module }}::{{ subroutine }}(@param_array);

{% endif %}

close(STDOUT);

{% if symbol is not none %}

open(STDOUT, ">&", OLDOUT);
print encode_json {{ symbol[1] }}returned;
close(OLDOUT);

{% endif %}
