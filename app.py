import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# Read the processed sales data
df = pd.read_csv("data/formatted_sales_data.csv")

# Rename columns
df = df.rename(columns={
    "Sales": "sales",
    "Date": "date",
    "Region": "region"
})

# Convert data types
df["sales"] = pd.to_numeric(df["sales"])
df["date"] = pd.to_datetime(df["date"])

# Create the Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div(
    className="container",
    children=[

        html.H1(
            "Soul Foods Sales Visualiser",
            className="title"
        ),

        html.P(
            "Select a region to view Pink Morsel sales.",
            className="subtitle"
        ),

        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": " All", "value": "all"},
                {"label": " North", "value": "north"},
                {"label": " East", "value": "east"},
                {"label": " South", "value": "south"},
                {"label": " West", "value": "west"},
            ],
            value="all",
            labelStyle={
                "display": "inline-block",
                "marginRight": "20px"
            },
            className="radio"
        ),

        dcc.Graph(id="sales-chart")

    ]
)

# Callback to update graph
@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):

    # Filter by region
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    # Group sales by date
    daily_sales = (
        filtered_df.groupby("date", as_index=False)["sales"]
        .sum()
        .sort_values("date")
    )

    # Create line chart
    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        title=f"Pink Morsel Sales ({selected_region.title()})",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        template="plotly_white"
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)