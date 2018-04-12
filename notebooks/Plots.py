
# coding: utf-8

# In[117]:


import pandas
import numpy as np
import math
import functools
import bokeh
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
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
    show(p)





def plotUniquePerMonth(data, columnName):
    amountPerMonth = data.groupby(data.serverTime.apply(lambda x:x[0:7]))[columnName].nunique()
    p = figure(title="ilość "+columnName+" w kolejnych miesiącach", x_axis_label='miesiąc', y_axis_label='ilość w miesiącu', x_range=amountPerMonth.index.values, plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT)
    p.xaxis.major_label_orientation = math.pi/5
    p.vbar(amountPerMonth.index.values, line_width=2,top=amountPerMonth.values,width=0.9)
    p.xaxis.major_label_text_font_size = "9pt"
    show(p)





def plotAmountPerMonth(data):
    amountPerMonth = data.groupby(data.serverTime.apply(lambda x:x[0:7])).apply(lambda x: x.shape[0])
    p = figure(title="ilość na miesiąc", x_axis_label='miesiąc', y_axis_label='ilość w miesiącu', x_range=amountPerMonth.index.values, plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT)
    p.xaxis.major_label_orientation = math.pi/5
    p.vbar(amountPerMonth.index.values, line_width=2,top=amountPerMonth.values,width=0.9)
    p.xaxis.major_label_text_font_size = "9pt"
    show(p)





def plotUniquePerMonthPercent(data, data2, columnName):
    amountPerMonth = data2.groupby(data.serverTime.apply(lambda x:x[0:7]))[columnName].nunique()/data.groupby(data.serverTime.apply(lambda x:x[0:7]))[columnName].nunique()
    p = figure(title="jaka część różnych "+columnName+" wystąpiła w poszczególnych miesiącach", x_axis_label='miesiąc', y_axis_label='ilość w miesiącu', x_range=amountPerMonth.index.values, plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT)
    p.xaxis.major_label_orientation = math.pi/5
    p.vbar(amountPerMonth.index.values, line_width=2,top=amountPerMonth.values,width=0.9)
    p.xaxis.major_label_text_font_size = "9pt"
    show(p)





def plotAmountPerMonthPercent(data, data2):
    amountPerMonth = data2.groupby(data.serverTime.apply(lambda x:x[0:7])).apply(lambda x: x.shape[0]) /data.groupby(data.serverTime.apply(lambda x:x[0:7])).apply(lambda x: x.shape[0])
    p = figure(title="procent w danym miesiącu", x_axis_label='miesiąc', y_axis_label='ilość w miesiącu', x_range=amountPerMonth.index.values, plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT)
    p.xaxis.major_label_orientation = math.pi/5
    p.vbar(amountPerMonth.index.values, line_width=2,top=amountPerMonth.values,width=0.9)
    p.xaxis.major_label_text_font_size = "9pt"
    show(p)



