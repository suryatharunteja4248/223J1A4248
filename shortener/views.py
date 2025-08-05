import json
import string
import random
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from .models import ShortURL, Click

def generate_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@csrf_exempt
def create_short_url(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    original_url = data.get("url")
    validity = data.get("validity", 30)
    shortcode = data.get("shortcode")

    if not original_url:
        return JsonResponse({"error": "Missing 'url'"}, status=400)

    if shortcode:
        if ShortURL.objects.filter(shortcode=shortcode).exists():
            return JsonResponse({"error": "Shortcode already exists"}, status=400)
    else:
        while True:
            shortcode = generate_shortcode()
            if not ShortURL.objects.filter(shortcode=shortcode).exists():
                break

    obj = ShortURL.objects.create(
        original_url=original_url,
        shortcode=shortcode,
        expiry_minutes=validity
    )

    expiry_time = obj.created_at + timezone.timedelta(minutes=validity)
    expiry_iso = expiry_time.isoformat().replace("+00:00", "Z")

    return JsonResponse({
        "shortLink": f"http://127.0.0.1:8000/{shortcode}",
        "expiry": expiry_iso
    }, status=201)

def redirect_url(request, shortcode):
    try:
        obj = ShortURL.objects.get(shortcode=shortcode)
        expiry_time = obj.created_at + timezone.timedelta(minutes=obj.expiry_minutes)
        if timezone.now() > expiry_time:
            return JsonResponse({"error": "Link expired"}, status=410)

        Click.objects.create(
            short_url=obj,
            referrer=request.META.get('HTTP_REFERER', ''),
            location=request.META.get('REMOTE_ADDR', '')
        )

        return HttpResponseRedirect(obj.original_url)
    except ShortURL.DoesNotExist:
        return JsonResponse({"error": "Shortcode not found"}, status=404)

@require_GET
def get_stats(request, shortcode):
    try:
        obj = ShortURL.objects.get(shortcode=shortcode)
        expiry_time = obj.created_at + timezone.timedelta(minutes=obj.expiry_minutes)

        click_list = []
        for click in obj.clicks.all():
            click_list.append({
                "timestamp": click.timestamp.isoformat(),
                "referrer": click.referrer,
                "location": click.location
            })

        return JsonResponse({
            "shortcode": obj.shortcode,
            "original_url": obj.original_url,
            "created_at": obj.created_at.isoformat(),
            "expiry": expiry_time.isoformat(),
            "total_clicks": obj.clicks.count(),
            "clicks": click_list
        })

    except ShortURL.DoesNotExist:
        return JsonResponse({"error": "Shortcode not found"}, status=404)
