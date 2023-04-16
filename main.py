import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from get_data import final_df
from dash.dependencies import Input, Output, State

# -------------------------- Create Dash App ----------------------------------

app = dash.Dash(__name__)
server = app.server

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
                    value="litecoin",
                    multi=False,
                    disabled=False,
                    clearable=True,
                    searchable=False,
                    placeholder="Choose First Crypto...",
                    className="form-dropdown",
                    style={"width": "95%"},
                    persistence=True,
                    persistence_type="session",
                ),
                dcc.Dropdown(
                    id="crypto_two",
                    options=[
                        {"label": x, "value": x}
                        for x in df.sort_values("name")["name"].unique()
                    ],
                    value="monero",
                    multi=False,
                    disabled=False,
                    clearable=True,
                    searchable=False,
                    placeholder="Choose Second Crypto...",
                    className="form-dropdown",
                    style={"width": "95%"},
                    persistence=True,
                    persistence_type="session",
                ),
                dcc.Dropdown(
                    id="crypto_three",
                    options=[
                        {"label": x, "value": x}
                        for x in df.sort_values("name")["name"].unique()
                    ],
                    value="bitcoin-cash",
                    multi=False,
                    disabled=False,
                    clearable=True,
                    searchable=False,
                    placeholder="Choose Third Crypto...",
                    className="form-dropdown",
                    style={"width": "95%"},
                    persistence=True,
                    persistence_type="session",
                ),
            ],
            className="three columns",
        ),
        html.Div([dcc.Graph(id="our_graph2")], className="nine columns"),
        html.Div([dcc.Graph(id="our_graph3")], className="nine columns"),
    ],

)

# ------------------------ Call Backs --------------------------

# --------------- Price evolution call back --------------------
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
            "font": {"size": 22},
            "x": 0.5,
            "xanchor": "center",
        },
    )
    return fig

# --------------- Market caps call back --------------------

@app.callback(
    Output("our_graph2", "figure"),
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

    fig2 = px.line(dff, x="date", y="market_caps", color="name")
    fig2.update_layout(
        yaxis={"title": "Market Caps"},
        title={
            "text": "Market Caps Evolution",
            "font": {"size": 22},
            "x": 0.5,
            "xanchor": "center",
        },
    )
    return fig2

# ----------------- Volume call back -----------------------

@app.callback(
    Output("our_graph3", "figure"),
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

    fig3 = px.line(dff, x="date", y="total_volumes", color="name")
    fig3.update_layout(
        yaxis={"title": "Total Volumes"},
        title={
            "text": "Total Volumes Evolution",
            "font": {"size": 22},
            "x": 0.5,
            "xanchor": "center",
        },
    )
    return fig3

# ---------------------------------------------------------------

if __name__ == "__main__":
    app.run_server(debug=True)

