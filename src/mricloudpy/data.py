import pandas as pd
from mricloudpy import read, access, visuals, analysis, imaging

class Data:
    """
    An object class for an MRICloud dataset.

    ...

    Attributes
    ----------
    path : str
        Path to MRICloud data text file
    id_type : str
        Type of subject ID formatting
    id_list : list
        List of custom subject IDs
    df : DataFrame
        DataFrame generated from path

    Methods
    -------
    import_data(path, id_type='numeric', id_list=None)
        Concatenate DataFrames from a list of MRICloud data files.
    rename_subject(old, new)
        Rename a specific subject ID.
    get_data()
        Retrieve DataFrame of a given data object.
    get_id()
        Retrieve list of unique subject IDs.
    long_to_wide()
        Convert default long form data to a wide format.
    chat(key)
        Use PandasAI on data object.
    generate_sunburst(type, id, base_level=5)
        Generate a Plotly Express sunburst Figure model.
    generate_treemap(type, id, base_level=5)
        Generate a Plotly Express treemap Figure model.
    generate_icicle(type, id, base_level=5)
        Generate a Plotly Express icicle Figure model.
    generate_bar(type, level, id=None, x='ID', y='Prop', log_y=False)
        Generates a Plotly Express bar graph Figure.
    generate_mean_diff(type, level, color='ID', id=None)
        Generate a Plotly Express mean difference plot Figure.
    generate_corr_matrix(type, level, id=None)
        Generate a Plotly Express heatmap Figure of a correlation matrix.
    append_covariate_data(file, icv=False, tbv=False)
        Append covariate dataset to data object.
    normalize_covariate_data(covariate_dataset, normalizing_factor)
        Normalize covariate data in data object by ICV, TBV, or ICV + TBV.
    OLS(covariate_dataset, covariates, outcome, log=False, residual_plot=False)
        Run statsmodels Ordinary Least Squares regression on data object.
    Logit(covariate_dataset, covariates, outcome, log=False, roc_plot=False)
        Run statsmodels Logit regression on data object.
    """

    _LEVEL_FILE = "src\mricloudpy\\resources\multilevel_lookup_table.txt"

    _LEVEL_COLUMNS = ['Type1-L5 Statistics', 'Type1-L4 Statistics', 
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
    def _get_files(self, path):
        return read._get_files(self, path)

    # Retrieve, clean-up, and return header from data file
    def _get_header(self, f):
        return read._get_header(self, f)

    # Retrieve first index/line of data
    def _get_start_index(self, f):
        return read._get_start_index(self, f)

    # Workaround to import first level label
    def _type1_l1_exception(self, f, df):
        return read._type1_l1_exception(self, f, df)

    # Read level lookup table into DataFrame
    def _read_lookup_table(self, col):
        return read._read_lookup_table(self, col)

    # Assign type label according to index
    def _get_type(self, i):
        return read._get_type(self, i)

    # Assign level label according to index
    def _get_level(self, i):
        return read._get_level(self, i)

    # Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
    def _level5_lookup(self, df, dfl):
        return read._level5_lookup(self, df, dfl)

    # Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
    def _level4_lookup(self, df, dfl):
        return read._level4_lookup(self, df, dfl)

    # Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
    def _level3_lookup(self, df, dfl):
        return read._level3_lookup(self, df, dfl)

    # Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
    def _level2_lookup(self, df, dfl):
        return read._level2_lookup(self, df, dfl)

    # Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
    def _level1_lookup(self, df):
        return read._level1_lookup(self, df)

    # Append base region and hemisphere columns
    def _append_region_cols(self, df: pd.DataFrame):
        return read._append_region_cols(self, df)

    # Appends hierarchical level 1-5 and ICV columns
    def _append_hierarchy_cols(self, df: pd.DataFrame, base_level: int):
        return read._append_hierarchy_cols(self, df, base_level)

    # Import and read data file into DataFrame
    def _read_file(self, file: str): 
        return read._read_file(self, file)

    # Returns DataFrame of type/level labels with preserved indices
    def _get_type_labels(self, file):
        return read._get_type_labels(self, file)

    # Combines DataFrames from a list of files
    def import_data(self, path: str, id_type: str = 'numeric', id_list: list = None):
        return read.import_data(self, path, id_type, id_list)

    # Renames specific subject ID
    def rename_subject(self, old: str, new: str):
        return access.rename_subject(self, old, new)

    # Returns DataFrame representing data object
    def get_data(self):
        return access.get_data(self)

    # Return list of all unique IDs in a DataFrame
    def get_id(self):
        return access.get_id(self)
    
    # Converts DataFrame from long to wide form
    def long_to_wide(self):
        return access.long_to_wide(self)

    # def chat(self, key):
    #     return access.chat(self, key)

    # Get hierarchy path for 'part-of-whole' figure function according to base level
    def _get_hierarchy_path(self, base_level):
        return visuals._get_hierarchy_path(self, base_level)

    # Generate Plotly Express sunburst Figure from DataFrame
    def generate_sunburst(self, type: int, id: str, base_level: str = 5):
        return visuals.generate_sunburst(self, type, id, base_level)

    # Generate Plotly Express treemap Figure from DataFrame
    def generate_treemap(self, type: int, id: str, base_level: str = 5):
        return visuals.generate_treemap(self, type, id, base_level)

    # Generate Plotly Express icicle Figure from DataFrame
    def generate_icicle(self, type: int, id: str, base_level: str = 5):
        return visuals.generate_icicle(self, type, id, base_level)

    # Generate Plotly Express bar graph Figure from DataFrame
    def generate_bar(self, type: int, level: int, id: list = None, 
            x: str = 'ID', y: str = 'Prop', log_y: bool = False):
        return visuals.generate_bar(self, type, level, id, x, y, log_y)
    
    # Return mean difference data for figure
    def _get_mean_diff(self, df):
        return visuals._get_mean_diff(self, df)

    # Generate mean difference between left and right hemispheres of brain
    def generate_mean_diff(self, type: int, level: int, color: str = 'ID', id: list = None):
        return visuals.generate_mean_diff(self, type, level, color, id)

    # Transform DataFrame for correlation matrix
    def _corr_transform(self, df):
        return visuals._corr_transform(self, df)

    # Generate correlation matrix Plotly heatmap
    def generate_corr_matrix(self, type: int, level: int, id: list = None):
        return visuals.generate_corr_matrix(self, type, level, id)
    
    # Append covariate data to subjects in dataset object
    def append_covariate_data(self, file: str, icv: bool = False, tbv: bool = False):
        return read.append_covariate_data(self, file, icv, tbv)
    
    # Normalize region volumes by normalizing factor (ICV, TBV, ICV+TBV) in covariate dataset
    def normalize_covariate_data(self, covariate_dataset, normalizing_factor: str):
        return access.normalize_covariate_data(self, covariate_dataset, normalizing_factor)
    
    # Run statsmodels Ordinary Least Squares regression on data object.
    def OLS(self, covariate_dataset, covariates: list, outcome: str, log: bool = False, residual_plot: bool = False):
        return analysis.OLS(self, covariate_dataset, covariates, outcome, log, residual_plot)
    
    # Run statsmodels Logit regression on data object.
    def Logit(self, covariate_dataset, covariates: list, outcome: str, log: bool = False, roc_plot: bool = False):
        return analysis.Logit(self, covariate_dataset, covariates, outcome, log, roc_plot)
    
    # def RandomForest(self, covariate_dataset, covariates: list, outcome: str):
    #     return analysis.RandomForest(self, covariate_dataset, covariates, outcome)

if __name__ == '__main__':
    print(__name__)