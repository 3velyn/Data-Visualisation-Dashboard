from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    from datetime import datetime as dt
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = dt(2015, 11, 1)
    end = dt(2016, 3, 1)
    df = data.DataReader(name='GOOG', data_source='yahoo', start=start, end=end)

    def inc_dec(close, open):
        if close > open:
            value = 'Increase'
        elif close < open:
            value = 'Decrease'
        else:
            value = 'Equal'
        return value

    def rect_build(plot, status, color):
        hours_in_ms = 12*60*60*1000
        plot.rect(df.index[df.Status == status], df.Average[df.Status == status], hours_in_ms, 
            df.Height[df.Status == status], fill_color=color, line_color='black', legend_label=status)

    df['Status'] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
    df['Average'] = (df.Open + df.Close)/2
    df['Height'] = abs(df.Open - df.Close)

    plot = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode='scale_width')
    plot.title.text = 'Candlestick Chart'
    plot.grid.grid_line_alpha = 0.3
    plot.segment(df.index, df.High, df.index, df.Low, color='Black')

    rect_build(plot, 'Increase', '#7B9B74')
    rect_build(plot, 'Decrease', '#FF6C00')
    rect_build(plot, 'Equal', '#C4C7CC')

    # output_file('CS.html')
    # show(plot)

    script1, div1 = components(plot)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files

if __name__ == '__main__':
    app.run(debug=True)