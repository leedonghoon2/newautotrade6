import time

import pyupbit



access = 

secret =

upbit = pyupbit.Upbit(access, secret)



# 코인 리스트

coin_list = ["BTC", "ETH", "XRP"]



# 매수 기준 RSI 값

buy_rsi = 30



while True:

    try:

        for coin in coin_list:

            # 코인의 잔고와 현재가 가져오기

            balance = upbit.get_balance("KRW-" + coin)

            current_price = pyupbit.get_current_price("KRW-" + coin)



            # RSI 가져오기

            rsi = pyupbit.get_indicators("KRW-" + coin, "minute5", 14)['RSI'][-1]



            # RSI 값이 buy_rsi보다 작을 때 매수

            if rsi <= buy_rsi and balance == 0:

                # 매수 금액 설정

                buy_amount = 10000

                # 시장가 주문으로 매수

                upbit.buy_market_order("KRW-" + coin, buy_amount)



            # RSI 값이 70을 넘어갈 때 매도

            if rsi >= 70 and balance > 0:

                # 절반 매도

                upbit.sell_market_order("KRW-" + coin, balance/2)

                # 이후 RSI 값이 70 아래로 떨어질 때 나머지 절반 매도

                while True:

                    rsi = pyupbit.get_indicators("KRW-" + coin, "minute5", 14)['RSI'][-1]

                    if rsi <= 70:

                        remaining_balance = upbit.get_balance("KRW-" + coin)

                        upbit.sell_market_order("KRW-" + coin, remaining_balance)

                        break

                    time.sleep(300) # 5분 대기



            # 5초 대기

            time.sleep(5)

    except Exception as e:

        print(e)

        time.sleep(1)

