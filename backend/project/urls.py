"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from server.views import (
    get_ticker,
    get_trades,
    get_flagged_trades,
    get_member_trades,
    get_members,
    get_market_trends,
    test_db,
    run_daily_updates,
)
from django.http import HttpResponse

from server.handlers.stock import (
    get_stock_history,
    get_stock_news,
    get_stock_profile,
)


def health_check(request):
    print("Health Check Called")
    return HttpResponse("OK")


urlpatterns = [
    path("", health_check),  # Base URL returns 200 OK
    path("test/db", test_db),  # GET
    path("admin/", admin.site.urls),  # GET
    path("stock/", get_ticker),  # GET
    path("stock/history", get_stock_history),  # GET
    path("stock/news", get_stock_news),
    path("stock/profile", get_stock_profile),
    path("trades/", get_trades),  # GET
    path("trades/flagged", get_flagged_trades),  # GET
    path("trades/member", get_member_trades),  # GET
    path("members/", get_members),  # GET
    path("market/trends/", get_market_trends),  # GET
    path("daily-updates/", run_daily_updates),  # POST
]
