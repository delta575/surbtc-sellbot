from surbtc import SURBTC
import yaml
import random
import time

authkeys = yaml.load(open("authkeys.yml").read())

surbtc_key = authkeys['key']
surbtc_secret = authkeys['secret']

market = 'btc-clp'

surbtc = SURBTC(key=surbtc_key, secret=surbtc_secret, test=False, timeout=120)

def quote_price(amount):
    quote = float(surbtc.quotation(market_id=market, quotation_type='bid', reverse=False, amount=amount)['quotation']['quote_balance_change'][0])
    price = -quote/amount
    return price

if __name__ == '__main__':

    while True:
        # Cancel Active Orders
        active_orders = surbtc.orders(market, state='pending')['orders']
        for order in active_orders:
            surbtc.cancel_order(order['id'])

        # Recover available BTC balance
        available_btc = surbtc.balance('btc')['balance']['available_amount'] /1e8

        if available_btc >= 0.0001: # If available BTC amount is higher than SURBTC's minimun order amount
            if available_btc > 0.9: # If the amount is high enough then sell some and limit sell the rest
                rand = random.uniform(0.6, 0.9)
                amount1 = int(rand * 1e8)
                amount2 = int((available_btc - rand) * 1e8)
                
                price = int(quote_price(0.6) * 1e2)

                surbtc.new_order(market_id=market, order_type='ask', limit=0, amount=amount1, price_type='market')
                surbtc.new_order(market_id=market, order_type='ask', limit=price, amount=amount2, price_type='limit')

            else: # If the amount is small then sell all
                amount = available_btc
                surbtc.new_order(market_id=market, order_type='ask', limit=0, amount=amount, price_type='market')

        time.sleep(random.uniform(60*30, 60*60)) # Sleeps 30 to 60 minutes