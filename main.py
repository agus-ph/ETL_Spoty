import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from get_data import final_df
from dash.dependencies import Input, Output, State

# -------------------------- Create Dash App ----------------------------------

app = dash.Dash(__name__)

df = final_df


# ----------------------------- App layout -------------------------------------

app.layout = html.Div(
    [
        html.Div([dcc.Graph(id="our_graph")], className="nine columns"),
        html.Div(
            [
                html.Br(),
                html.Label(
                    ["Choose Cryptos to Compare:"],
                    style={"font-weight": "bold", "text-align": "center"},
                ),
                dcc.Dropdown(
                    id="crypto_one",
                    options=[
                        {"label": x, "value": x}
                        for x in df.sort_values("name")["name"].unique()
                    ],
                    value="bitcoin",
                    multi=False,
                    disabled=False,
                    clearable=True,
                    searchable=False,
                    placeholder="Choose Crypto...",
                    className="form-dropdown",
                    style={"width": "90%"},
                    persistence=True,
                    persistence_type="session",
                ),
                dcc.Dropdown(
                    id="crypto_two",
                    options=[
                        {"label": x, "value": x}
                        for x in df.sort_values("name")["name"].unique()
                    ],
                    value="ethereum",
                    multi=False,
                    clearable=False,
                    persistence=True,
                    persistence_type="session",
                ),
                dcc.Dropdown(
                    id="crypto_three",
                    options=[
                        {"label": x, "value": x}
                        for x in df.sort_values("name")["name"].unique()
                    ],
                    value="litecoin",
                    multi=False,
                    clearable=False,
                    persistence=True,
                    persistence_type="session",
                ),
            ],
            className="three columns",
        ),
    ]
)

# ---------------------------------------------------------------


@app.callback(
    Output("our_graph", "figure"),
    [
        Input("crypto_one", "value"),
        Input("crypto_two", "value"),
        Input("crypto_three", "value"),
    ],
)
def build_graph(first_crypto, second_crypto, third_crypto):
    dff = df[
        (df["name"] == first_crypto)
        | (df["name"] == second_crypto)
        | (df["name"] == third_crypto)
    ]

    fig = px.line(dff, x="date", y="prices", color="name")
    fig.update_layout(
        yaxis={"title": "Price"},
        title={
            "text": "Crypto Price Evolution",
            "font": {"size": 28},
            "x": 0.5,
            "xanchor": "center",
        },
    )
    return fig


# ---------------------------------------------------------------

if __name__ == "__main__":
    app.run_server(debug=True)
