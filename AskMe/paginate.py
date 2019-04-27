from django.core.paginator import Paginator


def paginate(request, objects_list):
    paginator = Paginator(objects_list, 3)
    return paginator
