import datetime


class Converter:
    @staticmethod
    # date example: 13-03-2019 19:18
    def convert(date):
        try:
            return datetime.datetime.strptime(date, "%d-%m-%Y %H:%M")
        except IndexError as ie:
            print(ie)

    @staticmethod
    # date example: 13-03-2019
    def convert_date(date):
        try:
            return datetime.datetime.strptime(date, "%d-%m-%Y")
        except IndexError as ie:
            print(ie)
