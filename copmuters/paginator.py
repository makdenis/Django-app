from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#

def paginate(data, page):
        paginator = Paginator(data,5)
        try:
            data = paginator.page(page)

        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        # print(data.paginator.num_pages)
        return data