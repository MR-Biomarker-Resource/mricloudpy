# mricloudpy

![Static Badge](https://img.shields.io/badge/version-0.0.1-blue)
![GitHub repo size](https://img.shields.io/github/repo-size/MR-Biomarker-Resource/mricloudpy?logo=Github&color=orange)

`mricloudpy` is a Python library for handling MRICloud output data.

## Description

`mricloudpy` is a library designed to streamline the data processing, analysis, and visualization of subject-specific hierarchical volumetric MRICloud data. This free and open-source library provides a suite of tools to create and manage dataset objects, including a web app GUI.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `mricloudpy`.

```bash
pip install mricloudpy
```

Alternatively, clone [this](https://mr-biomarker-resource.github.io/MRICloudPy/) repository and install the package locally.

### Running web app GUI

To use the web app GUI, clone this repository and install `panel` and `jupyter` as well:

```bash
pip install panel jupyter
```

Then start the Bokeh server on your local machine:

```bash
cd ./app
panel serve app.py
```

## Documentation and usage

Documentation for the library can be found [here](https://mr-biomarker-resource.github.io/MRICloudPy/).

## Contributing

To contribute to `mricloudpy`, follow these steps:

### Step 1

Fork [this](https://mr-biomarker-resource.github.io/MRICloudPy/) repository.

### Step 2

Clone the repository to your local machine:

```bash
git clone https://github.com/username/repository.git
```

### Step 3

Create a branch:

```bash
git checkout -b '<branch_name>'
```

### Step 4

Make your changes and commit them to the branch:

```bash
git add .
git commit -m '<commit_message>'
```

### Step 5

Push the branch to the forked repository:

```bash
git push origin '<branch_name>'
```

### Step 6

Create a pull request.
See the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

Please provide clear and detailed information about the changes in your pull request.

Thank you for your interest in contributing to our project!

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Acknowledgements

- Johns Hopkins Bloomberg School of Public Health Department of Biostatistics
- Caffo Lab
