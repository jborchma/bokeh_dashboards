# Interactive Bokeh dashboard

This repository holds an explanation and a blueprint for how to create interactive dashboards
with bokeh and bokeh server. Bokeh is a powerful visualization package for Python which let's the
user create interactive plots, tabs and whole applications.

However, it takes a little while to learn how bokeh interacts with the data that is supposed to
be plotted, how widgets and tooltips are implemented and how one can set up multiple plots that
depend on the same data source.

## Interactive Tab

The main content of this repo is the abstract base class called `InteractiveTab` in `core.py`
as well as a specific implementation `LineTab` in `linetab.py`. The former establishes the
basic framework that is needed to create an interactive tab with bokeh and the latter is an
example of how one can plot a dataset by some x-axis value and segment/filter by all available
segments. It addresses a use case that I have faced many times at work as well as in personal
projects when one is faced with a new dataset and wants to go through many different plots and
segmentations in order to gain intuition about the data. This is just one example how one can use
interactive dashboards to automatically generate a large number of possible plots without too
much effort.

## Bokeh ColumnDataSource class

Even though one can pass data from a list or a pandas dataframe directly into the bokeh plotting
functions, bokeh has its own data format that interacts well with the general functionality
of widgets, plots and and collection of plots. It can be created from dataframes, lists,
dictionaries and once instantiated it builds the foundational data layer for a plot or even
multiple plots.

This is important because our bokeh app will work in exactly this way: we will load our data
into a ColumnDataSource and then base the plot on it. When we interact with the app and change
a selection through a widget, we actually just update the ColumnDataSource underlying our tab,
which will then update the plot.

## Bokeh server

Bokeh server

## How to run the app

I have implemented an example bokeh app that can be run by executing

```bash
bokeh serve --show bokeh_app/
```

This executes the code that is in `main.py` and should start up the dashboard in a new browser tab.
