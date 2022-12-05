import os
import pandas as pd
import plotly_express as px

__all__ = ['read_file', 'import_data', 'get_id', 'append_hierarchy_cols',
            'rename_subject', 'long_to_wide', 'generate_sunburst', 'generate_treemap', 
            'generate_icicle', 'generate_bar', 'generate_mean_diff', 
            'generate_corr_matrix']

class Data:

    LEVEL_FILE = "multilevel_lookup_table.txt"

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

    #Retrieves list of text files from directory
    def get_files(self, path):
        file_list = os.listdir(path)
        file_list = [x for x in file_list if x.endswith('.txt')]

        if not path.endswith('/'):
            path = path + '/'
        file_list = [path + x for x in file_list]

        return file_list

    #Retrieve, clean-up, and return header from data file
    def get_header(self, f):
        file = open(f)
        content = file.readlines()
        header_line = content.index('Image\tObject\tVolume_mm3\tMin\tMax\tMean\tStd\t\n')

        head = content[header_line].split('\t')
        head.pop()

        return head

    #Retrieve first index/line of data
    def get_start_index(self, f):
        file = open(f)
        content = file.readlines()
        start_index = content.index('Type1-L1 Statistics\n')

        return start_index

    #Workaround to import first level label
    def type1_l1_exception(self, f, df):
        row = pd.DataFrame(columns=self.get_header(f))
        row.at[0, 'Image'] = "Type1-L1 Statistics"
        new = pd.concat([row, df])

        return new

    #Read level lookup table into dataframe
    def read_lookup_table(self, col):
        df = pd.read_csv(self.LEVEL_FILE, sep='\t', skiprows=1, index_col=False, 
            header=None, usecols=range(1, 11), names=col)

        return df

    #Assign type label according to index
    def get_type(self, i):
        if 0 < i < 9:
            return 1
        elif 9 < i < 29:
            return 1
        elif 29 < i < 84:
            return 1
        elif 84 < i < 221:
            return 1
        elif 221 < i < 498:
            return 1
        elif 498 < i < 504:
            return 2
        elif 504 < i < 523:
            return 2
        elif 523 < i < 576:
            return 2
        elif 576 < i < 647:
            return 2
        elif i > 647:
            return 2

    #Assign level label according to index
    def get_level(self, i):
        if 0 < i < 9:
            return 1
        elif 9 < i < 29:
            return 2
        elif 29 < i < 84:
            return 3
        elif 84 < i < 221:
            return 4
        elif 221 < i < 498:
            return 5
        elif 498 < i < 504:
            return 1
        elif 504 < i < 523:
            return 2
        elif 523 < i < 576:
            return 3
        elif 576 < i < 647:
            return 4
        elif i > 647:
            return 5

    #Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
    def level5_lookup(self, df, dfl):
        #Iterate over data
        for i, r1 in df.iterrows():
            #Check for type and level
            if (r1['Type'] == 1):
                if (r1['Level'] == 5):
                    #Append level directly from object
                    df.loc[i, 'Level5'] = df.loc[i, 'Object']
                    #Iterate over lookup table
                    for j, r2 in dfl.iterrows():
                        #Cross reference lookup table and populate rows in accordance
                        if (r2['Type1-L5 Statistics'] == df.loc[i, 'Object']):
                            df.loc[i, 'Level4'] = r2['Type1-L4 Statistics']
                            df.loc[i, 'Level3'] = r2['Type1-L3 Statistics']
                            df.loc[i, 'Level2'] = r2['Type1-L2 Statistics']
                            df.loc[i, 'Level1'] = r2['Type1-L1 Statistics']
            #Check for type and level
            if (r1['Type'] == 2):
                if (r1['Level'] == 5):
                    #Append level directly from object
                    df.loc[i, 'Level5'] = df.loc[i, 'Object']
                    #Iterate over lookup table
                    for j, r2 in dfl.iterrows():
                        #Cross reference lookup table and populate rows in accordance
                        if (r2['Type2-L5 Statistics'] == df.loc[i, 'Object']):
                            df.loc[i, 'Level4'] = r2['Type2-L4 Statistics']
                            df.loc[i, 'Level3'] = r2['Type2-L3 Statistics']
                            df.loc[i, 'Level2'] = r2['Type2-L2 Statistics']
                            df.loc[i, 'Level1'] = r2['Type2-L1 Statistics']

    #Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
    def level4_lookup(self, df, dfl):
        #Iterate over data
        for i, r1 in df.iterrows():
            #Check for type and level
            if (r1['Type'] == 1):
                if (r1['Level'] == 4):
                    #Append level directly from object
                    df.loc[i, 'Level4'] = df.loc[i, 'Object']
                    #Iterate over lookup table
                    for j, r2 in dfl.iterrows():
                        #Cross reference lookup table and populate rows in accordance
                        if (r2['Type1-L4 Statistics'] == df.loc[i, 'Object']):
                            df.loc[i, 'Level3'] = r2['Type1-L3 Statistics']
                            df.loc[i, 'Level2'] = r2['Type1-L2 Statistics']
                            df.loc[i, 'Level1'] = r2['Type1-L1 Statistics']
            #Check for type and level
            if (r1['Type'] == 2):
                if (r1['Level'] == 4):
                    #Append level directly from object
                    df.loc[i, 'Level4'] = df.loc[i, 'Object']
                    #Iterate over lookup table
                    for j, r2 in dfl.iterrows():
                        #Cross reference lookup table and populate rows in accordance
                        if (r2['Type2-L4 Statistics'] == df.loc[i, 'Object']):
                            df.loc[i, 'Level3'] = r2['Type2-L3 Statistics']
                            df.loc[i, 'Level2'] = r2['Type2-L2 Statistics']
                            df.loc[i, 'Level1'] = r2['Type2-L1 Statistics']

    #Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
    def level3_lookup(self, df, dfl):
        #Iterate over data
        for i, r1 in df.iterrows():
            #Check for type and level
            if (r1['Type'] == 1):
                if (r1['Level'] == 3):
                    #Append level directly from object
                    df.loc[i, 'Level3'] = df.loc[i, 'Object']
                    #Iterate over lookup table
                    for j, r2 in dfl.iterrows():
                        #Cross reference lookup table and populate rows in accordance
                        if (r2['Type1-L3 Statistics'] == df.loc[i, 'Object']):
                            df.loc[i, 'Level2'] = r2['Type1-L2 Statistics']
                            df.loc[i, 'Level1'] = r2['Type1-L1 Statistics']
            #Check for type and level
            if (r1['Type'] == 2):
                if (r1['Level'] == 3):
                    #Append level directly from object
                    df.loc[i, 'Level3'] = df.loc[i, 'Object']
                    #Iterate over lookup table
                    for j, r2 in dfl.iterrows():
                        #Cross reference lookup table and populate rows in accordance
                        if (r2['Type2-L3 Statistics'] == df.loc[i, 'Object']):
                            df.loc[i, 'Level2'] = r2['Type2-L2 Statistics']
                            df.loc[i, 'Level1'] = r2['Type2-L1 Statistics']

    #Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
    def level2_lookup(self, df, dfl):
        #Iterate over data
        for i, r1 in df.iterrows():
            #Check for type and level
            if (r1['Type'] == 1):
                if (r1['Level'] == 2):
                    #Append level directly from object
                    df.loc[i, 'Level2'] = df.loc[i, 'Object']
                    #Iterate over lookup table
                    for j, r2 in dfl.iterrows():
                        #Cross reference lookup table and populate rows in accordance
                        if (r2['Type1-L2 Statistics'] == df.loc[i, 'Object']):
                            df.loc[i, 'Level1'] = r2['Type1-L1 Statistics']
            #Check for type and level
            if (r1['Type'] == 2):
                if (r1['Level'] == 2):
                    #Append level directly from object
                    df.loc[i, 'Level2'] = df.loc[i, 'Object']
                    #Iterate over lookup table
                    for j, r2 in dfl.iterrows():
                        #Cross reference lookup table and populate rows in accordance
                        if (r2['Type2-L2 Statistics'] == df.loc[i, 'Object']):
                            df.loc[i, 'Level1'] = r2['Type2-L1 Statistics']

    #Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
    def level1_lookup(self, df):
        #Iterate over data
        for i, r1 in df.iterrows():
            #Check for type and level
            if (r1['Type'] == 1):
                if (r1['Level'] == 1):
                    #Append level directly from object
                    df.loc[i, 'Level1'] = df.loc[i, 'Object']
            #Check for type and level
            if (r1['Type'] == 2):
                if (r1['Level'] == 1):
                    #Append level directly from object
                    df.loc[i, 'Level1'] = df.loc[i, 'Object']

    #Append base region and hemisphere columns
    def append_region_cols(self, df: pd.DataFrame):
        #Iterate over dataframe
        for i, row in df.iterrows():
            #Parse object and populate based on relevant region and hemisphere
            if (row['Object'].endswith('_L') or '_L_' in row['Object']):
                base = row['Object'][:-2]
                base = base.replace('_L_', '_')
                df.loc[i, 'BaseRegion'] = base
                df.loc[i, 'Hemisphere'] = 'Left'
            elif (row['Object'].endswith('_R') or '_R_' in row['Object']):
                base = row['Object'][:-2]
                base = base.replace('_R_', '_')
                df.loc[i, 'BaseRegion'] = base
                df.loc[i, 'Hemisphere'] = 'Right'
            else:
                df.loc[i, 'BaseRegion'] = row['Object']
                df.loc[i, 'Hemisphere'] = 'Central'
        return

    #Appends hierarchical level 1-5 and ICV columns
    def append_hierarchy_cols(self, df: pd.DataFrame, base_level: int):
        #Populate necessary columns based on base level
        if (base_level == 5):
            self.level5_lookup(df, self.read_lookup_table(self.LEVEL_COLUMNS))
            self.level4_lookup(df, self.read_lookup_table(self.LEVEL_COLUMNS))
            self.level3_lookup(df, self.read_lookup_table(self.LEVEL_COLUMNS))
            self.level2_lookup(df, self.read_lookup_table(self.LEVEL_COLUMNS))
            self.level1_lookup(df)
            df['ICV'] = "ICV"
        elif (base_level == 4):
            self.level4_lookup(df, self.read_lookup_table(self.LEVEL_COLUMNS))
            self.level3_lookup(df, self.read_lookup_table(self.LEVEL_COLUMNS))
            self.level2_lookup(df, self.read_lookup_table(self.LEVEL_COLUMNS))
            self.level1_lookup(df)
            df['ICV'] = "ICV"
            return
        elif (base_level == 3):
            self.level3_lookup(df, self.read_lookup_table(self.LEVEL_COLUMNS))
            self.level2_lookup(df, self.read_lookup_table(self.LEVEL_COLUMNS))
            self.level1_lookup(df)
            df['ICV'] = "ICV"
            return
        elif (base_level == 2):
            self.level2_lookup(df, self.read_lookup_table(self.LEVEL_COLUMNS))
            self.level1_lookup(df)
            df['ICV'] = "ICV"
            return
        elif (base_level == 1):
            self.level1_lookup(df)
            df['ICV'] = "ICV"
            return
        else:
            #Invalid base level error
            print(str(self.append_hierarchy_cols.__name__) + ": Invalid base_level: " 
                    + "\'" + str(base_level) + "\'" + ", valid base_level(s) include: 1-5")
            return

        return df

    #Import and read data file into dataframe
    def read_file(self, file: str): 
        #Read text file and store in dataframe
        df = pd.read_csv(file, sep='\t', skiprows=self.get_start_index(file)+1, 
            index_col=False, header=None, names=self.get_header(file))
        df.index += 1 #Shifts index up by 1 to make room for first level label

        #Removes level labels from dataframe
        df = df[df['Image'].str.contains('Type')==False]

        #Appends 'Type' column
        df['Type'] = df.index.map(self.get_type)

        #Appends 'Level' column
        df['Level'] = df.index.map(self.get_level)

        #Appends region and hemisphere detail columns
        self.append_region_cols(df)

        #Appends 'Prop' column
        tot_vol = df.loc[1:8, 'Volume_mm3'].sum()
        Prop = df.loc[:, 'Volume_mm3'] / tot_vol
        df['Prop'] = Prop

        #Rename 'Image' column to 'ID' and 'Volume_mm3' column to 'Volume'
        df.rename(columns={'Image':'ID', 'Volume_mm3':'Volume'}, inplace=True)

        #Drop unnecessary columns
        df = df.drop(columns=['Min', 'Max', 'Mean', 'Std'])

        return df

    #Returns dataframe of type/level labels with preserved indices
    def get_type_labels(self, file):
        #Read text file and store in dataframe
        df = pd.read_csv(file, sep='\t', skiprows=self.get_start_index(file)+1, 
            index_col=False, header=None, names=self.get_header(file))
        df.index += 1 #Shifts index up by 1 to make room for first level label
        
        #Isolates level labels with preserved indices, adds first level label
        df = df[df['Image'].str.match('Type')]
        df = self.type1_l1_exception(file, df)

        #Rename column to more suitable 'Labels'
        df = df['Image'].rename('Labels')

        return df

    #Combines dataframes from a list of files
    def import_data(self, path: str, id_type: str = 'numeric', id_list: list = None):
        files = self.get_files(path)
        files_found = files.copy()
        files_found = [x.replace(path + '/', '') for x in files_found]
        print(str(self.import_data.__name__) + ": Data files found \n" + str(files_found))
        print(str(self.import_data.__name__) + ": Importing...")
        df = pd.DataFrame()
        #Iterate over list of files, read in files, and concatenate into a dataframe
        for f in files:
            df2 = self.read_file(f)
            #Populate ID column based on id_type (custom, filename, numeric)
            if (id_type == 'custom'):
                if (id_list is None):
                    print(str(self.import_data.__name__) + ": id_type \'custom\' requires id_list")
                    return
                df2['ID'] = str(id_list[files.index(f)])
            elif (id_type == 'filename'):
                df2['ID'] = str(files_found[files.index(f)].replace('.txt', ''))
            elif (id_type == 'numeric'):
                df2['ID'] = str(files.index(f))
            else:
                #Invalid ID error
                print(str(self.import_data.__name__) + ": Invalid id_type: " 
                    + "\'" + str(id_type) + "\'" + ", valid id_type(s) include: numeric, filename, custom")
                return
            df = pd.concat([df, df2], ignore_index=True)
        return df

    #Renames specific subject ID
    def rename_subject(self, old: str, new: str):
        if (old not in self.df['ID']):
            #Invalid ID error
            print(str(self.rename_subject.__name__) + ": Invalid old ID: " + "\'" + str(old) + "\'")
        df_id = self.df['ID'].replace(old, new)
        self.df['ID'] = df_id
        return self.df

    def get_data(self):
        return self.df

    #Return list of all unique IDs in a dataframe
    def get_id(self):
        ids = self.df['ID'].unique()
        return ids

    #Converts dataframe from long to wide form
    def long_to_wide(self):

        df = self.df.copy()
        print(str(self.long_to_wide.__name__) + ": Converting...")

        #Eliminate duplicates by appending type and level data to object strings
        for i, row in df.iterrows():
            df.loc[i, 'Object'] = row['Object'] + '_Type' + str(row['Type']) + '_L' + str(row['Level'])
        
        #Retain necessary columns
        df = df.filter(['ID', 'Object', 'Volume'])

        #Filter and pivot by each ID to avoid duplicates
        df_wide = pd.DataFrame()
        #Get list of IDs to iterate over
        ids = self.get_id()
        for id in ids:
            df_id = df.loc[df['ID'] == id]
            #Drop second 'BasalForebrain_L/R_Type1_L5' row
            df_id = df_id.drop_duplicates(subset=['Object'], keep='first')
            df_id = df_id.pivot(index='ID', columns='Object', values='Volume')
            df_wide = pd.concat([df_wide, df_id])

        return df_wide

    #Get hiearchy path for 'part-of-whole' figure function according to base level
    def get_hierarchy_path(self, base_level):
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

    #Generate Plotly Express sunburst model from dataframe
    def generate_sunburst(self, type: int, id: str, base_level: str = 5):
        #Check valid ID
        if (id not in self.df['ID'].unique()):
            print(str(self.generate_sunburst.__name__) + ": Invalid ID: " + "\'" + str(id) + "\'")
            return

        #Check valid base_level
        if (not 0 < base_level <= 5):
            print(str(self.generate_sunburst.__name__) + ": Invalid base_level: " 
                    + "\'" + str(base_level) + "\'" + ", valid base level(s) include: 1-5")
            return

        #Invalid type error
        if (type not in [1, 2]):
            print(str(self.generate_sunburst.__name__) + ": Invalid type: " + 
                    "\'" + str(type) + "\'" + ", valid type(s) include: 1, 2")
            return

        print(str(self.generate_sunburst.__name__) + ": Generating...")

        #Sunburst title
        TITLE = (str(self.generate_sunburst.__name__) + ": ID: " + str(id) + ", Type: " + 
                str(type) + ", Base Level: " + str(base_level))

        #Filter type rows, get path according to base_level, 
        #and drop NaN/level columns rows for square data
        df_type = self.df[self.df['Type'] == type]
        df_type = df_type[df_type['ID'] == id]
        path = self.get_hierarchy_path(base_level)
        #Append hierarchy columns for sunburst
        self.append_hierarchy_cols(df_type, base_level=base_level)
        #df_type1 = drop_sunburst_col(df_type1, base_level)
        df_type = df_type.dropna()

        #Create and show Plotly Express sunburst figure
        fig = px.sunburst(df_type, path=path, values='Prop', title=TITLE)
        fig.show()

    def generate_treemap(self, type: int, id: str, base_level: str = 5):
        #Check valid ID
        if (id not in self.df['ID'].unique()):
            print(str(self.generate_treemap.__name__) + ": Invalid ID: " + "\'" + str(id) + "\'")
            return

        #Check valid base_level
        if (not 0 < base_level <= 5):
            print(str(self.generate_treemap.__name__) + ": Invalid base_level: " 
                    + "\'" + str(base_level) + "\'" + ", valid base level(s) include: 1-5")
            return
        
        #Invalid type error
        if (type not in [1, 2]):
            print(str(self.generate_treemap.__name__) + ": Invalid type: " + 
                    "\'" + str(type) + "\'" + ", valid type(s) include: 1, 2")
            return

        print(str(self.generate_treemap.__name__) + ": Generating...")

        #Treemap title
        TITLE = (str(self.generate_treemap.__name__) + ": ID: " + str(id) + ", Type: " + 
                str(type) + ", Base Level: " + str(base_level))

        #Filter type rows, get path according to base_level, 
        #and drop NaN/level columns rows for square data
        df_type = self.df[self.df['Type'] == type]
        df_type = df_type[df_type['ID'] == id]
        path = self.get_hierarchy_path(base_level)
        #Append hierarchy columns for sunburst
        self.append_hierarchy_cols(df_type, base_level=base_level)
        #df_type1 = drop_sunburst_col(df_type1, base_level)
        df_type = df_type.dropna()

        #Create and show Plotly Express sunburst figure
        fig = px.treemap(df_type, path=path, values='Prop', title=TITLE)
        fig.show()

    def generate_icicle(self, type: int, id: str, base_level: str = 5):
        #Check valid ID
        if (id not in self.df['ID'].unique()):
            print(str(self.generate_icicle.__name__) + ": Invalid ID: " + "\'" + str(id) + "\'")
            return

        #Check valid base_level
        if (not 0 < base_level <= 5):
            print(str(self.generate_icicle.__name__) + ": Invalid base_level: " 
                    + "\'" + str(base_level) + "\'" + ", valid base level(s) include: 1-5")
            return

        #Invalid type error
        if (type not in [1, 2]):
            print(str(self.generate_icicle.__name__) + ": Invalid type: " + 
                    "\'" + str(type) + "\'" + ", valid type(s) include: 1, 2")
            return

        print(str(self.generate_icicle.__name__) + ": Generating...")

        #Icicle title
        TITLE = (str(self.generate_icicle.__name__) + ": ID: " + str(id) + ", Type: " + 
                str(type) + ", Base Level: " + str(base_level))

        #Filter type rows, get path according to base_level, 
        #and drop NaN/level columns rows for square data
        df_type = self.df[self.df['Type'] == type]
        df_type = df_type[df_type['ID'] == id]
        path = self.get_hierarchy_path(base_level)
        #Append hierarchy columns for sunburst
        self.append_hierarchy_cols(df_type, base_level=base_level)
        #df_type1 = drop_sunburst_col(df_type1, base_level)
        df_type = df_type.dropna()

        #Create and show Plotly Express sunburst figure
        fig = px.icicle(df_type, path=path, values='Prop', title=TITLE)
        fig.show()

    #Generate Plotly Express bar graph from dataframe
    def generate_bar(self, type: int, level: int, id: list = None, 
            x: str = 'ID', y: str = 'Prop', log_y: bool = False):

        #Check valid ID if ID argument passed
        if (id is not None and id in id not in self.df['ID'].unique()):
            print(str(self.generate_bar.__name__) + ": Invalid ID: " + "\'" + str(id) + "\'")
            return

        #Invalid type error
        if (type not in [1, 2]):
            print(str(self.generate_bar.__name__) + ": Invalid type: " + 
                    "\'" + str(type) + "\'" + ", valid type(s) include: 1, 2")
            #Invalid level error
            if (level not in [1, 2, 3, 4, 5]):
                print(str(self.generate_bar.__name__) + ": Invalid level: " + 
                    "\'" + str(level) + "\'" + ", valid level(s) include: 1-5")
            return

        print(str(self.generate_bar.__name__) + ": Generating...")

        #Bar title if ID argument is/is not passed
        if (id is None):
            TITLE = str(self.generate_bar.__name__) + ": Type: " + str(type) + ", Level: " + str(level)
        else:
            TITLE = (str(self.generate_bar.__name__) + ": ID: " + str(id) + ", Type: " + 
                    str(type) + ", Level: " + str(level))

        #Logarithmic title label
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
        figlevel.show()
        
    def get_mean_diff(self, df):

        df_left = df[df['Hemisphere'] == 'Left']
        df_right = df[df['Hemisphere'] == 'Right']
        df_left.reset_index(inplace=True)
        df_right.reset_index(inplace=True)
        df_left = df_left.filter(['ID', 'Object', 'Volume'])
        df_right = df_right.filter(['ID', 'Object', 'Volume'])

        df_diff = df_left.copy()
        df_diff.loc[:, 'Difference'] = df_left['Volume'] - df_right['Volume']
        df_diff = df_diff.drop(columns=['Volume'])
        #df_diff.rename(columns={'Volume':'Difference'}, inplace=True)
        df_mean = df_left.copy()
        df_mean.loc[:, 'Mean'] = (df_left['Volume'] + df_right['Volume']) / 2
        df_mean = df_mean.drop(columns=['ID', 'Object', 'Volume'])
        #df_mean.rename(columns={'Volume':'Mean'}, inplace=True)

        df_mean_diff = pd.concat([df_diff, df_mean], axis=1)
        
        return df_mean_diff

    #Generate mean difference between left and right hemispheres of brain
    def generate_mean_diff(self, type: int, level: int, color: str = 'ID', id: list = None):
        #Check valid ID if ID argument passed
        if (id is not None and id in id not in self.df['ID'].unique()):
            print(str(self.generate_mean_diff.__name__) + ": Invalid ID: " + "\'" + str(id) + "\'")
            return

        #Check for valid color
        if not(color == 'ID' or color == 'Object'):
            #Invalid color error
            print(str(self.generate_mean_diff.__name__) + ": Invalid color: " + 
                    "\'" + str(color) + "\'" + ", valid color(s) include: ID, Object")
            return

        #Invalid type error
        if (type not in [1, 2]):
            print(str(self.generate_mean_diff.__name__) + ": Invalid type: " + 
                    "\'" + str(type) + "\'" + ", valid type(s) include: 1, 2")
            #Invalid level error
            if (level not in [1, 2, 3, 4, 5]):
                print(str(self.generate_mean_diff.__name__) + ": Invalid level: " + 
                    "\'" + str(level) + "\'" + ", valid level(s) include: 1-5")
            return

        print(str(self.generate_mean_diff.__name__) + ": Generating...")

        #Title if ID argument is/is not passed
        if (id is None):
            TITLE = str(self.generate_mean_diff.__name__) + ": Type: " + str(type) + ", Level: " + str(level)
        else:
            TITLE = str(self.generate_mean_diff.__name__) + ": ID: " + str(id) + ", Type: " + str(type) + ", Level: " + str(level)

        point_size = 10

        #Filter Type rows and ID
        df_type1 = self.df[self.df['Type'] == type]
            
        #Filter ID if ID argument passed
        if (id is not None):
            df_type = df_type[df_type['ID'].isin(id)]
            
        #Filter level and generate Plotly scatter plot
        df_typelevel = df_type[df_type['Level'] == level]
        figlevel = px.scatter(self.get_mean_diff(df_typelevel), x='Mean', y='Difference', 
            color=color, title=TITLE, hover_data=['Object'], labels={'Mean':'Mean (mm\u00b3)', 
            'Difference':'Difference (mm\u00b3)'})
        figlevel.update_traces(marker={'size': point_size})
        figlevel.show()

    #Transform dataframe for correlation matrix
    def corr_transform(self, df):

        df = df.copy()
        #Filter and pivot dataframe from long to wide
        df = df.filter(['ID', 'Object', 'Volume'])
        df = df.pivot(index='ID', columns='Object', values='Volume')

        #Create corrariance matrix
        df_corr = df.corr()
        return df_corr

    def generate_corr_matrix(self, type: int, level: int, id: list = None):

        df = self.df.copy()

        #Check valid ID if ID argument passed
        if (id is not None and id in id not in df['ID'].unique()):
            print(str(self.generate_corr_matrix.__name__) + ": Invalid ID: " + "\'" + str(id) + "\'")
            return

        #Invalid type error
        if (type not in [1, 2]):
            print(str(self.generate_corr_matrix.__name__) + ": Invalid type: " + 
                    "\'" + str(type) + "\'" + ", valid type(s) include: 1, 2")
            #Invalid level error
            if (level not in [1, 2, 3, 4, 5]):
                print(str(self.generate_corr_matrix.__name__) + ": Invalid level: " + 
                    "\'" + str(level) + "\'" + ", valid level(s) include: 1-5")
            return

        print(str(self.generate_corr_matrix.__name__) + ": Generating...")
        
        #Title if ID argument is/is not passed
        if (id is None):
            TITLE = str(self.generate_corr_matrix.__name__) + ": Type: " + str(type) + ", Level: " + str(level)
        else:
            TITLE = str(self.generate_corr_matrix.__name__) + ": ID: " + str(id) + ", Type: " + str(type) + ", Level: " + str(level)

        #Filter Type rows and ID
        df_type = df[df['Type'] == type]
            
        #Filter ID if ID argument passed
        if (id is not None):
            df_type = df_type[df_type['ID'].isin(id)]
            
        #Filter level and generate Plotly heatmap
        df_typelevel = df_type[df_type['Level'] == level]

        df_typelevel_corr = self.corr_transform(df_typelevel)
        figlevel = px.imshow(df_typelevel_corr, title=TITLE)
        figlevel.update_xaxes(autorange='reversed')
        figlevel.show()


       
