import pandas as pd
import read
import access
import visuals
import analysis
import imaging

class Data:

    LEVEL_FILE = "main\multilevel_lookup_table.txt"

    LEVEL_COLUMNS = ['Type1-L5 Statistics', 'Type1-L4 Statistics', 
                'Type1-L3 Statistics', 'Type1-L2 Statistics',
                'Type1-L1 Statistics', 'Type2-L5 Statistics',
                'Type2-L4 Statistics', 'Type2-L3 Statistics',
                'Type2-L2 Statistics', 'Type2-L1 Statistics']

    def __init__(self, path: str, id_type: str = 'numeric', id_list: list = None): 
        self.path = path
        self.id_type = id_type
        self.id_list = id_list
        self.df = self.import_data(path, id_type, id_list)
        return

    # Retrieves list of text files from directory
    def get_files(self, path):
        return read.get_files(self, path)

    # Retrieve, clean-up, and return header from data file
    def get_header(self, f):
        return read.get_header(self, f)

    # Retrieve first index/line of data
    def get_start_index(self, f):
        return read.get_start_index(self, f)

    # Workaround to import first level label
    def type1_l1_exception(self, f, df):
        return read.type1_l1_exception(self, f, df)

    # Read level lookup table into dataframe
    def read_lookup_table(self, col):
        return read.read_lookup_table(self, col)

    # Assign type label according to index
    def get_type(self, i):
        return read.get_type(self, i)

    # Assign level label according to index
    def get_level(self, i):
        return read.get_level(self, i)

    # Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
    def level5_lookup(self, df, dfl):
        return read.level5_lookup(self, df, dfl)

    # Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
    def level4_lookup(self, df, dfl):
        return read.level4_lookup(self, df, dfl)

    # Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
    def level3_lookup(self, df, dfl):
        return read.level3_lookup(self, df, dfl)

    # Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
    def level2_lookup(self, df, dfl):
        return read.level2_lookup(self, df, dfl)

    # Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
    def level1_lookup(self, df):
        return read.level1_lookup(self, df)

    # Append base region and hemisphere columns
    def append_region_cols(self, df: pd.DataFrame):
        return read.append_region_cols(self, df)

    # Appends hierarchical level 1-5 and ICV columns
    def append_hierarchy_cols(self, df: pd.DataFrame, base_level: int):
        return read.append_hierarchy_cols(self, df, base_level)

    # Import and read data file into dataframe
    def read_file(self, file: str): 
        return read.read_file(self, file)

    # Returns dataframe of type/level labels with preserved indices
    def get_type_labels(self, file):
        return read.get_type_labels(self, file)

    # Combines dataframes from a list of files
    def import_data(self, path: str, id_type: str = 'numeric', id_list: list = None):
        return read.import_data(self, path, id_type, id_list)

    # Renames specific subject ID
    def rename_subject(self, old: str, new: str):
        return access.rename_subject(self, old, new)

    def get_data(self):
        return access.get_data(self)

    # Return list of all unique IDs in a dataframe
    def get_id(self):
        return access.get_id(self)
    
    # Converts dataframe from long to wide form
    def long_to_wide(self):
        return access.long_to_wide(self)

    def chat(self, key):
        return access.chat(self, key)

    # Get hiearchy path for 'part-of-whole' figure function according to base level
    def get_hierarchy_path(self, base_level):
        return visuals.get_hierarchy_path(self, base_level)

    # Generate Plotly Express sunburst model from dataframe
    def generate_sunburst(self, type: int, id: str, base_level: str = 5):
        return visuals.generate_sunburst(self, type, id, base_level)

    def generate_treemap(self, type: int, id: str, base_level: str = 5):
        return visuals.generate_treemap(self, type, id, base_level)

    def generate_icicle(self, type: int, id: str, base_level: str = 5):
        return visuals.generate_icicle(self, type, id, base_level)

    # Generate Plotly Express bar graph from dataframe
    def generate_bar(self, type: int, level: int, id: list = None, 
            x: str = 'ID', y: str = 'Prop', log_y: bool = False):
        return visuals.generate_bar(self, type, level, id, x, y, log_y)
     
    def get_mean_diff(self, df):
        return visuals.get_mean_diff(self, df)

    # Generate mean difference between left and right hemispheres of brain
    def generate_mean_diff(self, type: int, level: int, color: str = 'ID', id: list = None):
        return visuals.generate_mean_diff(self, type, level, color, id)

    # Transform dataframe for correlation matrix
    def corr_transform(self, df):
        return visuals.corr_transform(self, df)

    def generate_corr_matrix(self, type: int, level: int, id: list = None):
        return visuals.generate_corr_matrix(self, type, level, id)
    
    def append_covariate_data(self, file: str, icv: bool = False, tbv: bool = False):
        return read.append_covariate_data(self, file, icv, tbv)
    
    def normalize_covariate_data(self, covariate_dataset, normalizing_factor: str):
        return access.normalize_covariate_data(self, covariate_dataset, normalizing_factor)
    
    def OLS(self, covariate_dataset, covariates: list, outcome: str, log: bool = False):
        return analysis.OLS(self, covariate_dataset, covariates, outcome, log)
    
    def Logit(self, covariate_dataset, covariates: list, outcome: str, log: bool = False):
        return analysis.Logit(self, covariate_dataset, covariates, outcome, log)
    
    def RandomForest(self, covariate_dataset, covariates: list, outcome: str):
        return analysis.RandomForest(self, covariate_dataset, covariates, outcome)

if __name__ == '__main__':
    print(__name__)