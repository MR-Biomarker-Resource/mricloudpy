import nibabel as nib
import plotly_express as px
import read
import mricloudpy as mp
import numpy as np

IMG_PATH = 'template\JHU_MNI_SS_T1_283Labels_M2.img'
HDR_PATH = 'template\JHU_MNI_SS_T1_283Labels_M2.hdr'

img = nib.load(IMG_PATH)
hdr = nib.load(HDR_PATH)

lookup = read.read_lookup_table(mp.Data, mp.Data.LEVEL_COLUMNS).iloc[:, 0]
lookup.index += 1
lookup = lookup.to_dict()
lookup[0] = 'NA'

def remove_skull(slice_intensity: list):
    excluded = [249, 250, 251]
    for i in range(len(slice_intensity)):
        mask = np.isin(slice_intensity[i], excluded)
        slice_intensity[i][mask] = 0
    return slice_intensity

# Convert region IDs to region names
# slice_sagittal = [np.vectorize(lookup.get)(i).T for i in slice_sagittal_intensity]
# slice_coronal = [np.vectorize(lookup.get)(i).T for i in slice_coronal_intensity]
# slice_horizontal = [np.vectorize(lookup.get)(i).T for i in slice_horizontal_intensity]

def generate_3d_image(img, regions: list):

    # Import image data
    data = img.get_fdata()
    data = data.reshape(data.shape[0], data.shape[1], data.shape[2])

    # Clean and organize image data
    slice_sagittal_intensity = [data[i, :, :] for i in range(0, data.shape[0])]
    slice_sagittal_intensity = remove_skull(slice_sagittal_intensity)

    slice_coronal_intensity = [data[:, i, :] for i in range(0, data.shape[1])]
    slice_coronal_intensity = remove_skull(slice_coronal_intensity)

    slice_horizontal_intensity = [data[:, :, i] for i in range(0, data.shape[2])]
    slice_horizontal_intensity = remove_skull(slice_horizontal_intensity)

    # Convert region names to region IDs
    regions_id = [i for i,j in lookup.items() if j in regions]

    # Filter images for specificed regions
    regions_sagittal = np.array([np.where(np.isin(arr, regions_id), arr, 0) for arr in slice_sagittal_intensity])
    regions_coronal = np.array([np.where(np.isin(arr, regions_id), arr, 0) for arr in slice_coronal_intensity])
    regions_horizontal = np.array([np.where(np.isin(arr, regions_id), arr, 0) for arr in slice_horizontal_intensity])

    # Generate figure for each view
    fig_sagittal = px.imshow(regions_sagittal.T, animation_frame=2, origin='lower', 
                            color_continuous_scale='ice', title='sagittal', color_continuous_midpoint=140)
    fig_coronal = px.imshow(regions_coronal.T, animation_frame=2, origin='lower', 
                            color_continuous_scale='ice', title='coronal')
    fig_horizontal = px.imshow(regions_horizontal.T, animation_frame=2, origin='lower', 
                            color_continuous_scale='ice', title='horizontal')
    figs = [fig_sagittal, fig_coronal, fig_horizontal]

    # Remove axes from figures and change animation_frame label
    for i in figs:
        i.update_xaxes(visible=False)
        i.update_yaxes(visible=False)
        i.update_layout(sliders=[{"currentvalue": {"prefix": "Slice: "}}])

    fig_sagittal.show()
    fig_coronal.show()
    fig_horizontal.show()

    return figs

if __name__ == '__main__':
    print(__name__)