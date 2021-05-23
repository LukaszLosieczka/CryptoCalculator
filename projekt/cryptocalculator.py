import api
from gui import*
from pandas import DataFrame
import datetime

ARROW_UP = '\u2191'
ARROW_DOWN = '\u2193'
CHARTS_LIMIT = 360
BASE_CRYPTO = 'BTC'
BASE_CURRENCY = 'USD'
BTC_FILE = 'rates_history/btc.txt'
LTC_FILE = 'rates_history/ltc.txt'
DOGE_FILE = 'rates_history/doge.txt'
ETH_FILE = 'rates_history/eth.txt'


# calculation variables
currency1 = BASE_CRYPTO
currency2 = BASE_CURRENCY
rate = api.get_average_rate(currency1, currency2)
average_rates = {f'{currency1}-{currency2}': rate}
initial_rates = None
rates_history = {'BTC': ([], []), 'LTC': ([], []), 'DOGE': ([], []), 'ETH': ([], [])}

gui = Gui()


def write_data():
    paths = {'BTC': BTC_FILE, 'LTC': LTC_FILE, 'DOGE': DOGE_FILE, 'ETH': ETH_FILE}
    for key in rates_history.keys():
        try:
            file = open(paths[key], 'w')
            rates = rates_history[key][0]
            time = rates_history[key][1]
            file.write('\tRates\t\t\t\tTime\n')
            count = 0
            for i in range(0, len(rates)):
                count += 1
                file.write(f'{count}\t{rates[i]}\t\t\t\t{time[i]}\n')
            file.close()
        except IOError:
            gui.throw_error('Error', f'some problem with writing to file "{paths[key]}" occurred')


def read_data():
    paths = {'BTC': BTC_FILE, 'LTC': LTC_FILE, 'DOGE': DOGE_FILE, 'ETH': ETH_FILE}
    for key in rates_history.keys():
        try:
            file = open(paths[key], 'r')
            lines = file.readlines()
            for i in range(1, len(lines)):
                line = lines[i].split()
                rates_history[key][0].append(float(line[1]))
                rates_history[key][1].append(line[2])
            file.close()
        except IOError:
            gui.throw_error('Error', f'some problem with reading from file "{paths[key]}" occurred')


def add_history_rates(rates):
    for key in rates_history.keys():
        history = rates_history[key][0]
        dates = rates_history[key][1]
        if len(history) == CHARTS_LIMIT:
            history.pop(0)
            dates.pop(0)
        history.append(rates[key])
        dates.append(datetime.datetime.now().strftime('%d/%m,%H:%M:%S'))
        rates_history[key] = history, dates


def calculate_diff(markets):
    global initial_rates
    # gui labels
    labels = {gui.btc_rate: (gui.btc_diff, gui.btc_diff2), gui.ltc_rate: (gui.ltc_diff, gui.ltc_diff2),
              gui.doge_rate: (gui.doge_diff, gui.doge_diff2), gui.eth_rate: (gui.eth_diff, gui.eth_diff2)}
    current_rates = api.get_current_rate(markets.values(), BASE_CURRENCY)
    # assigning initial rates
    if initial_rates is None:
        initial_rates = current_rates
    # updating rates history
    add_history_rates(current_rates)
    for label in labels:
        initial = initial_rates[markets[label]]
        previous = float(label['text'])
        current = current_rates[markets[label]]
        diff = (current - previous)
        if diff > 0:
            gui.set_label_font_colour(label, GREEN)
        elif diff < 0:
            gui.set_label_font_colour(label, RED)
        else:
            gui.set_label_font_colour(label, BLUE)
        value_diff = round(current - initial, 4)
        percent_diff = round((value_diff / initial) * 100, 4)
        percent_label = labels[label][0]
        value_label = labels[label][1]
        if percent_diff > 0:
            arrow = ARROW_UP
            color = GREEN
        elif percent_diff < 0:
            arrow = ARROW_DOWN
            color = RED
        else:
            arrow = ''
            color = BLUE
        gui.set_label_txt(percent_label, f'{arrow} {abs(percent_diff)} %')
        gui.set_label_font_colour(percent_label, color)
        gui.set_label_txt(value_label, f'{arrow} {abs(value_diff)}')
        gui.set_label_font_colour(value_label, color)
    return current_rates


def stats_updating():
    markets = {gui.btc_rate: 'BTC', gui.ltc_rate: 'LTC', gui.doge_rate: 'DOGE', gui.eth_rate: 'ETH'}
    usd_rates = calculate_diff(markets)
    for label in markets.keys():
        gui.set_label_txt(label, usd_rates[markets[label]])
    gui.root.after(10000, stats_updating)


def opposite_market(market):
    tmp = market.split('-')
    return f'{tmp[1]}-{tmp[0]}'


def get_market_rate(market):
    markets = [market, opposite_market(market)]
    for m in markets:
        if m not in average_rates.keys():
            average_rates[m] = api.get_average_rate(m.split('-')[0], m.split('-')[1])
        if average_rates[m] is None:
            continue
        else:
            average_rates[opposite_market(m)] = 1 / average_rates[m]
            break
    return average_rates[market]


def calculate():
    global currency1, currency2, rate
    currency1_tmp = gui.currencies1_combobox.get()
    currency2_tmp = gui.currencies2_combobox.get()
    crypto_rate_tmp = rate
    if currency1_tmp == currency2_tmp:
        crypto_rate_tmp = 1
    elif currency1_tmp != currency1 or currency2_tmp != currency2:
        market = f'{currency1_tmp}-{currency2_tmp}'
        crypto_rate_tmp = get_market_rate(market)
        if crypto_rate_tmp is None:
            market1 = f'{currency1_tmp}-{BASE_CRYPTO}'
            market2 = f'{BASE_CRYPTO}-{currency2_tmp}'
            to_base = get_market_rate(market1)
            from_base = get_market_rate(market2)
            crypto_rate_tmp = to_base * from_base
            average_rates[market] = crypto_rate_tmp
    currency1 = currency1_tmp
    currency2 = currency2_tmp
    rate = crypto_rate_tmp
    gui.set_label_txt(gui.rate_label, f'1 {currency1} to w przeliczeniu {round(rate, 4)} {currency2}')
    try:
        value = abs(float(gui.currency1_entry.get()))
        result = round(value * rate, 4)
        gui.set_label_txt(gui.currency2_label, result)
    except ValueError:
        gui.throw_error('Error', 'Podana wartość nie jest liczbą')


def initialize_chart():
    currency = gui.chart_combobox.get().split('-')[0]
    title = f'{currency} wykres kursu (1h)'
    rates = rates_history[currency][0]
    time = rates_history[currency][1]
    data = {'Rates': rates, 'Time': time}
    data_frame = DataFrame(data, columns=['Time', 'Rates'])
    gui.draw_chart(data_frame, title)


def initialize_gui():
    # calculator initialization
    gui.set_label_txt(gui.rate_label, f'1 {currency1} to w przeliczeniu {round(rate, 4)} {currency2}')

    gui.set_entry_value(gui.currency1_entry, '1')
    gui.set_combobox_values(gui.currencies1_combobox, api.CURRENCIES, 0)

    gui.set_label_txt(gui.currency2_label, round(rate, 4))
    gui.set_combobox_values(gui.currencies2_combobox, api.CURRENCIES, 5)

    gui.set_button_command(gui.calc_button, calculate)

    # stats initialization
    current_rates = api.get_current_rate(['BTC', 'LTC', 'DOGE', 'ETH'], 'USD')

    gui.set_label_txt(gui.stats_market, 'RYNEK')
    gui.set_label_txt(gui.stats_rate, 'KURS')
    gui.set_label_txt(gui.stats_diff, 'ZMIANA(%)')

    gui.set_label_txt(gui.btc_label, 'BTC-USD')
    gui.set_label_txt(gui.btc_rate, current_rates['BTC'])
    gui.set_label_txt(gui.btc_diff, '0.0 %')

    gui.set_label_txt(gui.ltc_label, 'LTC-USD')
    gui.set_label_txt(gui.ltc_rate, current_rates['LTC'])
    gui.set_label_txt(gui.ltc_diff, '0.0 %')

    gui.set_label_txt(gui.doge_label, 'DOGE-USD')
    gui.set_label_txt(gui.doge_rate, current_rates['DOGE'])
    gui.set_label_txt(gui.doge_diff, '0.0 %')

    gui.set_label_txt(gui.eth_label, 'ETH-USD')
    gui.set_label_txt(gui.eth_rate, current_rates['ETH'])
    gui.set_label_txt(gui.eth_diff, '0.0 %')

    gui.set_combobox_values(gui.chart_combobox, ('BTC-USD', 'LTC-USD', 'DOGE-USD', 'ETH-USD'), 0)

    gui.set_button_command(gui.chart_button, initialize_chart)

    stats_updating()
    gui.run()


if __name__ == '__main__':
    read_data()
    initialize_gui()
    write_data()
