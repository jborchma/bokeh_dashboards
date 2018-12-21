"""Line tab module
"""
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import (ColumnDataSource, HoverTool, Panel)
from bokeh.models.widgets import (CheckboxGroup, Select)

from bokeh.layouts import row, WidgetBox
from bokeh.palettes import Category20_20 # pylint: disable=E0611

from core import InteractiveTab

class LineTab(InteractiveTab): # pylint: disable=R0902
    """Line Tab class

    This is the base class that holds the functions to create, style and update a tab that plots
    a number of metrics, segmented by a number of variables with every possible filter
    automatically generated. It has the following features:

    - All columns that are in the list ``metrics`` will be plotted against the column that is
      specified as the x-axis. A widget will be created in which the metric that is plotted can be
      selected.
    - The plot will be split by any of the segment variables that are contained in the segments
      list. A widget will be created in which the segment that is used to split the data can be
      selected.

    Attributes
    ----------
    data: pd.DataFrame
        Pandas dataframe with the input data.
    segments: [str]
        List with the names of the segment variables
    x_axis: str
        Name of the x-axis variable as a string
    metrics: [str]
        List with the names of the metric variables
    """
    def __init__(self, data, x_axis, segments, metrics):
        # set inputs
        self.data = data
        self.segments = segments
        self.x_axis = x_axis
        self.metrics = metrics

        # initializes the tab
        self.tab = self._initialize_tab()

    def _initialize_tab(self):
        """Create tab structure

        This internal function initializes the dataset, the widgets, the plot and the tab. The
        widgets for the segment and metric selections are created and initialized. The same is
        done with the filters and the variables to filter. Then, based on the initial selections,
        the data source is created and the plot is initialized. Subsequently, the layout is created
        and the tab is set as self.tab.
        """
        # set widgets
        self.segment_select = Select(title="Segments", value=self.segments[0],
                                     options=self.segments)
        self.segment_select.on_change("value", self.update)

        self.metric_select = Select(title="Metrics", value=self.metrics[0],
                                    options=self.metrics)
        self.metric_select.on_change("value", self.update)

        # set filters
        self.segment_filters = {}
        for segment in self.segments:
            available_segments = list(set(self.data[segment]))
            self.segment_filters[segment] = CheckboxGroup(labels=available_segments,
                                                          active=list(
                                                              range(len(available_segments))))
            self.segment_filters[segment].on_change("active", self.update)

        # initialize filters
        initial_segment = self.segment_select.value
        initial_metric = self.metric_select.value
        initial_filters = {}
        for segment in self.segments:
            initial_filters[segment] = [
                self.segment_filters[segment].labels[i]
                for i in self.segment_filters[segment].active
            ]

        self.source = self.make_dataset(initial_segment, initial_metric, initial_filters)
        self.bokeh_plot = self.make_plot(self.source)
        self.bokeh_plot = self.style(self.bokeh_plot)

        self.controls = WidgetBox(self.segment_select, self.metric_select)
        self.filters = WidgetBox(
            *list(self.segment_filters[segment] for segment in self.segment_filters))
        self.layout = row(self.controls, self.bokeh_plot, self.filters)

        return Panel(child=self.layout, title="Segment metrics")

    def make_dataset(self, segment, metric, segments_to_filter):
        """Make Bokeh dataset

        This method creates the dataset that is plotted based on the segment and metric selected.

        Parameters
        ----------
        segment: str
            Column name for the segment variable that is used to segment the data
        metric: str
            Column name for the metric that is plotted
        segments_to_filter: dict
            Dictionary with the column names for the segments as keys and the value for each
            segment variable that are supposed to the plotted as values.

        Returns
        -------
        bokeh.ColumnDataSource
            Data source that underlies the bokeh plot
        """
        data_filtered = self.data.copy()
        for segment_to_filter in segments_to_filter:
            data_filtered = data_filtered.loc[data_filtered[segment_to_filter].isin(
                segments_to_filter[segment_to_filter])]

        segment_values = list(set(data_filtered[segment]))

        dataframes = []
        # iterate through segment values
        for i, segment_value in enumerate(segment_values):
            # subset to the segment value and average by x_axis values
            segment_data = data_filtered[data_filtered[segment] == segment_value]
            segment_average = segment_data[
                [metric, self.x_axis]].groupby(self.x_axis).mean().reset_index()
            segment_average = segment_average.rename(columns={metric: "metric"})
            segment_average["name"] = segment_value
            segment_average["color"] = Category20_20[i]
            dataframes.append(segment_average)

        datasource = pd.concat(dataframes)
        datasource = datasource.sort_values(["name", self.x_axis])
        source = ColumnDataSource(datasource)

        return source

    def make_plot(self, source):
        """Create bokeh plot

        This method creates the bokeh plot object from the data source

        Parameters
        ----------
        source: bokeh.models.ColumnDataSource
            Column data source that underlies the plot.

        Returns
        -------
        bokeh.plotting.figure
            The figure object containing the plot
        """
        bokeh_plot = figure(plot_width=800, plot_height=400, x_axis_label=self.x_axis,
                            y_axis_label="Metric", title="Segment metrics")

        bokeh_plot.circle(self.x_axis, "metric", source=source, alpha=0.4,
                          color="color", size=5, legend="name")

        # hover tool
        hover = HoverTool(tooltips=[("Segment", "@name"),
                                    (self.x_axis, "@" + self.x_axis),
                                    ("Metric", "@metric")])

        bokeh_plot.add_tools(hover)

        return bokeh_plot

    def style(self, bokeh_plot):
        """Style method

        This method applies the stile we want to the bokeh plot.

        Parameters
        ----------
        bokeh_plot: bokeh.plotting.figure
            Bokeh figure to which the styling will be applied.

        Returns
        -------
        bokeh.plotting.figure
            The figure object to which the styling has been applied.
        """
        # title
        bokeh_plot.title.align = "center"
        bokeh_plot.title.text_font_size = "20pt"
        bokeh_plot.title.text_font = "serif"

        # axis labels
        bokeh_plot.xaxis.axis_label_text_font_size = "14pt"
        bokeh_plot.xaxis.axis_label_text_font_style = "bold"
        bokeh_plot.yaxis.axis_label_text_font_size = "14pt"
        bokeh_plot.yaxis.axis_label_text_font_style = "bold"

        # tick labels
        bokeh_plot.xaxis.major_label_text_font_size = "12pt"
        bokeh_plot.yaxis.major_label_text_font_size = "12pt"

        return bokeh_plot

    def update(self, attr, old, new): # pylint: disable=W0613
        """Update datasource

        This method updates the datasource underlying the plot. Its form is governed by
        bokeh and the old dataset can be accessed via ``old`` and the new one via ``new``.
        """
        segment = self.segment_select.value
        metric = self.metric_select.value
        segments_to_filter = {}
        for segment_to_filter in self.segments:
            segments_to_filter[segment_to_filter] = [
                self.segment_filters[segment_to_filter].labels[i]
                for i in self.segment_filters[segment_to_filter].active
            ]

        # get the new dataset
        new_source = self.make_dataset(segment, metric, segments_to_filter)

        self.source.data.update(new_source.data) # pylint: disable=E1101
