from django import template

register = template.Library()


@register.simple_tag
def breadcrumb(names, *args, **kwargs):
    names = names.split(',')
    if 'name' in kwargs:
        names.append(kwargs['name'])
    urls = list(args)
    urls.append('')

    results = list(zip(names, urls))
    # print(results)

    return results
