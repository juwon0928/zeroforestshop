from datetime import datetime

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path, include
from django.views.decorators.cache import never_cache

from core.models import Order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls', namespace='core')),
    path('summernote/', include('django_summernote.urls')),
    path('baton/', include('baton.urls'))
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

@never_cache
def index(self,request, extra_context=None):
    app_list = self.get_app_list(request)

    context = {
        **self.each_context(request),
        'title':self.index_title,
        'subtitle':None,
        'app_list':app_list,
        **(extra_context or {}),
    }

    request.current_app = self.name

    return TemplateResponse(request, self.index_template or 'admin/index.html', context)

origin_index = admin.site.index

def index(request, extra_context=None):
    base_date = datetime.datetime.now() - datetime.timedelta(days=7)
    order_data = {}

    for i in range(7):
        target_dttm = base_date + datetime.timedelta(days=i)
        date_key = target_dttm.strftime('%Y-%m-%d')
        target_date = datetime.date(target_dttm.year, target_dttm.month, target_dttm.day)
        order_cnt = Order.objects.filter(register_date__date=target_date).count()
        order_data[date_key] = order_cnt

    extra_context = {
        'orders': order_data}
    return origin_index(request, extra_context)

admin.site.index = index

