import json
from django import template
from django.db.models import QuerySet
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def variable(value, name):
    if type(value) == QuerySet:
        value = list(value)

    json_str = json.dumps(value, default=str)
    # second encoding encodes quotes
    js_str = json.dumps(json_str)
    result = f"""
<script>
    var {name} = JSON.parse({js_str});
</script>"""
    return mark_safe(result)