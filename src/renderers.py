def php(data: dict) -> str:
    from jinja2 import Environment, BaseLoader

    return (
        Environment(loader=BaseLoader())
        .from_string(
            """
{%- macro keyval(key,val) %}
{{ key | tojson  }} => {{ array(val) }},
{%- endmacro -%}

{%- macro inoval(val) %}
{{ array(val) }},
{%- endmacro -%}

{%- macro array(data) -%}
{%- if data is mapping -%}
[
{%- for key, val in data.items() -%}
{{ keyval(key,val) | indent(2) }}
{%- endfor %}
]
{%- elif data is iterable and data is not string -%}
[
{%- for val in data -%}
{{ inoval(val) | indent(2) }}
{%- endfor %}
]
{%- else -%}
{{ data | tojson }}
{%- endif -%}
{%- endmacro -%}

<?php

return {{ array(data) }};
"""
        )
        .render(data=data)
    )


def json(data: dict) -> str:
    from json import dumps

    return dumps(data, indent=2)
