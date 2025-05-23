from apps.urls.account import urlpatterns as account_urls
# from apps.urls.order import urlpatterns as order_urls
from apps.urls.product import urlpatterns as product_urls
from apps.urls.user import urlpatterns as user_urls

urlpatterns = [
    *user_urls,
    *account_urls,
    *product_urls,
    # *order_urls,
]
