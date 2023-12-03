import pandas as pd
import plotly_express as px

# Get hiearchy path for 'part-of-whole' figure function according to base level
def _get_hierarchy_path(self, base_level):
    if (base_level == 5):
        path = ['ICV', 'Level1', 'Level2', 'Level3', 'Level4', 'Level5']
    elif (base_level == 4):
        path = ['ICV', 'Level1', 'Level2', 'Level3', 'Level4']
    elif (base_level == 3):
        path = ['ICV', 'Level1', 'Level2', 'Level3']
    elif (base_level == 2):
        path = ['ICV', 'Level1', 'Level2']
    elif (base_level == 1):
        path = ['ICV', 'Level1']
    return path

# Generate Plotly Express sunburst model from dataframe
def generate_sunburst(self, type: int, id: str, base_level: str = 5):
    # Check valid ID
    if (id not in self.df['ID'].unique()):
        print(str(self.generate_sunburst.__name__) + ": Invalid ID: " + "\'" + str(id) + "\'")
        return

    # Check valid base_level
    if (not 0 < base_level <= 5):
        print(str(self.generate_sunburst.__name__) + ": Invalid base_level: " 
                + "\'" + str(base_level) + "\'" + ", valid base level(s) include: 1-5")
        return

    # Invalid type error
    if (type not in [1, 2]):
        print(str(self.generate_sunburst.__name__) + ": Invalid type: " + 
                "\'" + str(type) + "\'" + ", valid type(s) include: 1, 2")
        return

    print(str(self.generate_sunburst.__name__) + ": Generating...")

    # Sunburst title
    TITLE = (str(self.generate_sunburst.__name__) + ": ID: " + str(id) + ", Type: " + 
            str(type) + ", Base Level: " + str(base_level))

    # Filter type rows, get path according to base_level, 
    # and drop NaN/level columns rows for square data
    df_type = self.df[self.df['Type'] == type]
    df_type = df_type[df_type['ID'] == id]
    path = self._get_hierarchy_path(base_level)
    # Append hierarchy columns for sunburst
    self._append_hierarchy_cols(df_type, base_level=base_level)
    # df_type1 = drop_sunburst_col(df_type1, base_level)
    df_type = df_type.dropna()

    # Create and show Plotly Express sunburst figure
    fig = px.sunburst(df_type, path=path, values='Prop', title=TITLE)

    print(str(self.generate_sunburst.__name__) + ": Generation successful")
    fig.show()
    return fig

def generate_treemap(self, type: int, id: str, base_level: str = 5):
    # Check valid ID
    if (id not in self.df['ID'].unique()):
        print(str(self.generate_treemap.__name__) + ": Invalid ID: " + "\'" + str(id) + "\'")
        return

    # Check valid base_level
    if (not 0 < base_level <= 5):
        print(str(self.generate_treemap.__name__) + ": Invalid base_level: " 
                + "\'" + str(base_level) + "\'" + ", valid base level(s) include: 1-5")
        return
    
    # Invalid type error
    if (type not in [1, 2]):
        print(str(self.generate_treemap.__name__) + ": Invalid type: " + 
                "\'" + str(type) + "\'" + ", valid type(s) include: 1, 2")
        return

    print(str(self.generate_treemap.__name__) + ": Generating...")

    # Treemap title
    TITLE = (str(self.generate_treemap.__name__) + ": ID: " + str(id) + ", Type: " + 
            str(type) + ", Base Level: " + str(base_level))

    # Filter type rows, get path according to base_level, 
    # and drop NaN/level columns rows for square data
    df_type = self.df[self.df['Type'] == type]
    df_type = df_type[df_type['ID'] == id]
    path = self._get_hierarchy_path(base_level)
    # Append hierarchy columns for sunburst
    self._append_hierarchy_cols(df_type, base_level=base_level)
    # df_type1 = drop_sunburst_col(df_type1, base_level)
    df_type = df_type.dropna()

    # Create and show Plotly Express sunburst figure
    fig = px.treemap(df_type, path=path, values='Prop', title=TITLE)

    print(str(self.generate_treemap.__name__) + ": Generation succesful")
    fig.show()
    return fig

def generate_icicle(self, type: int, id: str, base_level: str = 5):
    # Check valid ID
    if (id not in self.df['ID'].unique()):
        print(str(self.generate_icicle.__name__) + ": Invalid ID: " + "\'" + str(id) + "\'")
        return

    # Check valid base_level
    if (not 0 < base_level <= 5):
        print(str(self.generate_icicle.__name__) + ": Invalid base_level: " 
                + "\'" + str(base_level) + "\'" + ", valid base level(s) include: 1-5")
        return

    # Invalid type error
    if (type not in [1, 2]):
        print(str(self.generate_icicle.__name__) + ": Invalid type: " + 
                "\'" + str(type) + "\'" + ", valid type(s) include: 1, 2")
        return

    print(str(self.generate_icicle.__name__) + ": Generating...")

    # Icicle title
    TITLE = (str(self.generate_icicle.__name__) + ": ID: " + str(id) + ", Type: " + 
            str(type) + ", Base Level: " + str(base_level))

    # Filter type rows, get path according to base_level, 
    # and drop NaN/level columns rows for square data
    df_type = self.df[self.df['Type'] == type]
    df_type = df_type[df_type['ID'] == id]
    path = self._get_hierarchy_path(base_level)
    # Append hierarchy columns for sunburst
    self._append_hierarchy_cols(df_type, base_level=base_level)
    # df_type1 = drop_sunburst_col(df_type1, base_level)
    df_type = df_type.dropna()

    # Create and show Plotly Express sunburst figure
    fig = px.icicle(df_type, path=path, values='Prop', title=TITLE)

    print(str(self.generate_icicle.__name__) + ": Generation successful")
    fig.show()
    return fig

# Generate Plotly Express bar graph from dataframe
def generate_bar(self, type: int, level: int, id: list = None, 
        x: str = 'ID', y: str = 'Prop', log_y: bool = False):

    # Check valid ID if ID argument passed
    if (id is not None and id in id not in self.df['ID'].unique()):
        print(str(self.generate_bar.__name__) + ": Invalid ID: " + "\'" + str(id) + "\'")
        return

    # Invalid type error
    if (type not in [1, 2]):
        print(str(self.generate_bar.__name__) + ": Invalid type: " + 
                "\'" + str(type) + "\'" + ", valid type(s) include: 1, 2")
        # Invalid level error
        if (level not in [1, 2, 3, 4, 5]):
            print(str(self.generate_bar.__name__) + ": Invalid level: " + 
                "\'" + str(level) + "\'" + ", valid level(s) include: 1-5")
        return

    print(str(self.generate_bar.__name__) + ": Generating...")

    # Bar title if ID argument is/is not passed
    if (id is None):
        TITLE = str(self.generate_bar.__name__) + ": Type: " + str(type) + ", Level: " + str(level)
    else:
        TITLE = (str(self.generate_bar.__name__) + ": ID: " + str(id) + ", Type: " + 
                str(type) + ", Level: " + str(level))

    # Logarithmic title label
    if (log_y):
        TITLE = TITLE + " (log)"

    df_type = self.df[self.df['Type'] == type]
    if (id is not None):
        df_type = df_type[df_type['ID'].isin(id)]
    
    df_typelevel = df_type[df_type['Level'] == level]
    figlevel =  px.bar(df_typelevel, x = x, y = y,
        color='Object', title=TITLE, log_y=log_y)
    if (y == 'Volume'):
            figlevel.update_layout(yaxis_title='Volume (mm\u00b3)')

    print(str(self.generate_bar.__name__) + ": Generation succesful")
    figlevel.show()
    return figlevel
    
def _get_mean_diff(self, df):

    df_left = df[df['Hemisphere'] == 'Left']
    df_right = df[df['Hemisphere'] == 'Right']
    df_left.reset_index(inplace=True)
    df_right.reset_index(inplace=True)
    df_left = df_left.filter(['ID', 'Object', 'Volume'])
    df_right = df_right.filter(['ID', 'Object', 'Volume'])

    df_diff = df_left.copy()
    df_diff.loc[:, 'Difference'] = df_left['Volume'] - df_right['Volume']
    df_diff = df_diff.drop(columns=['Volume'])
    # df_diff.rename(columns={'Volume':'Difference'}, inplace=True)
    df_mean = df_left.copy()
    df_mean.loc[:, 'Mean'] = (df_left['Volume'] + df_right['Volume']) / 2
    df_mean = df_mean.drop(columns=['ID', 'Object', 'Volume'])
    # df_mean.rename(columns={'Volume':'Mean'}, inplace=True)

    df_mean_diff = pd.concat([df_diff, df_mean], axis=1)
    
    return df_mean_diff

# Generate mean difference between left and right hemispheres of brain
def generate_mean_diff(self, type: int, level: int, color: str = 'ID', id: list = None):
    # Check valid ID if ID argument passed
    if (id is not None and id in id not in self.df['ID'].unique()):
        print(str(self.generate_mean_diff.__name__) + ": Invalid ID: " + "\'" + str(id) + "\'")
        return

    # Check for valid color
    if not(color == 'ID' or color == 'Object'):
        # Invalid color error
        print(str(self.generate_mean_diff.__name__) + ": Invalid color: " + 
                "\'" + str(color) + "\'" + ", valid color(s) include: ID, Object")
        return

    # Invalid type error
    if (type not in [1, 2]):
        print(str(self.generate_mean_diff.__name__) + ": Invalid type: " + 
                "\'" + str(type) + "\'" + ", valid type(s) include: 1, 2")
        # Invalid level error
        if (level not in [1, 2, 3, 4, 5]):
            print(str(self.generate_mean_diff.__name__) + ": Invalid level: " + 
                "\'" + str(level) + "\'" + ", valid level(s) include: 1-5")
        return

    print(str(self.generate_mean_diff.__name__) + ": Generating...")

    # Title if ID argument is/is not passed
    if (id is None):
        TITLE = str(self.generate_mean_diff.__name__) + ": Type: " + str(type) + ", Level: " + str(level)
    else:
        TITLE = str(self.generate_mean_diff.__name__) + ": ID: " + str(id) + ", Type: " + str(type) + ", Level: " + str(level)

    point_size = 10

    # Filter Type rows and ID
    df_type = self.df[self.df['Type'] == type]
        
    # Filter ID if ID argument passed
    if (id is not None):
        df_type = df_type[df_type['ID'].isin(id)]
        
    # Filter level and generate Plotly scatter plot
    df_typelevel = df_type[df_type['Level'] == level]
    figlevel = px.scatter(self._get_mean_diff(df_typelevel), x='Mean', y='Difference', 
        color=color, title=TITLE, hover_data=['Object'], labels={'Mean':'Mean (mm\u00b3)', 
        'Difference':'Difference (mm\u00b3)'})
    figlevel.update_traces(marker={'size': point_size})

    print(str(self.generate_mean_diff.__name__) + ": Generation successful")
    figlevel.show()
    return figlevel

# Transform dataframe for correlation matrix
def _corr_transform(self, df):

    df = df.copy()
    # Filter and pivot dataframe from long to wide
    df = df.filter(['ID', 'Object', 'Volume'])
    df = df.pivot(index='ID', columns='Object', values='Volume')

    # Create correlation matrix
    df_corr = df.corr()
    return df_corr

def generate_corr_matrix(self, type: int, level: int, id: list = None):

    df = self.df.copy()

    # Check valid ID if ID argument passed
    if (id is not None and id in id not in df['ID'].unique()):
        print(str(self.generate_corr_matrix.__name__) + ": Invalid ID: " + "\'" + str(id) + "\'")
        return

    # Invalid type error
    if (type not in [1, 2]):
        print(str(self.generate_corr_matrix.__name__) + ": Invalid type: " + 
                "\'" + str(type) + "\'" + ", valid type(s) include: 1, 2")
        # Invalid level error
        if (level not in [1, 2, 3, 4, 5]):
            print(str(self.generate_corr_matrix.__name__) + ": Invalid level: " + 
                "\'" + str(level) + "\'" + ", valid level(s) include: 1-5")
        return

    print(str(self.generate_corr_matrix.__name__) + ": Generating...")
    
    # Title if ID argument is/is not passed
    if (id is None):
        TITLE = str(self.generate_corr_matrix.__name__) + ": Type: " + str(type) + ", Level: " + str(level)
    else:
        TITLE = str(self.generate_corr_matrix.__name__) + ": ID: " + str(id) + ", Type: " + str(type) + ", Level: " + str(level)

    # Filter Type rows and ID
    df_type = df[df['Type'] == type]
        
    # Filter ID if ID argument passed
    if (id is not None):
        df_type = df_type[df_type['ID'].isin(id)]
        
    # Filter level and generate Plotly heatmap
    df_typelevel = df_type[df_type['Level'] == level]

    df_typelevel_corr = self._corr_transform(df_typelevel)
    figlevel = px.imshow(df_typelevel_corr, title=TITLE)
    figlevel.update_xaxes(autorange='reversed')

    print(str(self.generate_corr_matrix.__name__) + ": Generation successful")
    figlevel.show()
    return figlevel

if __name__ == '__main__':
    print(__name__)