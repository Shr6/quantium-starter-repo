import os
import sys

# Add the project root to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


def test_header_present(dash_duo):
    dash_duo.start_server(app)

    header = dash_duo.find_element("h1")

    assert header.text == "Soul Foods Sales Visualiser"


def test_graph_present(dash_duo):
    dash_duo.start_server(app)

    graph = dash_duo.find_element("#sales-chart")

    assert graph is not None


def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)

    radio = dash_duo.find_element("#region-filter")

    assert radio is not None