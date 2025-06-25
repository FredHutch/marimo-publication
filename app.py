import marimo

__generated_with = "0.14.7"
app = marimo.App(
    width="medium",
    app_title="Publishing Interactive Visualizations",
)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
    # Publishing Interactive Visualizations

    Effectively communicating complex datasets is one of the most rewarding tasks in modern science, but it comes with real challenges.
    When you have reached the limits of what can be done with a static manuscript figure, the next option to explore may be an **interactive visualization**.
    These displays are generally accessed using web browsers, since browsers are already installed on almost every personal computer in the word.
    However, it is often challenging for researchers to publish to the web without either running a server or forgoing interactivity.
    A new exciting development in this field is **marimo**, a Python-based framework for deploying interactive visualizations in an entirely serverless manner.

    The text and figures that you see on this page were generated using **marimo**, with all of the visualizations and interactivity generated within the browser on your computer.
    """
    )
    return


@app.cell
def _():
    # If the script is running in WASM (instead of local development mode), load micropip
    import sys
    if "pyodide" in sys.modules:
        import micropip
    else:
        micropip = None
    return (micropip,)


@app.cell
async def _(micropip, mo):
    # Load the python dependencies needed to read in data and display the 
    with mo.status.spinner("Loading dependencies"):
        import pyarrow
        import pandas as pd
        if micropip is not None:
            micropip.uninstall("narwhals")
            micropip.uninstall("plotly")
            await micropip.install("plotly<6.0.0")
        import plotly.express as px
        import gzip
        import requests
        from io import BytesIO

    return BytesIO, pd, px, requests


@app.cell
def _(mo):
    mo.md(
        """
    ## Loading Data

    Datasets can be read into memory from a public URL, the code repository which contains the manuscript text, or from any other source which can be loaded using a Python library.
    """
    )
    return


@app.cell
def _(BytesIO, micropip, pd, requests):
    def read_feather(data_path) -> pd.DataFrame:
        if micropip is None:
            return pd.read_feather(data_path)
        else:
            response = requests.get(data_path)
            content = response.content
            # if response.headers.get("Content-Encoding") == "gzip":
            #     content = gzip.decompress(content)
            return pd.read_feather(BytesIO(content))
    return (read_feather,)


@app.cell
def _(mo, read_feather):
    # Read in the dataset to display
    with mo.status.spinner("Loading data"):
        df = read_feather("https://fredhutch.github.io/marimo-publication/public/accidents_opendata.feather")
    return (df,)


@app.cell
def _(mo):
    mo.md(
        """
    The dataset that we will use here was obtained from [the Barcelona Traffic Accidents entry in Kaggle](https://www.kaggle.com/datasets/emmanuelfwerr/barcelona-car-accidents) on January 24, 2025 under the [CC0: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/) licence.
    A full description of the source and formatting modifications made to this table can be found in the README.md of [this repository's public/ folder](https://github.com/FredHutch/marimo-publication/tree/main/public).
    """
    )
    return


@app.cell
def _(df):
    df
    return


@app.cell
def _(mo):
    mo.md(r"""## Web Browsers are Inherently Interactive""")
    return


@app.cell
def _(df, pd):
    def bin_df(df: pd.DataFrame, nbins: int):

        return (
            df
            .assign(
                utm_coordinate_x=pd.cut(df["utm_coordinate_x"], nbins).apply(lambda v: v.mid).astype(float),
                utm_coordinate_y=pd.cut(df["utm_coordinate_y"], nbins).apply(lambda v: v.mid).astype(float),
            )
            .groupby(["utm_coordinate_x", "utm_coordinate_y", "district_name"])
            .apply(
                lambda d: pd.Series(dict(n_incidents=d.shape[0], n_vehicles=d["n_vehicles"].sum(), n_victims=d["n_victims"].sum())),
                include_groups=False
            )
            .reset_index()
        )    

    binned_df = bin_df(df, 40)
    return (binned_df,)


@app.cell
def _(binned_df):
    binned_df
    return


@app.cell
def _(binned_df, px):
    # Bin the points to prevent overplotting
    fig = px.scatter(
        binned_df,
        x='utm_coordinate_x',
        y='utm_coordinate_y',
        size='n_vehicles',
        color="district_name",
        template="simple_white",
        labels=dict(
            utm_coordinate_x="UTM Coordinate X",
            utm_coordinate_y="UTM Coordinate Y",
            district_name="District",
            n_vehicles="Number of Vehicles",
            n_victims="Number of Victims",
            n_incidents="Number of Incidents"
        ),
        title="Barcelona Accident Data",
        hover_data=["n_vehicles", "n_incidents", "n_victims"],
        width=800,
        height=600
    )
    fig.update_layout(
        xaxis_showticklabels=False,
        xaxis_showline=False,
        yaxis_showline=False,
        yaxis_showticklabels=False
    )
    fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Compared to a static manuscript, displaying figures in a web browser provides some immediate features that can be useful.
    A basic element of interactivity is moving your cursor over a single point a complex display, or by clicking and dragging a box to zoom into a particular region of the display. 
    For publications using **marimo**, the best options for generating interactive displays are [Plotly](https://plotly.com/python/) and [Altair](https://altair-viz.github.io/), each of which provide an amazing amount of flexibility and power.
    """
    )
    return


@app.cell
def _(df, pd):
    # Make a summary table
    summary = (
        df
        .groupby(
            ["district_name", "year_month"]
        )
        .apply(
            lambda d: pd.Series(dict(
                n_incidents=d.shape[0],
                **d[['n_victims', 'n_vehicles']].sum().to_dict()
            )),
            include_groups=False
        )
        .reset_index()
        .assign(
            year=lambda d: d["year_month"].apply(lambda s: int(s.split("-")[0])),
            month=lambda d: d["year_month"].apply(lambda s: int(s.split("-")[1]))
        )
    )
    return (summary,)


@app.cell
def _(mo):
    mo.md("""## Customizing Plots with User Input""")
    return


@app.cell
def _(px, summary):
    summary_lineplot = px.line(
        summary,
        x='year_month',
        y='n_incidents',
        color="district_name",
        template="simple_white",
        labels=dict(
            utm_coordinate_x="UTM Coordinate X",
            utm_coordinate_y="UTM Coordinate Y",
            district_name="District",
            n_vehicles="Number of Vehicles",
            n_victims="Number of Victims",
            n_incidents="Number of Incidents",
            datetime="Date / Time",
            year_month="Year / Month"
        )
    )
    summary_lineplot
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    While the summary figure above shows a number of patterns in the data (e.g. differences between districts, variability over months within a year, and a sharp dropoff in March 2020), it may be difficult for the reader to isolate those axes of variability in a focused display without loading the source data and rerunning the entire analysis process locally.

    The user input features provided by marimo are extremely open-ended, and can be used to provide the user with the ability to create precisely the plot they want.
    """
    )
    return


@app.cell
def _(df, mo):
    # Collect user input on how to summarize the data and format the plot
    params = (
        mo.md("""### User Input

    - Include Districts: {districts}
    - Include Neighborhoods: {neighborhoods}
    - Group by {group_by}
    - Include Years: {years}
    - X-axis: {x_axis}
    - Y-axis: {y_axis}
    """
             )
        .batch(
            districts=mo.ui.multiselect(options=df['district_name'].unique(), value=df['district_name'].unique()),
            neighborhoods=mo.ui.multiselect(options=df['neighborhood_name'].unique(), value=df['neighborhood_name'].unique()),
            group_by=mo.ui.dropdown(options=["Districts", "Neighborhoods"], value="Districts"),
            years=mo.ui.multiselect(options=df['year'].apply(str).unique(), value=df['year'].apply(str).unique()),
            months=mo.ui.multiselect(options=df['month'].apply(str).unique(), value=df['month'].apply(str).unique()),
            x_axis=mo.ui.dropdown(options=["Month", "Year"], value="Month"),
            y_axis=mo.ui.dropdown(options=["Incidents", "Vehicles"], value="Incidents")
        )
    )
    params
    return (params,)


@app.cell
def _(df, params, pd):
    # Subset the summary data based on the user input
    group_by_kw = params.value["group_by"].lower()[:-1] + "_name"
    time_unit = "year_month" if params.value["x_axis"] == "Month" else "year"
    subset_summary = (
        df
        .loc[
            (
                df.apply(
                    lambda r: (
                        r["district_name"] in params.value["districts"]
                        and
                        r["neighborhood_name"] in params.value["neighborhoods"]
                        and
                        str(r['year']) in params.value["years"]
                        and
                        str(r['month']) in params.value["months"]
                    ),
                    axis=1
                )
            )
        ]
        .groupby(
            [group_by_kw, time_unit]
        )
        .apply(
            lambda d: pd.Series(dict(
                n_incidents=d.shape[0],
                **d[['n_victims', 'n_vehicles']].sum().to_dict()
            )),
            include_groups=False
        )
        .reset_index()
    )
    if time_unit == "year_month":
        subset_summary = subset_summary.assign(
            year=lambda d: d["year_month"].apply(lambda s: int(s.split("-")[0])),
            month=lambda d: d["year_month"].apply(lambda s: int(s.split("-")[1]))
        )
    return group_by_kw, subset_summary, time_unit


@app.cell
def _(group_by_kw, params, px, subset_summary, time_unit):
    # Make the display
    y_cname = "n_incidents" if params.value["y_axis"] == "Incidents" else "n_vehicles"
    custom_fig = px.line(
        data_frame=subset_summary,
        x=time_unit,
        y=y_cname,
        color=group_by_kw,
        template="simple_white",
        labels=dict(
            utm_coordinate_x="UTM Coordinate X",
            utm_coordinate_y="UTM Coordinate Y",
            district_name="District",
            neighborhood_name="Neighborhood",
            n_vehicles="Number of Vehicles",
            n_victims="Number of Victims",
            n_incidents="Number of Incidents",
            datetime="Date / Time",
            year_month="Year / Month"
        )
    )
    custom_fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    When the user modifies the inputs, the figure is regenerated from the input data using Python code that runs entirely in the browser.
    The drawback of this approach is that code runs a bit slowly, so this is not the place to put long-running tasks.
    However, the advantage is that there is no limit to the number of users who can open this publication, and there is effectively no cost to host the website.

    ## Using this Approach

    All of the code needed to build this text and visualization into a website can be found in an open source GitHub repository - [FredHutch/marimo-publication](https://github.com/FredHutch/marimo-publication).
    To build something similar, just fork the repository, modify the contents to meet your needs, and then turn on GitHub pages to instantly create a website publishing your findings.
    More details can be found in the [Readme](https://github.com/FredHutch/marimo-publication).
    """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
