from .web import data_reader

def stocks(symbols, start, end):
    return data_reader(symbols, start, end)
