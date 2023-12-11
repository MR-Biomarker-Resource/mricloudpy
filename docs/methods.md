# Methods

## Reading and accessing data

### Data

**All methods except [`generate_3d_image`](methods.md/#generate_3d_image) are methods applied to the `Data` object.**

```python
Data(path, id_type='numeric', id_list=None)
```

**Attributes:**

- **path**: *str*
- **id_type**: *str, {'numeric', 'filename', 'custom'}, default = 'numeric'*
- **id_list**: *list, default = None*
- **df**: *DataFrame*

---

### get_data

Retrieve DataFrame of a given data object.

```python
get_data()
```

**Parameters:**

- **None**

---

### get_id

Retrieve list of unique subject IDs.

```python
get_id()
```

**Parameters:**

- **None**

---

## Manipulating data

### rename_subject

Rename a specific subject ID.

```python
rename_subject(old, new)
```

**Parameters:**

- **old**: *str*
- **new**: *str*

### long_to_wide

Convert default long form data to a wide format.

```python
long_to_wide()
```

**Parameters:**

- **None**

---

## Visualization

### generate_sunburst

Generate a Plotly Express sunburst Figure model.

```python
generate_sunburst(type, id, base_level=5)
```

**Parameters:**

- **type**: *int, {1, 2}*
- **id**: *str*
- **base_level**: *int, {1, 2, 3, 4, 5}, default = 5*

---

### generate_treemap

Generate a Plotly Express treemap Figure model.

```python
generate_treemap(type, id, base_level=5)
```

**Parameters:**

- **type**: *int, {1, 2}*
- **id**: *str*
- **base_level**: *int, {1, 2, 3, 4, 5}, default = 5*

---

### generate_icicle

Generate a Plotly Express icicle Figure model.

```python
generate_icicle(type, id, base_level=5)
```

**Parameters:**

- **type**: *int, {1, 2}*
- **id**: *str*
- **base_level**: *int, {1, 2, 3, 4, 5}, default = 5*

---

### generate_bar

Generates a Plotly Express bar graph Figure.

```python
generate_bar(type, level, id, x='ID', y='Prop', log_y=False)
```

**Parameters:**

- **type**: *int, {1, 2}*
- **level**: *int, {1, 2, 3, 4, 5}*
- **id**: *list, default = None*
- **x**: *str, {'ID', 'Object'}, default = 'ID'*
- **y**: *str, {'Prop', 'Volume'}, default = 'Prop'*
- **log_y**: *bool, default = False*

---

### generate_mean_diff

Generate a Plotly Express mean difference plot Figure.

```python
generate_mean_diff(type, level, color='ID', id=None)
```

**Parameters:**

- **type**: *int, {1, 2}*
- **level**: *int*, {1, 2, 3, 4, 5}
- **color**: *str, {'ID', 'Object'}, default = 'ID'*
- **id**: *list, default = None*

---

### generate_corr_matrix

Generate a Plotly Express heatmap Figure of a correlation matrix.

```python
generate_corr_matrix(type, level, id=None)
```

**Parameters:**

- **type**: *int, {1, 2}*
- **level**: *int*, {1, 2, 3, 4, 5}
- **id**: *list, default = None*

---

## Modeling and covariate analysis

### append_covariate_data

Append covariate dataset to data object.

```python
append_covariate_data(file, icv=False, tbv=False)
```

**Parameters:**

- **file**: *str*
- **icv**: *bool, default = False*
- **tbv**: *bool, default = False*

---

### normalize_covariate_data

Normalize region data in covariate dataset by ICV, TBV, or ICV + TBV.

```python
normalize_covariate_data(covariate_dataset, normalizing_factor)
```

**Parameters:**

- **covariate_dataset**: *DataFrame*
- **normalizing_factor**: *str, {'icv, tbv, icv_tbv'}*

---

### OLS

Run statsmodels Ordinary Least Squares regression on data object.

```python
OLS(covariate_dataset, covariates, outcome, log=False, residual_plot=False)
```

**Parameters:**

- **covariate_dataset**: *DataFrame*
- **covariates**: *list*
- **outcome**: *str*
- **log**: *bool, default = False*
- **residual_plot**: *bool, default = False*

---

### Logit

Run statsmodels Logit regression on data object.

```python
Logit(covariate_dataset, covariates, outcome, log=False, roc_plot=False)
```

**Parameters:**

- **covariate_dataset**: *DataFrame*
- **covariates**: *list*
- **outcome**: *str*
- **log**: *bool, default = False*
- **roc_plot**: *bool, default = False*

---

## Imaging

Generates a subplot or single image (if 'nrows' and 'ncols' is 1) of region-specific brain images on a template brain

### generate_3d_image

```python
generate_3d_image(img_path, regions, view, nrows, ncols, slice_n=0)
```

**Parameters:**

- **img_path**: *str*
- **regions**: *list*
- **view**: *int, {0 (horizontal), 1 (sagittal), 2 (coronal)}*
- **nrows**: *int, {1, 2, 3, 4, 5, 6, 7}*
- **ncols**: *int, {1, 2, 3, 4, 5, 6, 7}*
- **slice_n**: *int, default = 0*
