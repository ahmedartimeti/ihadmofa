import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from .models import PushSubscription


def _subscription_payload(subscription):
    return {
        'endpoint': subscription.endpoint,
        'keys': {
            'p256dh': subscription.p256dh,
            'auth': subscription.auth,
        },
    }


def _send_web_push(subscription, title, body):
    try:
        from pywebpush import WebPushException, webpush
    except Exception:
        return False, 'مكتبة pywebpush غير مثبتة بعد.'

    private_key = getattr(settings, 'WEBPUSH_VAPID_PRIVATE_KEY', '')
    contact = getattr(settings, 'WEBPUSH_VAPID_ADMIN_EMAIL', '')
    if not private_key or not contact:
        return False, 'مفاتيح Web Push غير مضافة في إعدادات السيرفر.'

    payload = json.dumps({'title': title, 'body': body, 'url': '/'}, ensure_ascii=False)
    try:
        webpush(
            subscription_info=_subscription_payload(subscription),
            data=payload,
            vapid_private_key=private_key,
            vapid_claims={'sub': f'mailto:{contact}'},
        )
        return True, 'تم إرسال التنبيه.'
    except WebPushException as exc:
        if getattr(exc, 'response', None) and exc.response.status_code in (404, 410):
            subscription.is_active = False
            subscription.save(update_fields=['is_active', 'updated_at'])
        return False, 'تعذر إرسال التنبيه لهذا الجهاز.'


@require_GET
def manifest(request):
    return JsonResponse({
        'name': 'IHAD',
        'short_name': 'IHAD',
        'start_url': '/',
        'scope': '/',
        'display': 'standalone',
        'dir': 'rtl',
        'lang': 'ar',
        'background_color': '#eef3f8',
        'theme_color': '#312e81',
        'icons': [
            {'src': settings.STATIC_URL + 'img/logo.jpg', 'sizes': '192x192', 'type': 'image/jpeg'},
            {'src': settings.STATIC_URL + 'img/logo.jpg', 'sizes': '512x512', 'type': 'image/jpeg'},
        ],
    })


@require_GET
def service_worker(request):
    service_worker_path = settings.BASE_DIR / 'static' / 'pwa' / 'service-worker.js'
    return FileResponse(open(service_worker_path, 'rb'), content_type='application/javascript')


@login_required
@require_GET
def public_key(request):
    key = getattr(settings, 'WEBPUSH_VAPID_PUBLIC_KEY', '')
    return JsonResponse({'publicKey': key, 'configured': bool(key)})


@login_required
@require_POST
def subscribe(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'ok': False, 'message': 'بيانات الاشتراك غير صحيحة.'}, status=400)

    endpoint = data.get('endpoint')
    keys = data.get('keys') or {}
    p256dh = keys.get('p256dh')
    auth = keys.get('auth')
    if not endpoint or not p256dh or not auth:
        return JsonResponse({'ok': False, 'message': 'بيانات الجهاز غير مكتملة.'}, status=400)

    subscription, _ = PushSubscription.objects.update_or_create(
        endpoint=endpoint,
        defaults={
            'user': request.user,
            'p256dh': p256dh,
            'auth': auth,
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'is_active': True,
        },
    )
    return JsonResponse({'ok': True, 'message': 'تم تفعيل تنبيهات هذا الجهاز.', 'id': subscription.pk})


@login_required
@require_POST
def unsubscribe(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = {}
    endpoint = data.get('endpoint')
    if endpoint:
        PushSubscription.objects.filter(user=request.user, endpoint=endpoint).update(is_active=False)
    return JsonResponse({'ok': True, 'message': 'تم إيقاف تنبيهات هذا الجهاز.'})


@login_required
@require_POST
def test_push(request):
    subscription = PushSubscription.objects.filter(user=request.user, is_active=True).first()
    if not subscription:
        return JsonResponse({'ok': False, 'message': 'لم يتم تفعيل أي جهاز بعد.'}, status=400)
    ok, message = _send_web_push(subscription, 'تنبيه تجريبي', 'تم تجهيز تنبيهات المذكر اليومي على هذا الجهاز.')
    return JsonResponse({'ok': ok, 'message': message}, status=200 if ok else 400)
