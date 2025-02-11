# marimo-publication
Example of publishing serverless interactive visualizations using marimo

Open this example publication at [https://fredhutch.github.io/marimo-publication/](https://fredhutch.github.io/marimo-publication/)

[![Example Marimo Publication](https://github.com/fredhutch/marimo-publication/raw/main/public/screenshot.gif)](https://fredhutch.github.io/marimo-publication/)

Goal:

- Publish an interactive visualization as a standalone website

Approach:

- Using the open source [marimo](https://marimo.io/) Python library,
- Enter figures and text using a familar notebook interface,
- Test locally to quickly author a manuscript or report,
- Deploy to a static webpage, where all code is run directly in the reader's browser.

Benefits:

- No need to run costly webservers
- Use the rich Python ecosystem for data science and visualization
- Publications are 100% reproducible, with all code available to the reader

Drawbacks:

- Not appropriate for long-running or costly computational tasks
- Upper limit of ~2GB for in-browser tasks

## Deployment

To deploy the visualization defined in `app.py` to a public website,
simply set up GitHub Pages for this repository.
Select the option for deploying from Actions.
The Action defined in `.github/workflows/deploy.yaml` will trigger
a build and deployment every time a commit is pushed to this repository.
After you enable Actions, you will need to push a commit to trigger the
Action for the first time.

## Development

### Set up local environment

1. Install Python
2. Install dependencies (`pip install -r requirements.txt`) (ideally within a virtual environment)

### Edit visualization

Using the local environment, the visualization in `app.py` can be edited
interactively before publishing to the web.

```
marimo edit app.py
```

### Adding data

Files added to the `public/` folder will be included in the deployment.
Following the [marimo documentation](https://docs.marimo.io/guides/wasm/#including-data),
using the pattern `path_to_csv = mo.notebook_location() / "public" / "data.csv"`
will ensure that the data is sources from the appropriate location during
local development as well as the deployed website.

### Testing deployment

To run a local test of the conversion to HTML-WASM:

```
rm -rf test_build
marimo export html-wasm app.py -o test_build --mode run
python -m http.server --directory test_build
```

And then open `localhost:8000` in your browser.
