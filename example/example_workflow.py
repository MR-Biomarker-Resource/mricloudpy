import mricloudpy as mp
# from imaging import generate_3d_image

SUBJECTS = ['Kermit', 'Miss Piggy', 'Fozzie', 'Gonzo',
'Rowlf', 'Scooter', 'Animal', 'Pepe', 'Rizzo', 'Beaker', 
'Statler', 'Waldorf', 'Swedish Chef', 'Bob', 'Sally']

DATA_PATH = 'sample_data_covariate'
COVARIATE_DATA_PATH = 'sample_data_covariate\hcp_sample_clean.csv'
IMG_PATH = 'template\JHU_MNI_SS_T1_283Labels_M2.img'

dataset = mp.Data(path=DATA_PATH, id_type='custom', id_list=SUBJECTS)
covariate_dataset = dataset.append_covariate_data(path=COVARIATE_DATA_PATH, icv=True, tbv=True)

# print(generate_3d_image(img_path=IMG_PATH, regions=['CSF'], view=2, nrows=6, ncols=6, slice_n=100))
covariate_dataset = dataset.normalize_covariate_data(covariate_dataset, normalizing_factor='none')
print(dataset.OLS(covariate_dataset, covariates=['Age', 'Cerebellum_L_Type1.0_L3.0', 'Hippo_L_Type1.0_L4.0'], outcome='CSF_Type1.0_L1.0', log=False))
# print(dataset.Logit(covariate_dataset, covariates=['Age', 'CSF_Type1.0_L1.0', 'Cerebellum_L_Type1.0_L3.0', 'Hippo_L_Type1.0_L4.0'], outcome='Gender', log=False, roc_plot=True))
# print(dataset.RandomForest(covariate_dataset, covariates=['Age', 'Cerebellum_L_Type1.0_L3.0', 'Hippo_L_Type1.0_L4.0', 'CSF_Type1.0_L1.0'], outcome='Gender'))










