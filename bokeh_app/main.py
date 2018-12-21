"""Main module that creates the bokeh server app
"""
from os.path import dirname, join

import pandas as pd
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from linetab import LineTab


data = pd.read_excel(join(dirname(__file__), "superstore.xls"))
data = data.fillna("NULL")
data['year'] = data['Order Date'].dt.year.astype(str)
data['month'] = pd.DatetimeIndex(data['Order Date']).month

x_axis = 'month'
segments = ["year", "Category", "Sub-Category", "Region"]
metrics = ["Sales", "Quantity", "Profit"]

# create tab
# here, intialize all tabs of the app
line_tab = LineTab(data, x_axis, segments, metrics).tab

# put all tabs into Tabs
tabs = Tabs(tabs=[line_tab])

# put tabs in the current document
curdoc().add_root(tabs)
