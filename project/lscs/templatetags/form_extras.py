from django import template

register = template.Library()

@register.filter
def input_placeholder(field, args=None):
    if args is None:
        return field
    field.field.widget.attrs.update({ "placeholder": args })
    return field

@register.filter
def input_autofocus(field):
    field.field.widget.attrs.update({"autofocus":""})
    return field