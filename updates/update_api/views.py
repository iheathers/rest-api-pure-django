from updates.models import Update as UpdateModel
from django.http import HttpResponse
from django.views.generic import View
import json

from updates.forms import UpdateForm
from .mixin import CSRFExemptMixin
from .utils import is_json


class UpdateModelDetailAPIView(CSRFExemptMixin, View):
    def get_object(self, id=None):
        try:
            obj = UpdateModel.objects.get(id=id)
        except UpdateModel.DoesNotExist:
            obj = None
        return obj
        # qs = UpdateModel.objects.filter(id=id)
        # if qs.count() == 1:
        #     return qs.first()
        # return None

    def get(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({"message": "Update not applied"})
            return HttpResponse(error_data, content_type="application/json", status=400)
        json_data = obj.serialize()
        return HttpResponse(json_data, content_type="application/json")

    def put(self, request, id, *args, **kwargs):
        if not is_json(request.body):
            error_data = json.dumps({"message": "INVALID DATA"})
            return HttpResponse(error_data, content_type="application/json", status=400)

        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({"message": "Update not applied"})
            return HttpResponse(error_data, content_type="application/json", status=400)
        data = json.loads(obj.serialize())
        new_data = json.loads(request.body)

        for key, value in new_data.items():
            data[key] = value

        form = UpdateForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            print(obj)
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type="application/json", status=201)
        if form.errors:
            json_data = json.dumps(form.errors)
            print(json_data)
            return HttpResponse(json_data, content_type="application/json", status=400)

        json_data = json.dumps({"message": "Err"})
        return HttpResponse(json_data, content_type="application/json")

    def delete(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({"message": "not found"})
            return HttpResponse(error_data, content_type="application/json", status=400)
        obj.delete()
        json_data = json.dumps({"message": "DELETED"})
        return HttpResponse(json_data, content_type="application/json", status=200)


class UpdateModelListAPIView(CSRFExemptMixin, View):
    def get(self, request, *args, **kwargs):
        qs = UpdateModel.objects.all()
        json_data = qs.serialize()
        return HttpResponse(json_data, content_type="application/json")

    def post(self, request, *args, **kwargs):
        json_data = json.dumps({"message": "Unknown data"})
        status_code = 400
        form = UpdateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=True)
            print(obj)
            json_data = obj.serialize()
            return HttpResponse(json_data, content_type="application/json", status=201)
        if form.errors:
            json_data = json.dumps(form.errors)
            print(json_data)
            return HttpResponse(json_data, content_type="application/json", status=400)
        json_data = json.dumps({"message": "Not allowed"})
        return HttpResponse(
            json_data, content_type="application/json", status=status_code
        )

    def delete(self, request, *args, **kwargs):
        json_data = json.dumps({"message": "You cannot delete entire list"})
        status_code = 403  # Not allowed
        return HttpResponse(
            json_data, content_type="application/json", status=status_code
        )

