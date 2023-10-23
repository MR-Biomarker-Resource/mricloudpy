import os
import pandas as pd

# Retrieves list of text files from directory
def get_files(self, path):
    file_list = os.listdir(path)
    file_list = [x for x in file_list if x.endswith('.txt')]

    if not path.endswith('/'):
        path = path + '/'
    file_list = [path + x for x in file_list]

    return file_list

# Retrieve, clean-up, and return header from data file
def get_header(self, f):
    file = open(f)
    content = file.readlines()
    header_line = content.index('Image\tObject\tVolume_mm3\tMin\tMax\tMean\tStd\t\n')

    head = content[header_line].split('\t')
    head.pop()

    return head

# Retrieve first index/line of data
def get_start_index(self, f):
    file = open(f)
    content = file.readlines()
    start_index = content.index('Type1-L1 Statistics\n')

    return start_index

# Workaround to import first level label
def type1_l1_exception(self, f, df):
    row = pd.DataFrame(columns=self.get_header(f))
    row.at[0, 'Image'] = "Type1-L1 Statistics"
    new = pd.concat([row, df])

    return new

# Read level lookup table into dataframe
def read_lookup_table(self, col):
    df = pd.read_csv(self.LEVEL_FILE, sep='\t', skiprows=1, index_col=False, 
        header=None, usecols=range(1, 11), names=col)

    return df

# Assign type label according to index
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

# Assign level label according to index
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

# Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
def level5_lookup(self, df, dfl):
    # Iterate over data
    for i, r1 in df.iterrows():
        # Check for type and level
        if (r1['Type'] == 1):
            if (r1['Level'] == 5):
                # Append level directly from object
                df.loc[i, 'Level5'] = df.loc[i, 'Object']
                # Iterate over lookup table
                for j, r2 in dfl.iterrows():
                    # Cross reference lookup table and populate rows in accordance
                    if (r2['Type1-L5 Statistics'] == df.loc[i, 'Object']):
                        df.loc[i, 'Level4'] = r2['Type1-L4 Statistics']
                        df.loc[i, 'Level3'] = r2['Type1-L3 Statistics']
                        df.loc[i, 'Level2'] = r2['Type1-L2 Statistics']
                        df.loc[i, 'Level1'] = r2['Type1-L1 Statistics']
        # Check for type and level
        if (r1['Type'] == 2):
            if (r1['Level'] == 5):
                # Append level directly from object
                df.loc[i, 'Level5'] = df.loc[i, 'Object']
                # Iterate over lookup table
                for j, r2 in dfl.iterrows():
                    # Cross reference lookup table and populate rows in accordance
                    if (r2['Type2-L5 Statistics'] == df.loc[i, 'Object']):
                        df.loc[i, 'Level4'] = r2['Type2-L4 Statistics']
                        df.loc[i, 'Level3'] = r2['Type2-L3 Statistics']
                        df.loc[i, 'Level2'] = r2['Type2-L2 Statistics']
                        df.loc[i, 'Level1'] = r2['Type2-L1 Statistics']

# Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
def level4_lookup(self, df, dfl):
    # Iterate over data
    for i, r1 in df.iterrows():
        # Check for type and level
        if (r1['Type'] == 1):
            if (r1['Level'] == 4):
                # Append level directly from object
                df.loc[i, 'Level4'] = df.loc[i, 'Object']
                # Iterate over lookup table
                for j, r2 in dfl.iterrows():
                    # Cross reference lookup table and populate rows in accordance
                    if (r2['Type1-L4 Statistics'] == df.loc[i, 'Object']):
                        df.loc[i, 'Level3'] = r2['Type1-L3 Statistics']
                        df.loc[i, 'Level2'] = r2['Type1-L2 Statistics']
                        df.loc[i, 'Level1'] = r2['Type1-L1 Statistics']
        # Check for type and level
        if (r1['Type'] == 2):
            if (r1['Level'] == 4):
                # Append level directly from object
                df.loc[i, 'Level4'] = df.loc[i, 'Object']
                # Iterate over lookup table
                for j, r2 in dfl.iterrows():
                    # Cross reference lookup table and populate rows in accordance
                    if (r2['Type2-L4 Statistics'] == df.loc[i, 'Object']):
                        df.loc[i, 'Level3'] = r2['Type2-L3 Statistics']
                        df.loc[i, 'Level2'] = r2['Type2-L2 Statistics']
                        df.loc[i, 'Level1'] = r2['Type2-L1 Statistics']

# Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
def level3_lookup(self, df, dfl):
    # Iterate over data
    for i, r1 in df.iterrows():
        # Check for type and level
        if (r1['Type'] == 1):
            if (r1['Level'] == 3):
                # Append level directly from object
                df.loc[i, 'Level3'] = df.loc[i, 'Object']
                # Iterate over lookup table
                for j, r2 in dfl.iterrows():
                    # Cross reference lookup table and populate rows in accordance
                    if (r2['Type1-L3 Statistics'] == df.loc[i, 'Object']):
                        df.loc[i, 'Level2'] = r2['Type1-L2 Statistics']
                        df.loc[i, 'Level1'] = r2['Type1-L1 Statistics']
        # Check for type and level
        if (r1['Type'] == 2):
            if (r1['Level'] == 3):
                # Append level directly from object
                df.loc[i, 'Level3'] = df.loc[i, 'Object']
                # Iterate over lookup table
                for j, r2 in dfl.iterrows():
                    # Cross reference lookup table and populate rows in accordance
                    if (r2['Type2-L3 Statistics'] == df.loc[i, 'Object']):
                        df.loc[i, 'Level2'] = r2['Type2-L2 Statistics']
                        df.loc[i, 'Level1'] = r2['Type2-L1 Statistics']

# Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
def level2_lookup(self, df, dfl):
    # Iterate over data
    for i, r1 in df.iterrows():
        # Check for type and level
        if (r1['Type'] == 1):
            if (r1['Level'] == 2):
                # Append level directly from object
                df.loc[i, 'Level2'] = df.loc[i, 'Object']
                # Iterate over lookup table
                for j, r2 in dfl.iterrows():
                    # Cross reference lookup table and populate rows in accordance
                    if (r2['Type1-L2 Statistics'] == df.loc[i, 'Object']):
                        df.loc[i, 'Level1'] = r2['Type1-L1 Statistics']
        # Check for type and level
        if (r1['Type'] == 2):
            if (r1['Level'] == 2):
                # Append level directly from object
                df.loc[i, 'Level2'] = df.loc[i, 'Object']
                # Iterate over lookup table
                for j, r2 in dfl.iterrows():
                    # Cross reference lookup table and populate rows in accordance
                    if (r2['Type2-L2 Statistics'] == df.loc[i, 'Object']):
                        df.loc[i, 'Level1'] = r2['Type2-L1 Statistics']

# Reference lookup table and append objects for levels 1-5 for both type 1 and type 2
def level1_lookup(self, df):
    # Iterate over data
    for i, r1 in df.iterrows():
        # Check for type and level
        if (r1['Type'] == 1):
            if (r1['Level'] == 1):
                # Append level directly from object
                df.loc[i, 'Level1'] = df.loc[i, 'Object']
        # Check for type and level
        if (r1['Type'] == 2):
            if (r1['Level'] == 1):
                # Append level directly from object
                df.loc[i, 'Level1'] = df.loc[i, 'Object']

# Append base region and hemisphere columns
def append_region_cols(self, df: pd.DataFrame):
    # Iterate over dataframe
    for i, row in df.iterrows():
        # Parse object and populate based on relevant region and hemisphere
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

# Appends hierarchical level 1-5 and ICV columns
def append_hierarchy_cols(self, df: pd.DataFrame, base_level: int):
    # Populate necessary columns based on base level
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
        # Invalid base level error
        print(str(self.append_hierarchy_cols.__name__) + ": Invalid base_level: " 
                + "\'" + str(base_level) + "\'" + ", valid base_level(s) include: 1-5")
        return

    return df

# Import and read data file into dataframe
def read_file(self, file: str): 
    # Read text file and store in dataframe
    df = pd.read_csv(file, sep='\t', skiprows=self.get_start_index(file)+1, 
        index_col=False, header=None, names=self.get_header(file))
    df.index += 1 # Shifts index up by 1 to make room for first level label

    # Removes level labels from dataframe
    df = df[df['Image'].str.contains('Type')==False]

    # Appends 'Type' column
    df['Type'] = df.index.map(self.get_type)

    # Appends 'Level' column
    df['Level'] = df.index.map(self.get_level)

    # Appends region and hemisphere detail columns
    self.append_region_cols(df)

    # Appends 'Prop' column
    tot_vol = df.loc[1:8, 'Volume_mm3'].sum()
    Prop = df.loc[:, 'Volume_mm3'] / tot_vol
    df['Prop'] = Prop

    # Rename 'Image' column to 'ID' and 'Volume_mm3' column to 'Volume'
    df.rename(columns={'Image':'ID', 'Volume_mm3':'Volume'}, inplace=True)

    # Drop unnecessary columns
    df = df.drop(columns=['Min', 'Max', 'Mean', 'Std'])

    return df

# Returns dataframe of type/level labels with preserved indices
def get_type_labels(self, file):
    # Read text file and store in dataframe
    df = pd.read_csv(file, sep='\t', skiprows=self.get_start_index(file)+1, 
        index_col=False, header=None, names=self.get_header(file))
    df.index += 1 # Shifts index up by 1 to make room for first level label
    
    # Isolates level labels with preserved indices, adds first level label
    df = df[df['Image'].str.match('Type')]
    df = self.type1_l1_exception(file, df)

    # Rename column to more suitable 'Labels'
    df = df['Image'].rename('Labels')

    return df

# Combines dataframes from a list of files
def import_data(self, path: str, id_type: str = 'numeric', id_list: list = None):
    files = self.get_files(path)
    files_found = files.copy()
    files_found = [x.replace(path + '/', '') for x in files_found]
    print(str(self.import_data.__name__) + ": Data files found")

    for i in files_found:
        print(i)

    print(str(self.import_data.__name__) + ": Importing...")
    df = pd.DataFrame()
    # Iterate over list of files, read in files, and concatenate into a dataframe
    for f in files:
        df2 = self.read_file(f)
        # Populate ID column based on id_type (custom, filename, numeric)
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
            # Invalid ID error
            print(str(self.import_data.__name__) + ": Invalid id_type: " 
                + "\'" + str(id_type) + "\'" + ", valid id_type(s) include: numeric, filename, custom")
            return
        df = pd.concat([df, df2], ignore_index=True)

    print(str(self.import_data.__name__) + ": Import successful")
    return df 

def append_covariate_data(self, file: str, icv: bool = False, tbv: bool = False):

    # Access data from data object
    df_original = self.long_to_wide()

    # Create dataframe of covariate data
    df_covariate = pd.read_csv(file)
    # Rename first column to 'ID' to match data and set as object
    df_covariate.rename(columns={df_covariate.columns[0]: 'ID'}, inplace=True)
    df_covariate['ID'] = df_covariate['ID'].astype(str)

    # DATA TESTING (DELETE LINE LATER)
    df_covariate.loc[:14, 'ID'] = ['Kermit', 'Miss Piggy', 'Fozzie', 'Gonzo',
                                    'Rowlf', 'Scooter', 'Animal', 'Pepe', 'Rizzo', 'Beaker', 
                                    'Statler', 'Waldorf', 'Swedish Chef', 'Bob', 'Sally']

    # Merge dataframes along ID column
    df = pd.merge(df_covariate, df_original, on='ID')

    # Append ICV volumes
    if icv:
        icv_cols = [col for col in df_original if col.endswith('_Type1.0_L1.0')]
        df['ICV'] = df[icv_cols].sum(axis=1)
    if tbv:
        tbv_cols = [col for col in df_original if col.endswith('_Type1.0_L1.0') and col != 'CSF_Type1.0_L1.0']
        df['TBV'] = df[tbv_cols].sum(axis=1)
    return df

if __name__ == '__main__':
    print(__name__)