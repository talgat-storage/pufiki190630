from django import template

register = template.Library()


@register.filter(name='add_css')
def add_css(field, css):
    attrs = field.field.widget.attrs
    class_attr = attrs['class'] if 'class' in attrs else ''
    return field.as_widget(attrs={'class': ' '.join([class_attr, css])})
