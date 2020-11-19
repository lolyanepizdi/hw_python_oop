import datetime as dt
from collections import namedtuple
Currency = namedtuple('Currency', 'rate name')

class Record():
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.comment = comment
        if date == '':
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator():
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_count = 0
        for x in self.records:
            if x.date == dt.datetime.now().date():
                today_count += x.amount
        return today_count

    def get_week_stats(self):
        week_count = 0
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        for x in self.records:
            if week_ago < x.date <= today:
                week_count += x.amount 
        return week_count


class CashCalculator(Calculator):
    USD_RATE = 60.70
    EURO_RATE = 70.56
    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency):
        currency_dict = {
            'rub': Currency('руб', 1),
            'eur': Currency('Euro', self.EURO_RATE),
            'usd': Currency('USD', self.USD_RATE),
        }
        currency_name = currency_dict[currency][0]
        currency_rate = currency_dict[currency][1]
        cash_remained = self.limit - self.get_today_stats()
        cash_in_currency = round((cash_remained / currency_rate), 2)
        
        if cash_remained > 0:
            return f'На сегодня осталось {cash_in_currency} {currency_name}'
        if cash_remained == 0:
            return f'Денег нет, держись'
        elif cash_remained < 0:
            return f'Денег нет, держись: твой долг - {abs(cash_in_currency)} {currency_name}'
        


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {calories_remained} кКал'
        else: 
            return 'Хватит есть!'

