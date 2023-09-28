import mricloudpy as mp
from imaging import generate_3d_image

SUBJECTS = ['Kermit', 'Miss Piggy', 'Fozzie', 'Gonzo',
'Rowlf','Scooter', 'Animal', 'Pepe', 'Rizzo', 'Beaker', 
'Statler', 'Waldorf', 'Swedish Chef']

DATA_PATH = 'sample_data'

IMG_PATH = 'template\JHU_MNI_SS_T1_283Labels_M2.img'

dataset = mp.Data(path=DATA_PATH, id_type='custom',
    id_list=SUBJECTS)

#dataset.chat('123')

print(dataset.get_data())
print(generate_3d_image(IMG_PATH, ['CSF']))

# dataset_wide = dataset.long_to_wide()
# print(dataset_wide)
# print(dataset.generate_sunburst(type=1, id='Beaker', base_level=5))
# dataset.generate_mean_diff(type=1, level=4)
# dataset.generate_corr_matrix(type=2, level=2)
# dataset.generate_bar(type=2, level=5)










