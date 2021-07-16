from django.contrib.sites import requests
from django.http import JsonResponse, Http404, HttpResponseBadRequest, HttpResponseNotFound
from random import randint

from generatetrack.settings import redis_instance


def get_dot_info(dotid: int = 0) -> dict:
    ret = requests.get(f'http://dots/api/dot/{dotid}')
    if ret.ok:
        return ret.json()
    raise ValueError("Dot not found!")


# Create your views here.
def build(request):
    if 'from' not in request.GET or 'to' not in request.GET:
        return HttpResponseBadRequest("You should set GET parameters `from` and `to`")

    from_coord, to_coord = redis_instance.geopos("DOT", request.GET.get('from'), request.GET.get('to'))
    if not from_coord or not to_coord:
        return HttpResponseNotFound("One of dots wasn`t found")

    radius = redis_instance.geodist("DOT", request.GET.get('from'), request.GET.get('to'), unit='km')
    dots1 = set(int(i) for i in redis_instance.georadius("DOT", *from_coord, radius, unit='km'))
    dots2 = set(int(i) for i in redis_instance.georadius("DOT", *to_coord, radius, unit='km'))
    path_length = randint(2, 100)
    same_dots = dots2 & dots1
    path = [int(request.GET.get('from')), ]
    while path_length > 0 and same_dots:
        path_length -=1
        path.append(same_dots.pop())
    path.append(int(request.GET.get('to')))
    return JsonResponse({'length': radius, 'dots': len(path), 'from': from_coord, 'to': to_coord, 'path': path})
