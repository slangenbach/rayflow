# Rayflow

A whirlwind tour of [Ray][3] and [MLflow Recipes][1] using the [NYC taxi dataset][4].

## Prerequisites

* Python 3.10+
* [poetry][5]
* Kaggle account (including credentials for [Kaggle CLI][6])

## Installation

Install dependencies

    poetry install

Create directories to store data

    CTRL+P -> Tasks: Run task -> Create directories

Download data

    CTRL+P -> Tasks: Run task -> Download data

Note: You can also download individual files using the _Download file from dataset_ task

Unzip data

    CTRL+P -> Tasks: Run task -> Unzip all zip archives

Optional: Remove archives

    CTRL+P -> Tasks: Run task -> Remove all zip archives

## Usage

Open the _prototype_ notebook and run all cells

    code notebooks/prototype.ipynb

## Contributing

Install dependencies

    poetry install

Install pre-commit hooks

    poetry run pre-commit install

Create a dedicated branch and start contributing

    git checkout -b your-branch-name

# Resources

* [MLflow Recipe documentation][1]
* [MLflow Recipes regression template][2]
* [Ray documentation][3]
* [NYC Taxi Trip Records Dataset][4]


[1]: https://mlflow.org/docs/latest/recipes.html
[2]: https://github.com/mlflow/recipes-regression-template
[3]: https://docs.ray.io/en/latest/
[4]: https://www.kaggle.com/datasets/microize/nyc-taxi-dataset
[5]: https://python-poetry.org/
[6]: https://github.com/Kaggle/kaggle-api/blob/main/docs/README.md
