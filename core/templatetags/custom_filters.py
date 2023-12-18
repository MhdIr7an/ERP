from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    css_classes = value.field.widget.attrs.get('class', '')
    css_classes += ' ' + arg
    value.field.widget.attrs['class'] = css_classes
    return value


@register.filter(name='new_id')
def new_id(field, id):
    return field.as_widget(attrs={'id': f'{field.id} {id}'})

@register.filter(name='readonly')
def readonly(field):
    return field.as_widget(attrs={'readonly': 'readonly'})