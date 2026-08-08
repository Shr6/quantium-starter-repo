import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Load the processed sales data
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

# Sum sales for each date
daily_sales = (
    df.groupby("date", as_index=False)["sales"]
      .sum()
      .sort_values("date")
)

# Create line chart (SVG rendering avoids WebGL issues)
fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    render_mode="svg"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales ($)",
    template="plotly_white"
)

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1(
        "Soul Foods Sales Visualiser",
        style={"textAlign": "center"}
    ),
    dcc.Graph(
        figure=fig,
        config={"displayModeBar": False}
    )
])

if __name__ == "__main__":
    app.run(debug=True)