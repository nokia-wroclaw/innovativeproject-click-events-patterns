
# coding: utf-8

# In[117]:


import pandas
import numpy as np
import math
import functools
import bokeh
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.io import output_notebook
from collections import Counter
output_notebook()




PLOT_WIDTH=900
PLOT_HEIGHT=750

    

def plot(series, title="",y_axis_label="ilość"):
    p = figure(title=title, x_axis_label=series.index.name, y_axis_label='ilość', x_range=series.index.values, plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT)
    p.xaxis.major_label_orientation = math.pi/5
    p.vbar(series.index.values, line_width=2,top=series.values,width=0.9)
    p.xaxis.major_label_text_font_size = "9pt"
    return p





def plotUniquePerMonth(data, columnName):
    amountPerMonth = data.groupby(data.serverTime.apply(lambda x:x[0:7]))[columnName].nunique()
    p = figure(title="ilość "+columnName+" w kolejnych miesiącach", x_axis_label='miesiąc', y_axis_label='ilość w miesiącu', x_range=amountPerMonth.index.values, plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT)
    p.xaxis.major_label_orientation = math.pi/5
    p.vbar(amountPerMonth.index.values, line_width=2,top=amountPerMonth.values,width=0.9)
    p.xaxis.major_label_text_font_size = "9pt"
    return p





def plotAmountPerMonth(data):
    amountPerMonth = data.groupby(data.serverTime.apply(lambda x:x[0:7])).apply(lambda x: x.shape[0])
    p = figure(title="ilość na miesiąc", x_axis_label='miesiąc', y_axis_label='ilość w miesiącu', x_range=amountPerMonth.index.values, plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT)
    p.xaxis.major_label_orientation = math.pi/5
    p.vbar(amountPerMonth.index.values, line_width=2,top=amountPerMonth.values,width=0.9)
    p.xaxis.major_label_text_font_size = "9pt"
    return p





def plotUniquePerMonthPercent(data, data2, columnName):
    amountPerMonth = data2.groupby(data.serverTime.apply(lambda x:x[0:7]))[columnName].nunique()/data.groupby(data.serverTime.apply(lambda x:x[0:7]))[columnName].nunique()
    p = figure(title="jaka część różnych "+columnName+" wystąpiła w poszczególnych miesiącach", x_axis_label='miesiąc', y_axis_label='ilość w miesiącu', x_range=amountPerMonth.index.values, plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT)
    p.xaxis.major_label_orientation = math.pi/5
    p.vbar(amountPerMonth.index.values, line_width=2,top=amountPerMonth.values,width=0.9)
    p.xaxis.major_label_text_font_size = "9pt"
    return p





def plotAmountPerMonthPercent(data, data2):
    amountPerMonth = data2.groupby(data.serverTime.apply(lambda x:x[0:7])).apply(lambda x: x.shape[0]) /data.groupby(data.serverTime.apply(lambda x:x[0:7])).apply(lambda x: x.shape[0])
    p = figure(title="procent w danym miesiącu", x_axis_label='miesiąc', y_axis_label='ilość w miesiącu', x_range=amountPerMonth.index.values, plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT)
    p.xaxis.major_label_orientation = math.pi/5
    p.vbar(amountPerMonth.index.values, line_width=2,top=amountPerMonth.values,width=0.9)
    p.xaxis.major_label_text_font_size = "9pt"
    return p

#    g = data.groupby([col2, col1]).size()
def squaredGraph(doubleGroupBy):
    xAxis = []
    yAxis = []
    fields = []

    g1=doubleGroupBy.unstack()
    g1=g1.fillna(0.0)
    for x in g1:
        for y_name, y in g1[x].iteritems():
            yAxis.append(x)
            fields.append(y)
            xAxis.append(y_name)
    colors = []
    maximum = max(fields)
    for c in fields:
        colors.append(bokeh.colors.RGB(255,(1-math.sqrt(c/maximum))*255,255))
    desc = list(map(lambda x:str(x),fields))
    source = ColumnDataSource(data=dict(
        y = yAxis, 
        x= xAxis,
        color=colors,
        desc = desc
    ))
    hover = HoverTool(tooltips=[
        ("department", "@y"),
        ("tool", "@x"),
        ("numbers", "@desc")
    ])
    hm = figure(title="Action count", tools=[hover,  'wheel_zoom', 'box_zoom', 'pan', 'reset'],
                y_range=list(doubleGroupBy.index.levels[1]), x_range=list(doubleGroupBy.index.levels[0]),  plot_width=600, plot_height=600)

    hm.rect(     y = 'y', x = 'x', source = source, color="color", width=1, height=1)
    hm.xaxis.major_label_orientation = math.pi/3

    return hm 

