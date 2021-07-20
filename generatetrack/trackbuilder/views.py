from random import randint

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound

from generatetrack.settings import redis_instance


# Create your views here.
def build(request):
    if 'from' not in request.GET or 'to' not in request.GET:
        return HttpResponseBadRequest("You should set GET parameters `from` and `to`")

    from_coord, to_coord = redis_instance.geopos("DOT", request.GET.get('from'), request.GET.get('to'))
    if not from_coord or not to_coord:
        return HttpResponseNotFound("One of dots wasn`t found")

    radius = redis_instance.geodist("DOT", request.GET.get('from'), request.GET.get('to'), unit='km')
    radius = 100
    dots1 = set(redis_instance.georadius("DOT", *from_coord, radius, unit='km'))
    dots2 = set(redis_instance.georadius("DOT", *to_coord, radius, unit='km'))
    path_length = randint(2, 100)
    if dots2 & dots1:
        same_dots = (i for i in  dots2 & dots1)
    else:
        same_dots = (i for i in dots2 | dots1)

    path = [int(request.GET.get('from')), ]
    for dot in same_dots:
        if len(path)>path_length:
            break
        dot_id = int(dot)
        if dot_id not in path and dot_id!= int(request.GET.get('to')):
            path.append(dot_id)
    path.append(int(request.GET.get('to')))
    return JsonResponse({'length': radius, 'dots': len(path), 'from': from_coord, 'to': to_coord, 'path': path})
