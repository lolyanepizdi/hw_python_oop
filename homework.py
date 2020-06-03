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
		self.currency_dict = {
                    'eur': [self.EURO_RATE, 'Euro'],
                    'usd': [self.USD_RATE, 'USD'],
                    'rub': [self.RUB_RATE, 'руб']
                }
		self.balance = round((self.limit - self.get_today_stats()
                        ) / self.currency_dict[currency][0], 2)
		if self.count_today < self.limit:
			return f'На сегодня осталось {self.balance} {self.currency_dict[currency][1]}'
		elif self.count_today == self.limit:
			return f'Денег нет, держись'
		elif self.count_today > self.limit:
			return f'Денег нет, держись: твой долг - {-self.balance} {self.currency_dict[currency][1]}'


class CaloriesCalculator(Calculator):
	def __init__(self, limit):
		super().__init__(limit)

	def get_calories_remained(self):
		self.calories = self.limit - self.get_today_stats()
		if self.count_today < self.limit:
			return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {self.limit - self.count_today} кКал'
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


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=1450, comment="кофе"))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(
	Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))

print(cash_calculator.get_today_cash_remained("rub"))
# должно напечататься
# На сегодня осталось 555 руб
