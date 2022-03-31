import matplotlib.pyplot as plt
# from ipywidgets import interact
import mplfinance as mpf
import finplot as fplt
import plotly.graph_objects as go


# def visualize_mplfinance(df):
#     mpf.plot(df[['시가', '고가', '저가', '현재가','거래량']], type = 'candle', mav = (5,10,20,60,90,120), volume = True)
#     mpf.show()

def visualize_finplot(df):
    fplt.candlestick_ochl(df[['시가', '현재가', '고가', '저가']])
    fplt.plot(df.현재가.rolling(5).mean())
    fplt.plot(df.현재가.rolling(10).mean())
    fplt.show()


def visualize_plotly(df):
    fig = go.Figure(
        data = [
            go.Candlestick(
                x=df.index,
                open = df['시가'],
                high = df['고가'],
                low = df['저가'],
                close = df['현재가'],
                increasing_line_color = 'red',
                decreasing_line_color = 'blue'
            )
        ]
    )
    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=list(df.index), y=list(df.현재가)))
    fig.update_layout(title_text = 'Time Series with Range Slider and Selectors')
    fig.update_layout(
        xaxis = dict(
            rangeselector = dict(
                buttons = list([
                    dict(
                        count = 5,
                        label = '5d',
                        step = 'day',
                        stepmode = 'backward'),
                    dict(
                        count = 10,
                        label = '10d',
                        step = 'day',
                        stepmode = 'backward'),
                    dict(
                        count = 20,
                        label = '20d',
                        step = 'day',
                        stepmode = 'backward'),  
                    dict(
                        count = 1,
                        label = '1m',
                        step = 'month',
                        stepmode = 'backward'),
                    dict(
                        count = 3,
                        label = '3m',
                        step = 'month',
                        stepmode = 'backward'),
                    dict(
                        count = 6,
                        label = '6m',
                        step = 'month',
                        stepmode = 'backward'),
                    dict(
                        count = 1,
                        label = 'YTD',
                        step = 'year',
                        stepmode = 'todate'),
                    dict(
                        count = 1,
                        label = '1y',
                        step = 'year',
                        stepmode = 'backward'),
                    dict(
                        count = 2,
                        label = '2y',
                        step = 'year',
                        stepmode = 'backward'),
                    dict(
                        count = 3,
                        label = '3y',
                        step = 'year',
                        stepmode = 'backward'),
                    dict(
                        count = 5,
                        label = '5y',
                        step = 'year',
                        stepmode = 'backward'),
                    dict(
                        count = 10,
                        label = '10y',
                        step = 'year',
                        stepmode = 'backward'),
                    dict(
                        count = 15,
                        label = '15y',
                        step = 'year',
                        stepmode = 'backward'),
                    dict(
                        count = 20,
                        label = '20y',
                        step = 'year',
                        stepmode = 'backward'),
                    dict(
                        count = 30,
                        label = '30y',
                        step = 'year',
                        stepmode = 'backward'),
                    dict(
                        count = 50,
                        label = '50y',
                        step = 'year',
                        stepmode = 'backward'),
                    dict(
                        step = 'all')
                ])
            ),
            rangeslider = dict(visible = True),
            type = 'date'
        )
    )

    fig.show()



