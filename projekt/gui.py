import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

CALC_FONT = ('Arial', 10)
BUTTONS_STYLE = 'raised'
ICON = 'images\\favicon.ico'
ROOT_SIZE = '575x410'
STATS_FONT1 = ('Arial', 12)
STATS_FONT2 = ('Arial', 12, 'underline')
STATS_FONT3 = ('Arial', 12, 'bold')
STATS_SPACE = 15
BACKGROUND = 'images\\background.png'
GREEN = '#008000'
RED = '#FF0000'
BLUE = '#0000FF'
BACKGROUND_COLOR = '#CCCCFF'
STATS_COLOR = BACKGROUND_COLOR
CALC_COLOR = BACKGROUND_COLOR


class Gui:
    def __init__(self):
        # main frame
        self.root = tk.Tk()
        self.root.title('Kalkulator kryptowalut')
        self.root.iconbitmap(ICON)
        self.root.geometry(ROOT_SIZE)
        self.root.resizable(False, False)
        self.root.config(bg=BACKGROUND_COLOR)

        # calculator
        self.calculator_frame = tk.LabelFrame(self.root, text='KALKULATOR')
        self.calculator_frame.config(bg=CALC_COLOR)
        self.rate_label = tk.Label(self.calculator_frame, borderwidth=2, relief='ridge', font=CALC_FONT)
        self.rate_label.config(bg='white')
        self.currency1_entry = tk.Entry(self.calculator_frame, width=26, borderwidth=0, font=CALC_FONT)
        self.currencies1_combobox = ttk.Combobox(self.calculator_frame, width=10, state='readonly', font=CALC_FONT)
        self.currency2_label = tk.Label(self.calculator_frame, width=23, borderwidth=0, anchor='w', font=CALC_FONT)
        self.currencies2_combobox = ttk.Combobox(self.calculator_frame, width=10, state='readonly', font=CALC_FONT)
        self.calc_button = tk.Button(self.calculator_frame, text='OBLICZ', padx=90, pady=5, font=CALC_FONT,
                                     relief=BUTTONS_STYLE)
        self.calc_button.config(bg='white')
        self.place_calculator()

        # stats
        self.stats_frame = tk.LabelFrame(self.root, text='STATYSTYKI')
        self.stats_frame.config(bg=STATS_COLOR)
        self.stats_market = tk.Label(self.stats_frame, width=10, borderwidth=10, anchor='w', font=STATS_FONT3)
        self.stats_market.config(bg=STATS_COLOR)
        self.stats_rate = tk.Label(self.stats_frame, width=10, borderwidth=10, anchor='w', font=STATS_FONT3)
        self.stats_rate.config(bg=STATS_COLOR)
        self.stats_diff = tk.Label(self.stats_frame, width=15, borderwidth=10, anchor='w', font=STATS_FONT3)
        self.stats_diff.config(bg=STATS_COLOR)
        self.stats_diff2 = tk.Label(self.stats_frame, width=15, borderwidth=10, anchor='w', font=STATS_FONT3)
        self.stats_diff2.config(bg=STATS_COLOR)
        self.btc_label = tk.Label(self.stats_frame, width=10, borderwidth=STATS_SPACE, anchor='w', font=STATS_FONT2)
        self.btc_label.config(bg=STATS_COLOR)
        self.btc_rate = tk.Label(self.stats_frame, width=10, borderwidth=0, anchor='w', font=STATS_FONT1)
        self.btc_rate.config(bg=STATS_COLOR)
        self.btc_diff = tk.Label(self.stats_frame, width=15, borderwidth=0, anchor='w', font=STATS_FONT1)
        self.btc_diff.config(bg=STATS_COLOR)
        self.btc_diff2 = tk.Label(self.stats_frame, width=15, borderwidth=0, anchor='w', font=STATS_FONT1)
        self.btc_diff2.config(bg=STATS_COLOR)
        self.ltc_label = tk.Label(self.stats_frame, width=10, borderwidth=STATS_SPACE, anchor='w', font=STATS_FONT2)
        self.ltc_label.config(bg=STATS_COLOR)
        self.ltc_rate = tk.Label(self.stats_frame, width=10, borderwidth=0, anchor='w', font=STATS_FONT1)
        self.ltc_rate.config(bg=STATS_COLOR)
        self.ltc_diff = tk.Label(self.stats_frame, width=15, borderwidth=0, anchor='w', font=STATS_FONT1)
        self.ltc_diff.config(bg=STATS_COLOR)
        self.ltc_diff2 = tk.Label(self.stats_frame, width=15, borderwidth=0, anchor='w', font=STATS_FONT1)
        self.ltc_diff2.config(bg=STATS_COLOR)
        self.doge_label = tk.Label(self.stats_frame, width=10, borderwidth=STATS_SPACE, anchor='w', font=STATS_FONT2)
        self.doge_label.config(bg=STATS_COLOR)
        self.doge_rate = tk.Label(self.stats_frame, width=10, borderwidth=0, anchor='w', font=STATS_FONT1)
        self.doge_rate.config(bg=STATS_COLOR)
        self.doge_diff = tk.Label(self.stats_frame, width=15, borderwidth=0, anchor='w', font=STATS_FONT1)
        self.doge_diff.config(bg=STATS_COLOR)
        self.doge_diff2 = tk.Label(self.stats_frame, width=15, borderwidth=0, anchor='w', font=STATS_FONT1)
        self.doge_diff2.config(bg=STATS_COLOR)
        self.eth_label = tk.Label(self.stats_frame, width=10, borderwidth=STATS_SPACE, anchor='w', font=STATS_FONT2)
        self.eth_label.config(bg=STATS_COLOR)
        self.eth_rate = tk.Label(self.stats_frame, width=10, borderwidth=0, anchor='w', font=STATS_FONT1)
        self.eth_rate.config(bg=STATS_COLOR)
        self.eth_diff = tk.Label(self.stats_frame, width=15, borderwidth=0, anchor='w', font=STATS_FONT1)
        self.eth_diff.config(bg=STATS_COLOR)
        self.eth_diff2 = tk.Label(self.stats_frame, width=15, borderwidth=0, anchor='w', font=STATS_FONT1)
        self.eth_diff2.config(bg=STATS_COLOR)

        # chart
        self.chart = tk.Toplevel().withdraw()
        self.chart_combobox = ttk.Combobox(self.stats_frame, width=15, state='readonly', font=CALC_FONT)
        self.chart_button = tk.Button(self.stats_frame, text='WYKRES', padx=50, pady=5, font=CALC_FONT,
                                      relief=BUTTONS_STYLE)
        self.chart_button.config(bg='white')
        self.place_stats()

    def place_calculator(self):
        self.calculator_frame.pack(side='top', fill='x')

        self.rate_label.grid(row=3, column=4, padx=10, pady=5)

        self.currency1_entry.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.currencies1_combobox.grid(row=3, column=3)

        self.currency2_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        self.currency2_label.config(bg='white')

        self.currencies2_combobox.grid(row=4, column=3)

        self.calc_button.grid(row=4, column=4)

    def place_stats(self):
        self.stats_frame.pack(side='bottom', fill='x')

        self.stats_market.grid(row=2, column=9)
        self.stats_market.configure(text='RYNEK')
        self.stats_rate.grid(row=2, column=10)
        self.stats_rate.configure(text='KURS')
        self.stats_diff.grid(row=2, column=11)
        self.stats_diff.configure(text='ZMIANA(%)')
        self.stats_diff2.grid(row=2, column=12)
        self.stats_diff2.configure(text='ZMIANA($)')

        self.btc_label.configure(text='BTC-USD')
        self.btc_label.grid(row=3, column=9)
        self.btc_rate.grid(row=3, column=10)
        self.btc_rate.configure(text='0.0')
        self.btc_diff.grid(row=3, column=11)
        self.btc_diff.config(text='0.0 %')
        self.btc_diff2.grid(row=3, column=12)
        self.btc_diff2.config(text='0.0')

        self.ltc_label.configure(text='LTC-USD')
        self.ltc_label.grid(row=4, column=9)
        self.ltc_rate.grid(row=4, column=10)
        self.ltc_rate.configure(text='0.0')
        self.ltc_diff.grid(row=4, column=11)
        self.ltc_diff.config(text='0.0 %')
        self.ltc_diff2.grid(row=4, column=12)
        self.ltc_diff2.config(text='0.0')

        self.doge_label.configure(text='DOGE-USD')
        self.doge_label.grid(row=5, column=9)
        self.doge_rate.grid(row=5, column=10)
        self.doge_rate.configure(text='0.0')
        self.doge_diff.grid(row=5, column=11)
        self.doge_diff.config(text='0.0 %')
        self.doge_diff2.grid(row=5, column=12)
        self.doge_diff2.config(text='0.0')

        self.eth_label.configure(text='ETH-USD')
        self.eth_label.grid(row=6, column=9)
        self.eth_rate.grid(row=6, column=10)
        self.eth_rate.configure(text='0.0')
        self.eth_diff.grid(row=6, column=11)
        self.eth_diff.config(text='0.0 %')
        self.eth_diff2.grid(row=6, column=12)
        self.eth_diff2.config(text='0.0')

        self.chart_button.grid(row=7, column=11)
        self.chart_combobox.grid(row=7, column=10, padx=5, pady=5)

    def close_chart(self):
        self.chart.destroy()
        self.chart_button['state'] = 'normal'

    def draw_chart(self, data_frame, title):
        self.chart_button['state'] = 'disable'
        self.chart = tk.Toplevel(self.root)
        self.chart.iconbitmap(ICON)
        self.chart.resizable(False, False)
        self.chart.protocol('WM_DELETE_WINDOW', self.close_chart)
        figure = plt.Figure(figsize=(9, 7), dpi=100)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, self.chart)
        line.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH)
        data_frame = data_frame[['Time', 'Rates']].groupby('Time').sum()
        data_frame.plot(kind='line', legend=False, ax=ax, color='r', fontsize=8)
        ax.set_title(title)

    def run(self):
        self.root.mainloop()

    @staticmethod
    def set_label_txt(label, message):
        label.config(text=message)

    @staticmethod
    def set_button_command(button, command):
        button.config(command=command)

    @staticmethod
    def set_combobox_values(box, values, current):
        box['values'] = values
        box.current(current)

    @staticmethod
    def set_entry_value(entry, value):
        entry.insert(0, value)

    @staticmethod
    def set_label_font_colour(label, colour):
        label.config(fg=colour)

    @staticmethod
    def throw_error(title, message):
        messagebox.showerror(title, message)


if __name__ == '__main__':
    gui = Gui()
    gui.run()
