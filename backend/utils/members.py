from server.models import Stock, Trade, CongressMember
from django.forms.models import model_to_dict


def get_returns(trade: Trade):
    og = trade.price_at_trade
    current = trade.current_price
    if og == 0:
        return 0
    prop_change = (current - og) / og
    if trade.type == "s":
        prop_change = prop_change * -1
    return prop_change * trade.amount


def get_trade_for_member(id):
    trades = Trade.objects.filter(member_id=id).order_by("-date")
    results = []
    history = {}
    purchases = 0
    sales = 0
    volume = 0
    returns = 0
    flagged_volume = 0
    flagged_returns = 0
    for trade in trades:
        trade_dict = model_to_dict(trade)
        volume += trade.amount
        if trade.type == "b":
            purchases += 1
        else:
            sales += 1
        # Add related objects as dictionaries
        trade_dict["member"] = model_to_dict(
            trade.member
        )  # Assuming ForeignKey to Member model
        trade_dict["stock"] = model_to_dict(trade.stock)
        trade_dict["sector"] = model_to_dict(trade.stock.sector)
        results.append(trade_dict)
        returns += get_returns(trade)
        if trade.flagged:
            flagged_returns += get_returns(trade)
            flagged_volume += trade.amount
    try:
        weighted_return = (returns / volume) * 100
    except:
        weighted_return = 0
    try:
        weighted_flagged_returns = (flagged_returns / flagged_volume) * 100
    except:
        weighted_flagged_returns = 0
    history["volume"] = volume
    history["purchases"] = purchases
    history["sales"] = sales
    history["weighted_return"] = weighted_return
    history["weighted_flagged_return"] = weighted_flagged_returns
    return results, history
