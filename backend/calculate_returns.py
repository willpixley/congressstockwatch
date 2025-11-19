import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()
from server.models import Trade, CongressMember


def get_trade_history(member :CongressMember):
    holdings = {}
    trades= Trade.objects.filter(member_id = member.bio_guide_id).order_by('date')
    for trade in trades:
        if trade.stock.ticker in holdings:
            if trade.type == 'B':
                holdings[trade.stock.ticker] += trade.amount
            else:
                holdings[trade.stock.ticker] -= trade.amount
        else:
            if trade.type == 'B':
                holdings[trade.stock.ticker] = trade.amount
            else:
                holdings[trade.stock.ticker] = -trade.amount
    print(holdings)
    
