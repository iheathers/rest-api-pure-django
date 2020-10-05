from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from django.views import View
from .models import Update


# Create your views here.
def update_detail_view(request):
    data = {
        "count": 10,
        "content": "Some contents",
    }
    return JsonResponse(data)


class UpdateView(View):
    def get(self, request, *args, **kwargs):
        data = {
            "count": 10,
            "content": "Some contents",
        }
        return JsonResponse(data)


class JsonResponseMixin(object):
    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(self.get_data(context), **response_kwargs)

    def get_data(self, context):
        return context


class UpdateView_with_mixin(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs):
        data = {
            "count": 10,
            "content": "Some contents",
        }
        return self.render_to_json_response(data)


class SerializedDetailView(View):
    def get(self, request, *args, **kwargs):
        obj = Update.objects.get(pk=1)
        data = obj.serialize()
        return HttpResponse(data)


class SerializedListView(View):
    def get(self, request, *args, **kwargs):
        queryset = Update.objects.all()
        data = queryset.serialize()
        return HttpResponse(data)
