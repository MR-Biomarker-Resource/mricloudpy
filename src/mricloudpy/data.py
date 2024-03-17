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
    id_type : str, {'numeric', 'filename', 'custom'}, default = 'numeric'
        Type of subject ID formatting
    id_list : list, default = None
        List of custom subject IDs
    df : DataFrame
        DataFrame generated from path

    Methods
    -------
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
        Generate a Plotly Express bar graph Figure.
    generate_mean_diff(type, level, color='ID', id=None)
        Generate a Plotly Express mean difference plot Figure.
    generate_corr_matrix(type, level, id=None)
        Generate a Plotly Express heatmap Figure of a correlation matrix.
    append_covariate_data(path, icv=False, tbv=False)
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
        """
        Constructs data object.

        Parameters
        ----------
            path : str
                Path to MRICloud data text file
            id_type : str, {'numeric', 'filename', 'custom'}, default='numeric' 
                Type of subject ID formatting
            id_list : list
                List of custom subject IDs
            df : DataFrame
                DataFrame generated from path
        """ 
        self.path = path
        self.id_type = id_type
        self.id_list = id_list
        self.df = self._import_data(path, id_type, id_list)
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
    def _import_data(self, path: str, id_type: str = 'numeric', id_list: list = None):
        return read._import_data(self, path, id_type, id_list)

    def rename_subject(self, old: str, new: str):
        """
        Rename a specific subject ID.

        Parameters
        ----------
        old : str
            Old subject name to be replaced
        new : str
            New subject name

        Returns
        -------
        DataFrame
        """
        return access.rename_subject(self, old, new)

    def get_data(self):
        """
        Retrieve DataFrame of a given data object.

        Parameters
        ----------
        None

        Returns
        -------
        DataFrame
        """
        return access.get_data(self)

    def get_id(self):
        """
        Retrieve list of unique subject IDs.

        Parameters
        ----------
        None

        Returns
        -------
        Series
        """
        return access.get_id(self)
    
    def long_to_wide(self):
        """
        Convert default long form data to a wide format.

        Parameters
        ----------
        None

        Returns
        -------
        DataFrame
        """
        return access.long_to_wide(self)

    # def chat(self, key):
    #     return access.chat(self, key)

    # Get hierarchy path for 'part-of-whole' figure function according to base level
    def _get_hierarchy_path(self, base_level):
        return visuals._get_hierarchy_path(self, base_level)

    def generate_sunburst(self, type: int, id: str, base_level: str = 5):
        """
        Generate a Plotly Express sunburst Figure model.

        Parameters
        ----------
        type : int, {1, 2}
            Type of hierarchical view
        id : str
            Subject ID
        base_level : int, {1, 2, 3, 4, 5}, default = 5
            Lowest hierarchical level to include

        Returns
        -------
        plotly.graph_objects.Figure
        """
        return visuals.generate_sunburst(self, type, id, base_level)

    def generate_treemap(self, type: int, id: str, base_level: str = 5):
        """
        Generate a Plotly Express treemap Figure model.

        Parameters
        ----------
        type : int, {1, 2}
            Type of hierarchical view
        id : str
            Subject ID
        base_level : int, {1, 2, 3, 4, 5}, default = 5
            Lowest hierarchical level to include

        Returns
        -------
        plotly.graph_objects.Figure
        """
        return visuals.generate_treemap(self, type, id, base_level)

    def generate_icicle(self, type: int, id: str, base_level: str = 5):
        """
        Generate a Plotly Express icicle Figure model.

        Parameters
        ----------
        type : int, {1, 2}
            Type of hierarchical view
        id : str
            Subject ID
        base_level : int, {1, 2, 3, 4, 5}, default = 5
            Lowest hierarchical level to include

        Returns
        -------
        plotly.graph_objects.Figure
        """
        return visuals.generate_icicle(self, type, id, base_level)

    def generate_bar(self, type: int, level: int, id: list = None, 
            x: str = 'ID', y: str = 'Prop', log_y: bool = False):
        """
        Generate a Plotly Express bar graph Figure.

        Parameters
        ----------
        type : int, {1, 2}
            Type of hierarchical view
        level : int, {1, 2, 3, 4, 5}
            Hierarchical level of interest
        id : list, default = None
            Subjects of interest
        x : str, {'ID', 'Object'}, default = 'ID'
            Independent variable
        y : str, {'Prop', 'Volume'}, default = 'Prop'
            Dependent variable
        log_y : bool, default = False
            Logarithm of dependent variable

        Returns
        -------
        plotly.graph_objects.Figure
        """
        return visuals.generate_bar(self, type, level, id, x, y, log_y)
    
    # Return mean difference data for figure
    def _get_mean_diff(self, df):
        return visuals._get_mean_diff(self, df)

    def generate_mean_diff(self, type: int, level: int, color: str = 'ID', id: list = None):
        """
        Generate a Plotly Express mean difference plot Figure.

        Parameters
        ----------
        type : int, {1, 2}
            Type of hierarchical view
        level : int, {1, 2, 3, 4, 5}
            Hierarchical level of interest
        color : str, {'ID', 'Object'}, default = 'ID'
            Variable to organize data by color
        id : list, default = None
            Subjects of interest

        Returns
        -------
        plotly.graph_objects.Figure
        """
        return visuals.generate_mean_diff(self, type, level, color, id)

    # Transform DataFrame for correlation matrix
    def _corr_transform(self, df):
        return visuals._corr_transform(self, df)

    def generate_corr_matrix(self, type: int, level: int, id: list = None):
        """
        Generate a Plotly Express heatmap Figure of a correlation matrix.

        Parameters
        ----------
        type : int, {1, 2}
            Type of hierarchical view
        level : int, {1, 2, 3, 4, 5}
            Hierarchical level of interest
        id : list, default = None
            Subjects of interest

        Returns
        -------
        plotly.graph_objects.Figure
        """
        return visuals.generate_corr_matrix(self, type, level, id)
    
    def append_covariate_data(self, path: str, icv: bool = False, tbv: bool = False):
        """
        Append covariate dataset to data object.

        Parameters
        ----------
        path : str
            Path to covariate dataset file
        icv : bool, default = False
            Append intracranial volume to covariate dataset
        tbv : bool, default = False
            Append total brain volume to covariate dataset

        Returns
        -------
        DataFrame
        """
        return read.append_covariate_data(self, path, icv, tbv)
    
    def normalize_covariate_data(self, covariate_dataset, normalizing_factor: str):
        """
        Normalize covariate data in data object by ICV, TBV, or ICV + TBV.

        Parameters
        ----------
        covariate_dataset : DataFrame
            Covariate dataset to be normalized
        normalizing_factor : str, {'icv, tbv, icv_tbv'}
            Variable to normalize region volumes by

        Returns
        -------
        DataFrame
        """
        return access.normalize_covariate_data(self, covariate_dataset, normalizing_factor)
    
    def OLS(self, covariate_dataset, covariates: list, outcome: str, log: bool = False, 
            residual_plot: bool = False):
        """
        Run statsmodels Ordinary Least Squares regression on data object.

        Parameters
        ----------
        covariate_dataset : DataFrame
            Dataset containing the covariates and outcome
        covariates : list
            Covariates to include in analysis (x, independent covariates)
        outcome : str
            Outcome of interest (y, dependent covariate)
        log : bool, default = False
            Logaritm of covariates   
        residual_plot : bool, default = False
            Return a residual plot of analysis results as Plotly Figure

        Returns
        -------
        statsmodels.regression.linear_model.RegressionResultsWrapper.summary()
        plotly.graph_objects.Figure
        """
        return analysis.OLS(self, covariate_dataset, covariates, outcome, log, residual_plot)
    
    def Logit(self, covariate_dataset, covariates: list, outcome: str, log: bool = False, 
              roc_plot: bool = False):
        """
        Run statsmodels Logit regression on data object.

        Parameters
        ----------
        covariate_dataset : DataFrame
            Dataset containing the covariates and outcome
        covariates : list
            Covariates to include in analysis (x, independent covariates)
        outcome : str
            Outcome of interest (y, dependent covariate)
        log : bool, default = False
            Logaritm of covariates   
        roc_plot : bool, default = False
            Return an ROC curve plot of analysis results as Plotly Figure

        Returns
        -------
        RegressionResults.summary()
        plotly.graph_objects.Figure
        """
        return analysis.Logit(self, covariate_dataset, covariates, outcome, log, roc_plot)
    
    def RandomForest(self, covariate_dataset, covariates: list, outcome: str, log: bool = False, 
                     n_estimators: int = 200, random_state: int = 42, importance_plot: bool = False):
        """
        Run statsmodels Random Forest classifier on data object.

        Parameters
        ----------
        covariate_dataset : DataFrame
            Dataset containing the covariates and outcome
        covariates : list
            Covariates to include in analysis (x, independent covariates)
        outcome : str
            Outcome of interest (y, dependent covariate)
        log : bool, default = False
            Logaritm of covariates
        n_estimators : int, default = 200
            Number of decision trees
        random_state : int, default = 42
            Control bootstrapping randomness 
        importance_plot : bool, default = False
            Return a feature importance plot of analysis results as Plotly Figure

        Returns
        -------
        sklearn.ensemble.RandomForestClassifier
        numpy.ndarray
        plotly.graph_objects.Figure
        """
        return analysis.RandomForest(self, covariate_dataset, covariates, outcome, log, 
                                     n_estimators, random_state, importance_plot)

if __name__ == '__main__':
    print(__name__)