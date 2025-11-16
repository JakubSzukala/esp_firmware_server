import datetime
from . import models
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from .models import EspDevice, HeartbeatSignal


def index(request):
    return JsonResponse({"key":"Here will be heartbeat of ESP devices"})


@csrf_exempt
@require_http_methods(["GET", "PUT"])
def device(request: HttpRequest, chip_id: int) -> JsonResponse:
    """
    GET for getting and PUT for updating heartbeat data of the ESP device.
    """
    def save_heartbeat_signal(chip_id):
        """
        Create heartbeat entry and associate it with ESP with given id.
        """
        esp_device = EspDevice.objects.get(chip_id__exact=chip_id)
        heartbeat = HeartbeatSignal(
            esp_device=esp_device,
            heartbeat_date=datetime.datetime.now()
        )
        heartbeat.save()

    if request.method == "GET":
        try:
            # Search database for requested chip id and fetch it's heartbeat data
            device_record: EspDevice = EspDevice.objects.get(chip_id__exact=chip_id)
            heartbeat_records = HeartbeatSignal.objects.filter(esp_device__exact=device_record)
            return JsonResponse(data={chip_id : list(heartbeat_records.values())})
        except:
            # Failed to find required data
            raise Http404()
    elif request.method == "PUT":
        if EspDevice.objects.filter(chip_id__exact=chip_id).exists():
            # Create heartbeat entry
            save_heartbeat_signal(chip_id)
            return JsonResponse(data={}, status=204)
        else:
            # Create new ESP device entry with given chip id
            EspDevice(chip_id=chip_id).save()
            save_heartbeat_signal(chip_id)

            # Return location of that new resource
            url = reverse(device, args=[chip_id])
            response = JsonResponse(data={"chip_id":chip_id}, status=201)
            response.headers["Location"] = url
            return response
    raise Http404()

