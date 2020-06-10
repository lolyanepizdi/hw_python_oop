import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(record.amount for record in self.records
                    if record.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                    if week_ago <= record.date <= today)

    def get_balance(self):
        balance = self.limit - self.get_today_stats()
        return balance
       

class CashCalculator(Calculator):
    USD_RATE = 71.01
    EURO_RATE = 78.13
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        currency_dict = {
                    'eur': [self.EURO_RATE, 'Euro'],
                    'usd': [self.USD_RATE, 'USD'],
                    'rub': [self.RUB_RATE, 'руб']
                }
        get_balance = self.get_balance()
        if get_balance == 0:
            return 'Денег нет, держись'
        if currency not in currency_dict:
            raise ValueError('Калькулятор не поддерживает данную валюту.')
        currency_rate, currency_name = currency_dict[currency]
        balance_cash = round((self.get_balance()) / currency_rate, 2)
        if get_balance > 0:
            return f'На сегодня осталось {balance_cash} {currency_name}'
        return (f'Денег нет, держись: твой долг - {abs(balance_cash)} ' \
                f'{currency_name}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.get_balance() > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей ' \
                    f'калорийностью не более {self.get_balance()} кКал')
        return 'Хватит есть!'


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
