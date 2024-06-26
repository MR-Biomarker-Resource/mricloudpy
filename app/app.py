# %%
import panel as pn
import mricloudpy as mp
from mricloudpy import imaging
from tkinter import Tk, filedialog
import ctypes
import plotly.io as pio
pio.renderers.default = 'browser'

pn.extension('plotly')
pn.config.notifications = True
# pn.extension('tabulator')

# Kermit, Miss Piggy, Fozzie, Gonzo, Rowlf, Scooter, Animal, Pepe, Rizzo, Beaker, Statler, Waldorf, Swedish Chef, Bob, Sally

# %% [markdown]
# ### Sidebar items

# %%
# Data directory select button and path text
dir_select_button = pn.widgets.Button(name='Select data directory', button_type='primary')
dir_select_text = pn.widgets.StaticText(visible=False)

# ID select button, covariate data requirement tip, and list input
id_type_select = pn.widgets.Select(name='ID Type', options={'Numeric': 'numeric',
                                                         'Filename': 'filename',
                                                         'Custom': 'custom'})
id_type_tooltip = pn.widgets.StaticText(value='ID type must be \'Custom\' to add covariate data')
id_list_text = pn.widgets.TextAreaInput(name='ID List', visible=False, 
                                        placeholder='ex: Kermit, Miss Piggy, Fozzie...')

# Data upload button
file_upload_button = pn.widgets.Button(name='Upload data', button_type='primary', visible=False)

# Covariate data directory select and path text
add_covariate_data_button = pn.widgets.Button(name='Add covariate data', visible=False)
add_covariate_data_text = pn.widgets.StaticText(visible=False)

# ICV and TBV checkbox
append_icv_checkbox = pn.widgets.Checkbox(name='Append ICV', visible=False)
append_tbv_checkbox = pn.widgets.Checkbox(name='Append TBV', visible=False)

# Covariate data upload button
upload_covariate_data_button = pn.widgets.Button(name='Upload covariate data', button_type='primary', visible=False)

# Sidebar data preview window
data = pn.widgets.Tabulator(height=500, width=300, page_size=100, pagination='local', disabled=True)
data_note = pn.widgets.StaticText(value='Truncated to 20 columns in preview')

# %% [markdown]
# ### Visualization items

# %%
# Visualization and analysis mode switch button
mode_radio = pn.widgets.Button(name='View analysis tools', button_type='primary',
                               width=200, height=30)

# Visualization option select dropdown
vis_select = pn.widgets.Select(name='Visual', options={'Sunburst':'sunburst', 
                                                       'Treemap': 'treemap',
                                                       'Icicle': 'icicle',
                                                       'Bar': 'bar',
                                                       'Mean Difference': 'mean_diff',
                                                       'Correlation Matrix': 'corr_matrix',
                                                       'Neuroimaging': 'imaging'},
                                                       width=140)
# Data filter (type, base level, ID) select dropdowns for visualization                                                       
type_select = pn.widgets.Select(name='Type', options=['1', '2'], width=50, visible=True)
base_level_select = pn.widgets.Select(name='Base Level', options=['1', '2', '3', '4', '5'], width=50, visible=True)
id_single_select = pn.widgets.Select(name='ID', options=[], width=100, visible=True)
id_multi_text = pn.widgets.TextAreaInput(name='ID List', placeholder='ex: Kermit, Miss Piggy... (or \"all\")',
                                          width=150, visible=False)
# x- and y-axis variable select for 'bar' visualization
x_select = pn.widgets.Select(name='x', options=['ID', 'Object'], width=100, visible=False)
y_select = pn.widgets.Select(name='y', options=['Prop', 'Volume'], width=100, visible=False)

# Log data select dropwdown
log_select = pn.widgets.Select(name='Logarithm', options=['False', 'True'], width=100, visible=False)

# Image (MNI) data directory select button and path text
image_upload_button = pn.widgets.Button(name='Upload image file', button_type='primary', margin=(35, 10, 10, 10), visible=False)
image_select_text = pn.widgets.StaticText(width=100, margin=(30, 10, 10, 10), visible=False)

# Image viewer filter and view options select and input
image_view_select = pn.widgets.Select(name='View', options={'Horizontal': 0, 
                                                       'Sagittal': 1,
                                                       'Coronal': 2},
                                                       width=100, visible=False)
image_size_input = pn.widgets.IntInput(name='Row/Column Size', value=1, step=1, start=1, end=10, width=100, visible=False)
image_size_tooltip = pn.widgets.TooltipIcon(value='Select size \'1\' to view individual slices. ' + 
                                            'Select a size greater than \'2\' to generate a grid of subplots.',
                                            visible=False)
region_selector = pn.widgets.CrossSelector(name='Regions', visible=False)

# Generate visualization button
generate_button = pn.widgets.Button(name='Generate', button_type='primary')

# Visualization and image plot objects
vis_plot = pn.pane.Plotly(sizing_mode="stretch_width", config={'responsive': True}, height=700, visible=False)
image_plot = pn.pane.Plotly(height=800, width=800, visible=False)

# Imaging module navigation arrows and input
image_plot_int_input = pn.widgets.IntInput(start=0, width=100)
image_plot_int_input_button = pn.widgets.Button(name='Jump to Slice', button_type='primary', width=50)
image_plot_left_arrow_single = pn.widgets.Button(icon='chevron-left', button_type='default', width=50)
image_plot_right_arrow_single = pn.widgets.Button(icon='chevron-right', button_type='default', width=50)
image_plot_left_arrow_multiple = pn.widgets.Button(icon='chevrons-left', button_type='default', width=50)
image_plot_right_arrow_multiple = pn.widgets.Button(icon='chevrons-right', button_type='default', width=50)

# %% [markdown]
# ### Analysis items

# %%
# Analysis option select dropdown
analysis_select = pn.widgets.Select(name='Analysis',
                                    options={'Ordinary Least Squares': 'ols',
                                             'Logistic Regression': 'logit',
                                             'Random Forest': 'randomforest'},
                                    width=200)

# Analysis parameter select and configuration menu
outcome_select = pn.widgets.Select(name='Outcome')
normalize_factor_radio = pn.widgets.RadioButtonGroup(name='Normalizing Factor', 
                                                     options={'None': 'none', 
                                                              'ICV': 'icv',
                                                              'TBV': 'tbv',
                                                              'ICV + TBV': 'icv_tbv'})
analysis_type_select = pn.widgets.Select(name='Type', options=['1', '2'], width=50, visible=True)
analysis_level_select = pn.widgets.Select(name='Base Level', options=['1', '2', '3', '4', '5'], width=50, visible=True)
log_covariates_checkbox = pn.widgets.Checkbox(name='Log of covariates')

# Estimators and random state input for random forest
n_estimators_int_input = pn.widgets.IntInput(name='Number of trees', start=200, width=100, visible=False)
random_state_int_input = pn.widgets.IntInput(name='Random state', start=42, width=100, visible=False)

# Residual and ROC plot checkbox for OLS and Logit
residual_plot_checkbox = pn.widgets.Checkbox(name='Generate residual plot')
roc_plot_checkbox = pn.widgets.Checkbox(name='Generate ROC curve', visible=False)

# Binary classifier and importance plot checkbox for random forest
classifier_checkbox = pn.widgets.Checkbox(name='Use binary classification', visible=False)
importance_plot_checkbox = pn.widgets.Checkbox(name='Generate feature importance plot', visible=False)

# Select covariates of interest
covariate_selector = pn.widgets.CrossSelector(name='Covariates')

# Run analysis button
run_button = pn.widgets.Button(name='Run', button_type='primary', width=50)

# Analysis output and plot
analysis_output = pn.pane.Str()
analysis_plot = pn.pane.Plotly(sizing_mode="stretch_width", config={'responsive': True}, height=700, visible=False)

# %% [markdown]
# ### Sidebar events

# %%
# Select data directory
def dir_select(event):
    # Open windows explorer
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = Tk()
    root.withdraw()                                        
    root.call('wm', 'attributes', '.', '-topmost', True) 
    # root.call('tk', 'scaling', 2.0)  
    dir_select.dir = filedialog.askdirectory(mustexist=True)

    # Store selected directory
    dir_select_text.value = dir_select.dir
    dir_select_text.visible = True

    # Check if directory is populated to allow upload
    if dir_select.dir is not None:
        file_upload_button.visible = True

# Check if custom ID type for ID list prompt visibility
def check_custom(event):
    if event.new == 'custom':
        id_list_text.visible = True
    else:
        id_list_text.visible = False

# Format custom and store custom list into Python list
def custom_list_format(event):
    text = event.new
    text = text.replace(', ', ',')
    custom_list_format.text_list = text.split(',')

# Handle data upload event
def upload(event):
    upload.is_uploaded = False
     
    if dir_select.dir is not None:
        # Try to upload with custom list, ignore parameter if missing
        try:
            upload.dataset = mp.Data(path=dir_select.dir, id_type=id_type_select.value, 
                             id_list=custom_list_format.text_list)
            data.value = upload.dataset.get_data()
        except:
            upload.dataset = mp.Data(path=dir_select.dir, id_type=id_type_select.value)
            data.value = upload.dataset.get_data()
        data.visible = True
        # Make covariate data upload visible if 'custom' ID type is selected
        if id_type_select.value == 'custom':
            add_covariate_data_button.visible = True
        # Populate ID list for future selection
        id_single_select.options = data.value['ID'].unique().tolist()
        
        # Upload successful
        upload.is_uploaded = True
        pn.state.notifications.success('Data upload successful.')

def add_covariate_data(event):
    # Open windows explorer
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = Tk()
    root.withdraw()                                        
    root.call('wm', 'attributes', '.', '-topmost', True) 
    # root.call('tk', 'scaling', 2.0)  
    add_covariate_data.file = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv'),
                                                                    ('Text Document', '*.txt')])
    
    # Store selected directory
    add_covariate_data_text.value = add_covariate_data.file
    add_covariate_data_text.visible = True

    # Make covariate upload button and checkboxes available if covariate data directory found
    if add_covariate_data.file is not None:
        upload_covariate_data_button.visible = True
        append_icv_checkbox.visible = True
        append_tbv_checkbox.visible = True

# Handle covariate data upload event
def upload_covariate_data(event):
    upload_covariate_data.is_uploaded = False
    # Check if covariate data directory found
    if add_covariate_data.file is not None:
        add_covariate_data.covariate_data = upload.dataset.append_covariate_data(path=add_covariate_data_text.value,
                                                                                 icv=append_icv_checkbox.value,
                                                                                 tbv=append_tbv_checkbox)
        # Update sidebar data preview
        data.value = add_covariate_data.covariate_data.iloc[:, :min(20, add_covariate_data.covariate_data.shape[1])]
        # Populate analysis select dropdowns with covariate data
        covariate_selector.options = add_covariate_data.covariate_data.columns.tolist()[1:]
        outcome_select.options = covariate_selector.options
        pn.state.notifications.success('Covariate data upload successful.')

# Event listeners for sidebar items 
dir_select_button.on_click(dir_select)
id_type_select.param.watch(check_custom, 'value')
id_list_text.param.watch(custom_list_format, 'value')
file_upload_button.on_click(upload)
add_covariate_data_button.on_click(add_covariate_data)
upload_covariate_data_button.on_click(upload_covariate_data)

data.visible = False

# Sidebar layout
side_col = pn.Column('# Upload Data',
                     dir_select_button,
                     dir_select_text, 
                     id_type_select,
                     id_type_tooltip,
                     id_list_text, 
                     file_upload_button,
                     add_covariate_data_button,
                     add_covariate_data_text,
                     append_icv_checkbox,
                     append_tbv_checkbox,
                     upload_covariate_data_button,
                     pn.layout.Divider(),
                     '### Data Preview',
                     data_note,
                     data)

# %% [markdown]
# ### Visualization events

# %%
# Handle updating available visualization options according to selected visualization type
def check_vis_type(event):
    # Available options for sunburst, treemap, and icicle plots
    if event.new == 'sunburst' or event.new == 'treemap' or event.new == 'icicle':
        type_select.visible = True
        base_level_select.visible = True
        id_single_select.visible = True
        id_multi_text.visible = False
        x_select.visible = False
        y_select.visible = False
        log_select.visible = False
        
        # Image upload
        image_upload_button.visible = False
        image_select_text.visible = False
        # Image options row
        image_view_select.visible = False
        image_size_input.visible = False
        image_size_tooltip.visible = False
        # Image region selector
        region_selector.visible = False
        # Image navigation row
        image_plot_arrow_row.visible = False
        image_plot.visible = False

    # Available options for bar plot
    elif event.new == 'bar':
        type_select.visible = True
        base_level_select.visible = True
        id_single_select.visible = False
        id_multi_text.visible = True
        x_select.visible = True
        y_select.visible = True
        log_select.visible = True

        # Image upload
        image_upload_button.visible = False
        image_select_text.visible = False
        # Image options row
        image_view_select.visible = False
        image_size_input.visible = False
        image_size_tooltip.visible = False
        # Image region selector
        region_selector.visible = False
        # Image navigation row
        image_plot_arrow_row.visible = False
        image_plot.visible = False

    # Available options for mean difference plot    
    elif event.new == 'mean_diff':
        type_select.visible = True
        base_level_select.visible = True
        id_single_select.visible = False
        id_multi_text.visible = True
        x_select.visible = True
        y_select.visible = False
        log_select.visible = False
        
        # Image upload
        image_upload_button.visible = False
        image_select_text.visible = False
        # Image options row
        image_view_select.visible = False
        image_size_input.visible = False
        image_size_tooltip.visible = False
        # Image region selector
        region_selector.visible = False
        # Image navigation row
        image_plot_arrow_row.visible = False
        image_plot.visible = False

    # Available options for correlation matrix plot
    elif event.new == 'corr_matrix':
        type_select.visible = True
        base_level_select.visible = True
        id_single_select.visible = False
        id_multi_text.visible = True
        x_select.visible = False
        y_select.visible = False
        log_select.visible = False
        
        # Image upload
        image_upload_button.visible = False
        image_select_text.visible = False
        # Image options row
        image_view_select.visible = False
        image_size_input.visible = False
        image_size_tooltip.visible = False
        # Image region selector
        region_selector.visible = False
        # Image navigation row
        image_plot_arrow_row.visible = False
        image_plot.visible = False

    # Available options for image data (MNI) viewer
    elif event.new == 'imaging':
        type_select.visible = False
        base_level_select.visible = False
        id_single_select.visible = False
        id_multi_text.visible = False
        x_select.visible = False
        y_select.visible = False
        log_select.visible = False
        
        # Image upload
        image_upload_button.visible = True
        image_select_text.visible = False
        # Image options row
        image_view_select.visible = False
        image_size_input.visible = False
        image_size_tooltip.visible = False
        # Image region selector
        region_selector.visible = False
        # Image navigation row
        image_plot_arrow_row.visible = False
        vis_plot.visible = False

# Format text input ID list into Python list
def id_list_format(event):
    text = event.new
    if text == 'all':
        id_list_format.text_list = list(id_single_select.options)
    else:
        text = text.replace(', ', ',')
        id_list_format.text_list = text.split(',')
    
# Handle visualization generation
def generate(event):
    if upload.is_uploaded:
        # Generate sunburst plot
        if vis_select.value == 'sunburst':
            vis_plot.object = upload.dataset.generate_sunburst(type=int(type_select.value), 
                                                        id=str(id_single_select.value), 
                                                        base_level=int(base_level_select.value))
            vis_plot.visible = True
        # Generate treemap plot
        elif vis_select.value == 'treemap':
            vis_plot.object = upload.dataset.generate_treemap(type=int(type_select.value), 
                                                        id=str(id_single_select.value), 
                                                        base_level=int(base_level_select.value))
            vis_plot.visible = True
        # Generate icicle plot
        elif vis_select.value == 'icicle':
            vis_plot.object = upload.dataset.generate_icicle(type=int(type_select.value), 
                                                        id=str(id_single_select.value), 
                                                        base_level=int(base_level_select.value))
            vis_plot.visible = True
        # Generate bar plot
        elif vis_select.value == 'bar':
            vis_plot.object = upload.dataset.generate_bar(type=int(type_select.value), 
                                                        id=id_list_format.text_list, 
                                                        level=int(base_level_select.value),
                                                        x=x_select.value,
                                                        y=y_select.value,
                                                        log_y=eval(log_select.value))
            vis_plot.visible = True
        # Generate mean difference plot
        elif vis_select.value == 'mean_diff':
            vis_plot.object = upload.dataset.generate_mean_diff(type=int(type_select.value),
                                                                id=id_list_format.text_list,
                                                                level=int(base_level_select.value),
                                                                color=x_select.value)
            vis_plot.visible = True
        # Generate correlation matrix plot
        elif vis_select.value == 'corr_matrix':
            vis_plot.object = upload.dataset.generate_corr_matrix(type=int(type_select.value),
                                                                  id=id_list_format.text_list,
                                                                  level=int(base_level_select.value))
            vis_plot.visible = True
    
    # Check if image data exists
    if upload_image.image_is_uploaded:
        # Generate image data viewer
        if vis_select.value == 'imaging':
            image_plot.object = imaging.generate_3d_image(img_path=image_select_text.value, 
                                                        regions=region_selector.value,
                                                        view=image_view_select.value, 
                                                        nrows=image_size_input.value,
                                                        ncols=image_size_input.value,
                                                        slice_n=0)
            image_plot_int_input.end = 100
            # If nrows or ncols > 1, generate grid
            if image_size_input.value > 1:
                image_plot.visible = False
            # Else, open slice-by-slice viewer
            else:
                image_plot.visible = True
                image_plot_arrow_row.visible = True

# Handle image data upload event
def upload_image(event):
    upload_image.image_is_uploaded = False
    # Open windows explorer
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = Tk()
    root.withdraw()                                        
    root.call('wm', 'attributes', '.', '-topmost', True) 
    # root.call('tk', 'scaling', 2.0)  
    upload_image.file = filedialog.askopenfilename()

    # Store selected directory and populate available regions for future selection
    image_select_text.value = upload_image.file
    region_selector.options = imaging._imaging_read_lookup(imaging._LEVEL_COLUMNS).iloc[:, 0].tolist()
    upload_image.image_is_uploaded = True

    # Reveal image data options if image upload successful
    if upload_image.image_is_uploaded:
        image_select_text.visible = True
        image_view_select.visible = True
        image_size_input.visible = True
        image_size_tooltip.visible = True
        region_selector.visible = True

# Go back 5 slices (indexes) in image array and regenerate plot
def prev_slice_single(event):
    image_plot_int_input.value = max(0, image_plot_int_input.value - 5)
    image_plot.object = imaging.generate_3d_image(img_path=image_select_text.value, 
                                                        regions=region_selector.value,
                                                        view=image_view_select.value, 
                                                        nrows=image_size_input.value,
                                                        ncols=image_size_input.value,
                                                        slice_n=image_plot_int_input.value)

# Go forward 5 slices (indexes) in image array and regenerate plot
def next_slice_single(event):
    image_plot_int_input.value = max(0, image_plot_int_input.value + 5)
    image_plot.object = imaging.generate_3d_image(img_path=image_select_text.value, 
                                                        regions=region_selector.value,
                                                        view=image_view_select.value, 
                                                        nrows=image_size_input.value,
                                                        ncols=image_size_input.value,
                                                        slice_n=image_plot_int_input.value)

# Go back 10 slices (indexes) in image array and regenerate plot
def prev_slice_multiple(event):
    image_plot_int_input.value = max(0, image_plot_int_input.value - 10)
    image_plot.object = imaging.generate_3d_image(img_path=image_select_text.value, 
                                                        regions=region_selector.value,
                                                        view=image_view_select.value, 
                                                        nrows=image_size_input.value,
                                                        ncols=image_size_input.value,
                                                        slice_n=image_plot_int_input.value)

# Go forward 10 slices (indexes) in image array and regenerate plot
def next_slice_multiple(event):
    image_plot_int_input.value = max(0, image_plot_int_input.value + 10)
    image_plot.object = imaging.generate_3d_image(img_path=image_select_text.value, 
                                                        regions=region_selector.value,
                                                        view=image_view_select.value, 
                                                        nrows=image_size_input.value,
                                                        ncols=image_size_input.value,
                                                        slice_n=image_plot_int_input.value)

# Jump to specific slice (integer index input)
def select_slice(event):
    image_plot.object = imaging.generate_3d_image(img_path=image_select_text.value, 
                                                        regions=region_selector.value,
                                                        view=image_view_select.value, 
                                                        nrows=image_size_input.value,
                                                        ncols=image_size_input.value,
                                                        slice_n=image_plot_int_input.value)

# Event listeners for visualization items
vis_select.param.watch(check_vis_type, 'value')
id_multi_text.param.watch(id_list_format, 'value')
# slider.param.watch(slide, 'value')
generate_button.on_click(generate)
image_upload_button.on_click(upload_image)
image_plot_left_arrow_single.on_click(prev_slice_single)
image_plot_right_arrow_single.on_click(next_slice_single)
image_plot_left_arrow_multiple.on_click(prev_slice_multiple)
image_plot_right_arrow_multiple.on_click(next_slice_multiple)
image_plot_int_input_button.on_click(select_slice)

# Image viewer layout
image_plot_arrow_row = pn.Row(image_plot_int_input,
                              image_plot_int_input_button,
                              pn.layout.Spacer(width=75),
                              image_plot_left_arrow_multiple,
                              image_plot_left_arrow_single, 
                              image_plot_right_arrow_single,
                              image_plot_right_arrow_multiple,)
image_plot_arrow_row.visible = False
vis_options = pn.Row(vis_select, type_select, base_level_select, id_single_select, 
                     id_multi_text, x_select, y_select, log_select, image_upload_button,
                     image_select_text)
image_options = pn.Row(image_view_select, image_size_input, image_size_tooltip)

# Visualization mode layout
vis_col_header = pn.Row('# Visualization', pn.layout.HSpacer(), mode_radio)
vis_col = pn.Column(vis_col_header,
                     vis_options,
                     image_options,
                     region_selector,
                     generate_button,
                     pn.layout.Spacer(height=50),
                     image_plot_arrow_row,
                     image_plot,
                     vis_plot)

# %% [markdown]
# ### Analysis events

# %%
def check_analysis_select(event):
    new_analysis = event.new
    # Check if ordinary least squares regression is selected
    if new_analysis == 'ols':
        residual_plot_checkbox.visible = True
        roc_plot_checkbox.visible = False
        n_estimators_int_input.visible = False
        random_state_int_input.visible = False
        classifier_checkbox.visible = False
        importance_plot_checkbox.visible = False
    # Check if logistical regression is selected
    elif new_analysis == 'logit':
        residual_plot_checkbox.visible = False
        roc_plot_checkbox.visible = True
        n_estimators_int_input.visible = False
        random_state_int_input.visible = False
        classifier_checkbox.visible = False
        importance_plot_checkbox.visible = False
    # Check if random forest is selected
    elif new_analysis == 'randomforest':
        analysis_level_select.visible = False
        residual_plot_checkbox.visible = False
        roc_plot_checkbox.visible = False
        n_estimators_int_input.visible = True
        random_state_int_input.visible = True
        classifier_checkbox.visible = True
        importance_plot_checkbox.visible = True
        
        # Populate covariate list filtered with Type 1, Level 5 regions as default
        original_covariates = add_covariate_data.covariate_data.columns.tolist()[1:]
        covariate_selector.options = [col for col in original_covariates if ('_Type' not in col) or (('_Type1.0_' in col) and ('_L5.0' in col))]

def check_analysis_type(event):
    new_type = event.new
    # Populate covariate selection list
    original_covariates = add_covariate_data.covariate_data.columns.tolist()[1:]
    # Filter according to selected analysis method and type
    if analysis_select.value == 'randomforest':
        covariate_selector.options = [col for col in original_covariates if ('_Type' not in col) or (('_Type' + new_type + '.0_' in col) and ('_L5.0' in col))]
    else:
        covariate_selector.options = [col for col in original_covariates if ('_Type' not in col) or (('_Type' + new_type + '.0_' in col) and ('_L' + analysis_level_select.value + '.0' in col))]

def check_analysis_level(event):
    new_level = event.new
    # Populate covariate selection list
    original_covariates = add_covariate_data.covariate_data.columns.tolist()[1:]
    # Filter according to selected analysis method and type
    if analysis_select.value == 'randomforest':
        covariate_selector.options = [col for col in original_covariates if ('_Type' not in col) or (('_Type' + analysis_type_select.value + '.0_' in col) and ('_L5.0' in col))]
    else:
        covariate_selector.options = [col for col in original_covariates if ('_Type' not in col) or (('_Type' + analysis_type_select.value + '.0_' in col) and ('_L' + new_level + '.0' in col))]

def run_analysis(event):
    # OLS
    if analysis_select.value == 'ols':
        # Check if normalization factor selected
        if normalize_factor_radio.value != 'none':
            normalized_covariate_data = upload.dataset.normalize_covariate_data(add_covariate_data.covariate_data, 
                                                                                        normalizing_factor=normalize_factor_radio.value)
        try:
            # Attempt to use normalized data to produce analysis results
            result = upload.dataset.OLS(normalized_covariate_data, 
                                        covariates=covariate_selector.value, 
                                        outcome=outcome_select.value,
                                        log=log_covariates_checkbox.value,
                                        residual_plot=residual_plot_checkbox.value)
        except:
            # Fallback if no normalized data found
            result = upload.dataset.OLS(add_covariate_data.covariate_data, 
                                        covariates=covariate_selector.value, 
                                        outcome=outcome_select.value,
                                        log=log_covariates_checkbox.value,
                                        residual_plot=residual_plot_checkbox.value)
        # sklearn regression summary output
        analysis_output.object = result[0]
        # Generate residual plot
        if residual_plot_checkbox.value == True:
            analysis_plot.object = result[1]
            analysis_plot.visible = True
    # Logit
    if analysis_select.value == 'logit':
        # Check if normalization factor selected
        if normalize_factor_radio.value != 'none':
            normalized_covariate_data = upload.dataset.normalize_covariate_data(add_covariate_data.covariate_data, 
                                                                                        normalizing_factor=normalize_factor_radio.value)
        try:
            # Attempt to use normalized data to produce analysis results
            result = upload.dataset.Logit(normalized_covariate_data, 
                                        covariates=covariate_selector.value, 
                                        outcome=outcome_select.value,
                                        log=log_covariates_checkbox.value,
                                        roc_plot=roc_plot_checkbox.value)
        except:
            # Fallback if no normalized data found
            result = upload.dataset.Logit(add_covariate_data.covariate_data, 
                                        covariates=covariate_selector.value, 
                                        outcome=outcome_select.value,
                                        log=log_covariates_checkbox.value,
                                        roc_plot=roc_plot_checkbox.value)
        # sklearn regression summary output
        analysis_output.object = result[0]
        # Generate ROC plot
        if roc_plot_checkbox.value == True:
            analysis_plot.object = result[1]
            analysis_plot.visible = True
    # Random Forest
    if analysis_select.value == 'randomforest':
        # Check if normalization factor selected
        if normalize_factor_radio.value != 'none':
            normalized_covariate_data = upload.dataset.normalize_covariate_data(add_covariate_data.covariate_data, 
                                                                                        normalizing_factor=normalize_factor_radio.value)
        try:
            # Attempt to use normalized data to produce analysis results
            result = upload.dataset.RandomForest(normalized_covariate_data, 
                                        covariates=covariate_selector.value, 
                                        outcome=outcome_select.value,
                                        log=log_covariates_checkbox.value,
                                        classifier=classifier_checkbox.value,
                                        n_estimators=n_estimators_int_input.value,
                                        random_state=random_state_int_input.value,
                                        importance_plot=importance_plot_checkbox.value)
        except:
            # Fallback if no normalized data found
            result = upload.dataset.RandomForest(add_covariate_data.covariate_data, 
                                        covariates=covariate_selector.value, 
                                        outcome=outcome_select.value,
                                        log=log_covariates_checkbox.value,
                                        classifier=classifier_checkbox.value,
                                        n_estimators=n_estimators_int_input.value,
                                        random_state=random_state_int_input.value,
                                        importance_plot=importance_plot_checkbox.value)
        # Random forest analysis output
        analysis_output.object = 'rf: ' + str(result[0]) + '\n'
        analysis_output.object += 'y_pred: ' + str(result[1]) + '\n'
        analysis_output.object += 'accuracy: {:.2f}\n'.format(result[2])
        analysis_output.object += 'mse: {:.2f}\n'.format(result[3])
        # Generate feature importance plot
        if importance_plot_checkbox.value == True:
            analysis_plot.object = result[4]
            analysis_plot.visible = True

# Event listeners for analysis items
analysis_select.param.watch(check_analysis_select, 'value')
analysis_type_select.param.watch(check_analysis_type, 'value')
analysis_level_select.param.watch(check_analysis_level, 'value')
run_button.on_click(run_analysis)

# Analysis mode layout
analysis_normalize_factor_col = pn.Column(pn.widgets.StaticText(value='Normalizing Factor'),
                                          normalize_factor_radio)
analysis_options = pn.Row(analysis_select, outcome_select)
analysis_col_header = pn.Row('# Analysis', pn.layout.HSpacer(), mode_radio)
analysis_col = pn.Column(analysis_col_header,
                         analysis_options,
                         pn.Row(analysis_normalize_factor_col, analysis_type_select, analysis_level_select, 
                                n_estimators_int_input, random_state_int_input),
                         pn.widgets.StaticText(value='Covariates'),
                         covariate_selector,
                         pn.Row(log_covariates_checkbox, residual_plot_checkbox, roc_plot_checkbox, 
                                classifier_checkbox, importance_plot_checkbox),
                         run_button,
                         analysis_output,
                         analysis_plot,
                         visible=False)

# %% [markdown]
# ### Mode handling

# %%
# Main window layout
main_col = pn.Column(vis_col, analysis_col)

# Handle switching between visualization and analysis modes
def switch_mode(event):
    if vis_col.visible == True:
        vis_col.visible = False
        analysis_col.visible = True
        mode_radio.name = 'View visualization tools'
    else:
        analysis_col.visible = False
        vis_col.visible = True
        mode_radio.name = 'View analysis tools'

# Event listener for mode switching button
mode_radio.on_click(switch_mode)

# %% [markdown]
# ### Render page

# %%
page = pn.template.BootstrapTemplate(
    title='MRICloudPy',
    sidebar=[side_col],
)

page.main.append(
    pn.Column(main_col),
)

page.show()


