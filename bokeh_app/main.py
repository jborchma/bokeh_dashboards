"""Main module that creates the bokeh server app
"""
from os.path import dirname, join

import pandas as pd
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from linetab import LineTab


data = pd.read_csv(join(dirname(__file__), "sales_data_sample.csv"), encoding="ISO-8859-1")
data = data.fillna("NULL")

x_axis = "MONTH_ID"
segments = ["DEALSIZE", "STATE", "COUNTRY"]
metrics = ["SALES", "PRICEEACH", "QUANTITYORDERED"]

# create tab
# here, intialize all tabs of the app
line_tab = LineTab(data, x_axis, segments, metrics).tab

# put all tabs into Tabs
tabs = Tabs(tabs=[line_tab])

# put tabs in the current document
curdoc().add_root(tabs)
