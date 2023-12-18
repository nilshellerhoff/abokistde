import json
import os

from django import template
from django.db.models import QuerySet
from django.utils.safestring import mark_safe

register = template.Library()


@register.tag
def include_templates(parser, token):
    """include all templates in the current directory"""
    tag_name, path = token.split_contents()
    path = path.strip("'").strip('"').strip("/")

    origin_path = os.path.dirname(str(parser.origin))
    templates_path = os.path.join(origin_path, path)
    files = [os.path.basename(f) for f in os.listdir(templates_path)]

    include_tags = ["{% " + f'include "./{path}/{file}"' + " %}" for file in files]

    paths = [f"./{path}/{file}" for file in files]
    return IncludeNode(paths)

class IncludeNode(template.Node):
    def __init__(self, paths):
        self.paths = paths

    def render(self, context):
        tags = ["{% include " + path + " %}" for path in self.paths]
        return "\n".join(tags)
