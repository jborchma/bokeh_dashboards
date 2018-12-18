"""Module for Bokeh Tab base class
"""
from abc import ABC, abstractmethod

class InteractiveTab(ABC):
    """Abstract base class

    This class is just a shell that implements abstract methods that are needed for the
    basic functionality. The general way it works, is the following:

    - The bokeh plot is created based on a ColumnDataSource. We can create Widgets that change
      for example the column that is plotted, the x-axis, the segmentation variable or some
      filter.
    - When a selection in a widget is changed, the update method is called which will recreate
      the ColumnDataSource based on the new selection and the display the new plot in the tab.
    - This enables also the display of multiple different plots on one tab that all depend on the
      same ColumnDataSource and get updated simultaneously when the update function is called.
    """
    @abstractmethod
    def _initialize_tab(self):
        """Abstract initialize tab method
        """
        pass

    @abstractmethod
    def make_dataset(self):
        """Abstract make dataset method
        """
        pass

    @abstractmethod
    def make_plot(self, source):
        """Abstract plot method
        """
        pass

    @abstractmethod
    def update(self, attr, old, new):
        """Abstract update datasource method
        """
        pass
