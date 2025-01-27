# marimo-publication
Example of publishing serverless interactive visualizations using marimo

## Deployment

To deploy the visualization defined in `app.py` to a public website,
simply set up GitHub Pages for this repository.
Select the option for deploying from Actions.
The Action defined in `.github/workflows/deploy.yaml` will trigger
a build and deployment every time a commit is pushed to this repository.

## Development

### Set up local environment

1. Install Python
2. Install dependencies (`pip install -r requirements.txt`)

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
