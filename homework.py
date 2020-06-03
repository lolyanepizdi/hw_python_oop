import datetime as dt


class Calculator:
	def __init__(self, limit):
		self.limit = limit
		self.records = []

	def add_record(self, record):
		self.records.append(record)

	def get_today_stats(self):
		self.count_today = 0
		for rec in self.records:
			if rec.date == dt.datetime.now().date():
				self.count_today += rec.amount
		return self.count_today

	def get_week_stats(self):
		self.count_week = 0
		self.week = dt.timedelta(days=7)
		for rec in self.records:
			if rec.date >= dt.datetime.now().date() - self.week:
				self.count_week += rec.amount
		return self.count_week


class CashCalculator(Calculator):
	USD_RATE = 71.01
	EURO_RATE = 78.13
	RUB_RATE = 1.00

	def __init__(self, limit):
		super().__init__(limit)

	def get_today_cash_remained(self, currency):
		currency_dict = {
                    'eur': [self.EURO_RATE, 'Euro'],
                    'usd': [self.USD_RATE, 'USD'],
                    'rub': [self.RUB_RATE, 'руб']
                }
		balance = round((self.limit - self.get_today_stats()) / currency_dict[currency][0], 2)
		if self.count_today < self.limit:
			return f'На сегодня осталось {balance} {currency_dict[currency][1]}'
		elif self.count_today == self.limit:
			return f'Денег нет, держись'
		elif self.count_today > self.limit:
			return f'Денег нет, держись: твой долг - {-balance} {currency_dict[currency][1]}'


class CaloriesCalculator(Calculator):
	def __init__(self, limit):
		super().__init__(limit)

	def get_calories_remained(self):
		self.calories = self.limit - self.get_today_stats()
		if self.count_today < self.limit:
			return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более ' \
                   f'{self.limit - self.count_today} кКал'
		else:
			return 'Хватит есть!'


class Record:
	def __init__(self, amount, comment, date=' '):
		self.amount = amount
		self.comment = comment
		if date == ' ':
			self.date = dt.datetime.now().date()
		else:
			self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()