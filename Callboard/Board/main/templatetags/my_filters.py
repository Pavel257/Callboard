from django import template

register = template.Library()


@register.filter(name='Censor')
def Censor(value):
    censor_list = ['дебил',
                   'дурак',
                   'придурок']

    value1 = (str(value)).split()
    for i in censor_list:
        for j in value1:
            if j == i:
                value1.remove(i)
    value = ' '.join(value1)
    return str(value)


@register.filter(name='update_page')
def update_page(full_path: str, page: int):
    try:
        params_list = full_path.split('?')[1].split('&')
        params = dict([tuple(str(param).split('=')) for param in params_list])
        params.update({'page': page})
        link = ''
        for key, value in params.items():
            link += (f"{key}={value}&")
        return link[:-1]
    except:
        return f"page={page}"
