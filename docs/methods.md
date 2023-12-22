# Methods

## Reading and accessing data

### Data

**All methods except [`generate_3d_image`](methods.md/#generate_3d_image) are methods applied to the `Data` object.**

```python
Data(path, id_type='numeric', id_list=None)
```

**Attributes:**

- **`path`**: *str*
    - Path to MRICloud data text file
- **`id_type`**: *str, {'numeric', 'filename', 'custom'}, default = 'numeric'*
    - Type of subject ID formatting
- **`id_list`**: *list, default = None*
    - List of custom subject IDs
- **`df`**: *DataFrame*
    - DataFrame generated from path

---

### get_data

Retrieve DataFrame of a given data object.

```python
get_data()
```

**Parameters:**

- **None**

**Returns:**
[**`DataFrame`**](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)

---

### get_id

Retrieve list of unique subject IDs.

```python
get_id()
```

**Parameters:**

- **None**

**Returns:**
[**`Series`**](https://pandas.pydata.org/docs/reference/api/pandas.Series.html)

---

## Manipulating data

### rename_subject

Rename a specific subject ID.

```python
rename_subject(old, new)
```

**Parameters:**

- **`old`**: *str*
    - Old subject name to be replaced
- **`new`**: *str*
    - New subject name

**Returns:**
[**`DataFrame`**](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)

### long_to_wide

Convert default long form data to a wide format.

```python
long_to_wide()
```

**Parameters:**

- **None**

**Returns:**
[**`DataFrame`**](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)

---

## Visualization

### generate_sunburst

Generate a Plotly Express sunburst Figure model.

```python
generate_sunburst(type, id, base_level=5)
```

**Parameters:**

- **`type`**: *int, {1, 2}*
    - Type of hierarchical view
- **`id`**: *str*
    - Subject ID
- **`base_level`**: *int, {1, 2, 3, 4, 5}, default = 5*
    - Lowest hierarchical level to include

**Returns:**
[**`Figure`**](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html)

---

### generate_treemap

Generate a Plotly Express treemap Figure model.

```python
generate_treemap(type, id, base_level=5)
```

**Parameters:**

- **`type`**: *int, {1, 2}*
    - Type of hierarchical view
- **`id`**: *str*
    - Subject ID
- **`base_level`**: *int, {1, 2, 3, 4, 5}, default = 5*
    - Lowest hierarchical level to include

**Returns:**
[**`Figure`**](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html)

---

### generate_icicle

Generate a Plotly Express icicle Figure model.

```python
generate_icicle(type, id, base_level=5)
```

**Parameters:**

- **`type`**: *int, {1, 2}*
    - Type of hierarchical view
- **`id`**: *str*
    - Subject ID
- **`base_level`**: *int, {1, 2, 3, 4, 5}, default = 5*
    - Lowest hierarchical level to include


**Returns:**
[**`Figure`**](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html)

---

### generate_bar

Generates a Plotly Express bar graph Figure.

```python
generate_bar(type, level, id, x='ID', y='Prop', log_y=False)
```

**Parameters:**

- **`type`**: *int, {1, 2}*
    - Type of hierarchical view
- **`level`**: *int, {1, 2, 3, 4, 5}*
    - Hierarchical level of interest
- **`id`**: *list, default = None*
    - Subjects of interest
- **`x`**: *str, {'ID', 'Object'}, default = 'ID'*
    - Independent variable
- **`y`**: *str, {'Prop', 'Volume'}, default = 'Prop'*
    - Dependent variable
- **`log_y`**: *bool, default = False*
    - Logarithm of dependent variable

**Returns:**
[**`Figure`**](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html)

---

### generate_mean_diff

Generate a Plotly Express mean difference plot Figure.

```python
generate_mean_diff(type, level, color='ID', id=None)
```

**Parameters:**

- **`type`**: *int, {1, 2}*
    - Type of hierarchical view
- **`level`**: *int*, {1, 2, 3, 4, 5}
    - Hierarchical level of interest
- **`color`**: *str, {'ID', 'Object'}, default = 'ID'*
    - Variable to organize data by color
- **`id`**: *list, default = None*
    - Subjects of interest

**Returns:**
[**`Figure`**](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html)

---

### generate_corr_matrix

Generate a Plotly Express heatmap Figure of a correlation matrix.

```python
generate_corr_matrix(type, level, id=None)
```

**Parameters:**

- **`type`**: *int, {1, 2}*
    - Type of hierarchical view
- **`level`**: *int*, {1, 2, 3, 4, 5}
    - Hierarchical level of interest
- **`id`**: *list, default = None*
    - Subjects of interest

**Returns:**
[**`Figure`**](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html)

---

## Modeling and covariate analysis

### append_covariate_data

Append covariate dataset to data object.

```python
append_covariate_data(path, icv=False, tbv=False)
```

**Parameters:**

- **`path`**: *str*
    - Path to covariate dataset file
- **`icv`**: *bool, default = False*
    - Append intracranial volume to covariate dataset
- **`tbv`**: *bool, default = False*
    - Append total brain volume to covariate dataset

**Returns:**
[**`DataFrame`**](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)

---

### normalize_covariate_data

Normalize region data in covariate dataset by ICV, TBV, or ICV + TBV.

```python
normalize_covariate_data(covariate_dataset, normalizing_factor)
```

**Parameters:**

- **`covariate_dataset`**: *DataFrame*
    - Covariate dataset to be normalized
- **`normalizing_factor`**: *str, {'icv, tbv, icv_tbv'}*
    - Variable to normalize region volumes by

**Returns:**
[**`DataFrame`**](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)

---

### OLS

Run statsmodels Ordinary Least Squares regression on data object.

```python
OLS(covariate_dataset, covariates, outcome, log=False, residual_plot=False)
```

**Parameters:**

- **`covariate_dataset`**: *DataFrame*
    - Dataset containing the covariates and outcome
- **`covariates`**: *list*
    - Covariates to include in analysis (x, independent covariates)
- **`outcome`**: *str*
    - Outcome of interest (y, dependent covariate)
- **`log`**: *bool, default = False*
    - Logaritm of covariates
- **`residual_plot`**: *bool, default = False*
    - Return a residual plot of analysis results as Plotly Figure

**Returns:**
[**`RegressionResultsWrapper.summary()`**](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.html),
[**`Figure`**](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html)

---

### Logit

Run statsmodels Logit regression on data object.

```python
Logit(covariate_dataset, covariates, outcome, log=False, roc_plot=False)
```

**Parameters:**

- **`covariate_dataset`**: *DataFrame*
    - Dataset containing the covariates and outcome
- **`covariates`**: *list*
    - Covariates to include in analysis (x, independent covariates)
- **`outcome`**: *str*
    - Outcome of interest (y, dependent covariate)
- **`log`**: *bool, default = False*
    - Logaritm of covariates
- **`roc_plot`**: *bool, default = False*
    - Return a residual plot of analysis results as Plotly Figure

**Returns:**
[**`RegressionResultsWrapper.summary()`**](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.html),
[**`Figure`**](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html)

---

## Imaging

Generates a subplot or single image (if 'nrows' and 'ncols' is 1) of region-specific brain images on a template brain

### generate_3d_image

```python
generate_3d_image(img_path, regions, view, nrows, ncols, slice_n=0)
```

**Parameters:**

- **`img_path`**: *str*
- **`regions`**: *list*
- **`view`**: *int, {0 (horizontal), 1 (sagittal), 2 (coronal)}*
- **`nrows`**: *int, {1, 2, 3, 4, 5, 6, 7}*
- **`ncols`**: *int, {1, 2, 3, 4, 5, 6, 7}*
- **`slice_n`**: *int, default = 0*
