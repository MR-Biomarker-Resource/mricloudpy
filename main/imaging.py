import nibabel as nib
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import ndimage

LEVEL_FILE = "main\multilevel_lookup_table.txt"

LEVEL_COLUMNS = ['Type1-L5 Statistics', 'Type1-L4 Statistics', 
                'Type1-L3 Statistics', 'Type1-L2 Statistics',
                'Type1-L1 Statistics', 'Type2-L5 Statistics',
                'Type2-L4 Statistics', 'Type2-L3 Statistics',
                'Type2-L2 Statistics', 'Type2-L1 Statistics']

IMG_PATH = 'template\JHU_MNI_SS_T1_283Labels_M2.img'
HDR_PATH = 'template\JHU_MNI_SS_T1_283Labels_M2.hdr'

TEMPLATE_PATH = 'mni_template_data\mni_icbm152_t1_tal_nlin_sym_09c.nii'

def imaging_read_lookup(col):
    df = pd.read_csv(LEVEL_FILE, sep='\t', skiprows=1, index_col=False, 
        header=None, usecols=range(1, 11), names=col)

    return df

def create_lookup_dict(col):
    lookup_dict = imaging_read_lookup(col).iloc[:, 0]
    lookup_dict.index += 1
    lookup_dict = lookup_dict.to_dict()
    lookup_dict[0] = 'NA'

    return lookup_dict

def remove_skull(slice_intensity: list):
    excluded = [249, 250, 251]
    for i in range(len(slice_intensity)):
        mask = np.isin(slice_intensity[i], excluded)
        slice_intensity[i][mask] = 0
    return slice_intensity

def generate_3d_image(img_path: str, regions: list, view: int, nrows: int, 
                      ncols: int, slice_n: int = 0):

    SAGITTAL_TITLE = generate_3d_image.__name__ + ': Sagittal View'
    CORONAL_TITLE = generate_3d_image.__name__ + ': Coronal View'
    HORIZONTAL_TITLE = generate_3d_image.__name__ + ': Horizontal View'
    COLOR_SCALE = [[0, 'black'], [0.5 ,'red'], [1, 'white']]

    img = nib.load(img_path)
    template = nib.load(TEMPLATE_PATH)

    # 'view' dictionary
    # 0 = horizontal/axial
    # 1 = sagittal
    # 2 = coronal

    # Create lookup dictionary
    lookup_dict = create_lookup_dict(LEVEL_COLUMNS)

    # Import image data
    img_data = img.get_fdata()
    img_data = img_data.reshape(img_data.shape[0], img_data.shape[1], img_data.shape[2])
    template_data = template.get_fdata()

    # Clean and organize image data
    slice_sagittal_intensity = [img_data[i, :, :] for i in range(0, img_data.shape[0])]
    slice_sagittal_intensity = remove_skull(slice_sagittal_intensity)

    slice_coronal_intensity = [img_data[:, i, :] for i in range(0, img_data.shape[1])]
    slice_coronal_intensity = remove_skull(slice_coronal_intensity)

    slice_horizontal_intensity = [img_data[:, :, i] for i in range(0, img_data.shape[2])]
    slice_horizontal_intensity = remove_skull(slice_horizontal_intensity)

    # Convert region names to region IDs
    regions_id = [i for i,j in lookup_dict.items() if j in regions]

    # Filter images for specificed regions
    regions_sagittal = np.array([np.where(np.isin(arr, regions_id), arr, 0) for arr in slice_sagittal_intensity])
    regions_coronal = np.array([np.where(np.isin(arr, regions_id), arr, 0) for arr in slice_coronal_intensity])
    regions_horizontal = np.array([np.where(np.isin(arr, regions_id), arr, 0) for arr in slice_horizontal_intensity])
    
    # Slice-by-slice plot
    if nrows == 1 or ncols == 1:
        # Create empty figure
        fig = go.Figure()
        
        if view == 0: # Horizontal/axial
            # Resize template to fit image data
            template_data_resized = ndimage.zoom(template_data[:,:,slice_n].T, 
                                                (template_data.shape[0] / template_data.shape[0] * 1.1, 
                                                img_data.shape[1] / template_data.shape[1] * 1.1))
            # Draw template data in background
            fig.add_trace(go.Heatmap(z=template_data_resized,
                                    colorscale='Gray',
                                    showscale=False))
            fig.add_trace(go.Heatmap(z=regions_horizontal[slice_n,:,:].T, 
                                    colorscale=[[0, 'rgba(0,0,0,0)'], [0.01, 'rgb(128, 0, 32)'], [1, 'red']],
                                    showscale=False,
                                    x0=10,
                                    y0=5, 
                                    zmid=140,
                                    opacity=1.0))
        elif view == 1: # Sagittal
            # Resize template to fit image data
            template_data_resized = ndimage.zoom(template_data[slice_n,:,:].T, 
                                                (template_data.shape[0] / template_data.shape[0] * 1.1, 
                                                img_data.shape[1] / template_data.shape[1] * 1.1))
            # Draw template data in background
            fig.add_trace(go.Heatmap(z=template_data_resized,
                                    colorscale='Gray',
                                    showscale=False))
            fig.add_trace(go.Heatmap(z=regions_sagittal[slice_n,:,:].T, 
                                    colorscale=[[0, 'rgba(0,0,0,0)'], [0.01, 'rgb(128, 0, 32)'], [1, 'red']],
                                    showscale=False,
                                    x0=10,
                                    y0=5, 
                                    zmid=140,
                                    opacity=1.0))
        else: # Coronal
            # Resize template to fit image data
            template_data_resized = ndimage.zoom(template_data[:,slice_n,:].T, 
                                                (template_data.shape[0] / template_data.shape[0] * 1.1, 
                                                img_data.shape[1] / template_data.shape[1] * 1.1))
            # Draw template data in background
            fig.add_trace(go.Heatmap(z=template_data_resized,
                                    colorscale='Gray',
                                    showscale=False))
            fig.add_trace(go.Heatmap(z=regions_coronal[slice_n,:,:].T, 
                                    colorscale=[[0, 'rgba(0,0,0,0)'], [0.01, 'rgb(128, 0, 32)'], [1, 'red']],
                                    showscale=False,
                                    x0=10,
                                    y0=5, 
                                    zmid=140,
                                    opacity=1.0))

        # Clean up, reshape, and organize figure for clarity
        fig.update_layout(yaxis=dict(scaleanchor='x'),
                        coloraxis=dict(showscale=False),
                        plot_bgcolor='rgba(0, 0, 0, 0)')
        fig.update_xaxes(visible=False, showticklabels=False, scaleanchor='y')
        fig.update_yaxes(visible=False, showticklabels=False, scaleanchor='x')

        return fig

    # Create subplot figure
    total_plots = nrows * ncols
    fig_height = nrows * 200
    fig_width = ncols * 200
    fig = make_subplots(rows=nrows, 
                        cols=ncols,
                        shared_xaxes=True, 
                        shared_yaxes=True,
                        vertical_spacing=0,
                        horizontal_spacing=0)

    # Iterate through subplot grid cells
    for i in fig._get_subplot_rows_columns()[0]:
        for j in fig._get_subplot_rows_columns()[1]:
            # Track current total index
            current_total_index = ((i-1)*ncols)+(j-1)

            # Calculate equal intervals to fill subplots
            intervals = (img_data.shape[0] // total_plots)
            result = [intervals] * total_plots
            if img_data.shape[2] - sum(result) >= 0:
                result[0] += img_data.shape[2] - sum(result)
            else:
                result[0] = 0
            cumsum_result = [sum(result[:i]) for i in range(len(result))]

            #Check view selection and draw image data
            if view == 0: # Horizontal/axial
                # Resize template to fit image data
                template_data_resized = ndimage.zoom(template_data[:,:,cumsum_result[current_total_index]].T, 
                                                 (template_data.shape[0] / template_data.shape[0] * 1.1, 
                                                  img_data.shape[1] / template_data.shape[1] * 1.1))
                # Draw template data in background
                fig.add_trace(go.Heatmap(z=template_data_resized,
                                        colorscale='Gray',
                                        showscale=False),
                                        row=i,
                                        col=j)
                fig.add_trace(go.Heatmap(z=regions_horizontal[cumsum_result[current_total_index],:,:].T, 
                                        colorscale=[[0, 'rgba(0,0,0,0)'], [0.01, 'rgb(128, 0, 32)'], [1, 'red']],
                                        showscale=False,
                                        x0=10,
                                        y0=5, 
                                        zmid=140,
                                        opacity=1.0),
                                        row=i,
                                        col=j)
            elif view == 1: # Sagittal
                # Resize template to fit image data
                template_data_resized = ndimage.zoom(template_data[cumsum_result[current_total_index],:,:].T, 
                                                 (template_data.shape[0] / template_data.shape[0] * 1.1, 
                                                  img_data.shape[1] / template_data.shape[1] * 1.1))
                # Draw template data in background
                fig.add_trace(go.Heatmap(z=template_data_resized,
                                        colorscale='Gray',
                                        showscale=False),
                                        row=i,
                                        col=j)
                fig.add_trace(go.Heatmap(z=regions_sagittal[cumsum_result[current_total_index],:,:].T, 
                                        colorscale=[[0, 'rgba(0,0,0,0)'], [0.01, 'rgb(128, 0, 32)'], [1, 'red']],
                                        showscale=False,
                                        x0=10,
                                        y0=5, 
                                        zmid=140,
                                        opacity=1.0),
                                        row=i,
                                        col=j)
            else: # Coronal
                # Resize template to fit image data
                template_data_resized = ndimage.zoom(template_data[:,cumsum_result[current_total_index],:].T, 
                                                 (template_data.shape[0] / template_data.shape[0] * 1.1, 
                                                  img_data.shape[1] / template_data.shape[1] * 1.1))
                # Draw template data in background
                fig.add_trace(go.Heatmap(z=template_data_resized,
                                        colorscale='Gray',
                                        showscale=False),
                                        row=i,
                                        col=j)
                fig.add_trace(go.Heatmap(z=regions_coronal[cumsum_result[current_total_index],:,:].T, 
                                        colorscale=[[0, 'rgba(0,0,0,0)'], [0.01, 'rgb(128, 0, 32)'], [1, 'red']],
                                        showscale=False,
                                        x0=10,
                                        y0=5, 
                                        zmid=140,
                                        opacity=1.0),
                                        row=i,
                                        col=j)
    
    # Clean up, reshape, and organize figure for clarity
    fig.update_layout(yaxis=dict(scaleanchor='x'),
                    coloraxis=dict(showscale=False),
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    height=fig_height,
                    width=fig_width)
    fig.update_xaxes(visible=False, showticklabels=False, scaleanchor='y')
    fig.update_yaxes(visible=False, showticklabels=False, scaleanchor='x')

    fig.show()
    return fig

if __name__ == '__main__':
    print(__name__)