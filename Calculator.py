import datetime as dt


class Record:
    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, amount, comment, date=dt.date.today()):
        self.amount = amount
        self.comment = comment

        if type(date) == dt.date:
            self.date = date
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records += [record]

    def get_stats(self, quantity_of_days):
        spent_money = 0
        last_date = dt.date.today() - dt.timedelta(days=quantity_of_days)

        for record in self.records:
            if last_date < record.date <= dt.date.today():
                spent_money += record.amount
        return spent_money

    def get_today_stats(self):
        return self.get_stats(1)

    def get_week_stats(self):
        return self.get_stats(7)


class CashCalculator(Calculator):
    def get_today_cash_remained(self, currency):
        USD_RATE = 75
        EURO_RATE = 90
        spent = self.get_today_stats()
        remained = self.limit - spent

        if remained == 0:
            return f"Денег нет, держись"

        if currency == 'rub':
            left_money = remained
            currency_name = "руб"
        if currency == "usd":
            left_money = round(remained / USD_RATE, 2)
            currency_name = "USD"
        if currency == "eur":
            left_money = round(remained / EURO_RATE, 2)
            currency_name = "Euro"
        if remained < 0:
            return f"Денег нет, держись: твой долг - {left_money} {currency_name}"

        else:
            return f"На сегодня осталось {left_money} {currency_name}"


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        spent = self.get_today_stats()
        remained = self.limit - spent

        if remained > 0:
            return f'Сегодня можно съесть что-нибудь ещё, ' \
                   f'но с общей калорийностью не более {remained} кКал'

        else:
            return f'Хватит есть!'


cash_calculator = CashCalculator(1000)
cash_calculator.add_record(Record(amount=500, comment="кофе"))
cash_calculator.add_record(Record(amount=100, comment="Сереге за обед"))
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
print(cash_calculator.get_today_cash_remained('rub'))
print(cash_calculator.get_today_cash_remained('eur'))
calories_calculator = CaloriesCalculator(1000)
calories_calculator.add_record(Record(amount=500, comment="кофе"))
calories_calculator.add_record(Record(amount=100, comment="Сереге за обед"))
calories_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
print(calories_calculator.get_calories_remained())
