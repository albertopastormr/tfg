from backend.solar.hours_analysis import generate_hours_data as data_hours
from backend.solar.month_analysis import generate_month_data as data_month
from backend.solar.solar_batterie import Batteries
from bs4 import BeautifulSoup
import plotly.graph_objs as go


def generate_analysis_month(center, date, num_panels):
    return data_month.analysis_monthly(center=center, date=date, num_panels=num_panels)


def generate_hourly_graphics(consume_ret, dates, extra_information=None):
    date_day = []
    for hour in dates:
        if hour[5:8] == "00":
            date_day.append('{}:00'.format(hour[0:4]))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=consume_ret, name="Consume"))

    fig.update_layout(title_text='Time Series with Rangeslider',
                      xaxis_rangeslider_visible=True, xaxis_title="Hours", yaxis_title="Consume (Kw/h)")

    soup = BeautifulSoup(fig.to_html())
    divs = soup.findAll('div')

    if extra_information is not None:
        fig_rest = go.Figure()
        fig_rest.add_trace(go.Scatter(x=date_day, y=extra_information, name="Cost"))

        fig_rest.update_layout(title_text='Time Series with Rangeslider',
                          xaxis_rangeslider_visible=True, xaxis_title="Hours", yaxis_title="Consume (Kw/h)")

        soup = BeautifulSoup(fig_rest.to_html())
        divs_cost = soup.findAll('div')
    else:
        return divs[0]
    return divs[0], divs_cost[0]


def consume_hourly_generic(center, date, num_panels):
    consume_ret, extra_information, dates = data_hours.analysis_hourly(center = center, date = date, num_panels=num_panels, solar_batterie=False)
    return generate_hourly_graphics(consume_ret = consume_ret, extra_information = extra_information, dates = dates)


def consume_hourly_with_batteries(center, date, num_panels, number_serie_batteries, power_battery, min_discharging_percent):
    bt = Batteries(number_serie=number_serie_batteries, power=power_battery, min_discharging_percent=min_discharging_percent)
    consume_ret, _, dates = data_hours.analysis_hourly(center=center, date=date, num_panels=num_panels, solar_batterie=bt)
    return generate_hourly_graphics(consume_ret=consume_ret, dates=dates)
