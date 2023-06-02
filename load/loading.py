import datetime
import pandas as pd
import numpy as np
import ntpath


class CPTHeader:
    def __init__(self, date, gwl, ground_lvl, pre_drill, easting, northing, name):
        self.date = date
        self.gwl = gwl
        self.ground_lvl = ground_lvl
        self.pre_drill = pre_drill
        self.easting = easting
        self.northing = northing
        self.name = name

    @property
    def latex_dict(self):
        _list = ['Name:', 'Date:', 'Ground Water Level:', 'Ground Level:', 'Pre-Drill:', 'Easting', 'Northing']
        _values = [self.name, self.date, self.gwl, self.ground_lvl, self.pre_drill, self.easting, self.northing]
        _suffix = ['', '', ' m', ' m', ' m', ' m', ' m']
        _dict = {}
        for k, v, s in zip(_list, _values, _suffix):
            _dict[k] = str(v) + s
        return _dict


def load_cpt_header(file):
    headers = ['Date:', 'Assumed GWL:', 'groundlvl', 'Pre-Drill:', 'Easting', 'Northing',
               'aratio', 'Sounding Number']

    limit = 24
    name = file.split('CPT_')[-1].split('.csv')[0]
    df = pd.read_csv(file, sep=';')
    new_df = df.iloc[:limit, 0:2]
    series1 = list(new_df.iloc[:, 0])  # Store  all 1st row variables  from DataFrame
    series2 = list(new_df.iloc[:, 1])  # Store all 2nd row values from DataFrame
    d = dict(zip(series1, series2))

    try:
        d['Date:'] = datetime.datetime.strptime(d['Date:'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        d['Date:'] = datetime.datetime.strptime(d['Date:'], '%m/%d/%Y %H:%M:%S %p')

    d['Date:'] = d['Date:'].strftime('%d-%m-%Y')
    d['groundlvl'] = round(float(d['groundlvl']), 2)
    return CPTHeader(d['Date:'], d['Assumed GWL:'], d['groundlvl'], d['Pre-Drill:'], d['Easting'], d['Northing'], name)


def load_dataframe(ffps):
    """"

    Iterates through the output folder, looking for all csv files
    It reads file by file, looking through the contents of header
    data.

    Example:
     "Easting" : "2600985"
     "Assumed GWL" : 0.00
    
    A header list is created and it searches for the values that 
    reference the headers. It also loads the CPT data as a CPT object 
    for further processing. Every file is appended in the DataFrame
    row by row.

   
    
    Parameters
    ------------
    out_fp : str
        Folder path of existing  CPT files in CSV format
    save_fp : str 
        Folder path where dataframe files should be saved
    
    Returns 
    ------------
    DataFrame
        Data frame contains
    
    See Also
    ------------
    load_mpa_cpt_file()

    """

    # ffps = glob.glob(out_fp + "*.csv")  #

    headers = ['Date:', 'Assumed GWL:', 'groundlvl', 'Pre-Drill:', 'Easting', 'Northing',
               'aratio', 'Length', 'CPT-ID', 'Object']
    limit = 24
    hh = headers[0:-3]  # Up to but not including the 'CPT-ID' & 'Object'. T
    dfo = pd.DataFrame(columns=[""] * 10)
    dfo.columns = headers
    for i, file in enumerate(ffps):
        # print(file)
        name = file.split('CPT_')[-1].split('.csv')[0]
        df = pd.read_csv(file, sep=';')

        new_df = df.iloc[:limit, 0:2]

        series1 = list(new_df.iloc[:, 0])  # Store  all 1st row variables  from DataFrame
        series2 = list(new_df.iloc[:, 1])  # Store all 2nd row values from DataFrame
        dicty = dict(zip(series1, series2))

        l = []  # Store the dict values based on the order of appeareance
        for x in hh:
            l.append(dicty[x])

        vals = dict(zip(headers, l))
        # print(vals)
        cpt = load_mpa_cpt_file(file, delimiter=";")
        # Create a list out of the dictionary values
        val_list = list(vals.values())
        val_list.extend([cpt.depth.size / 100, name, cpt])  # Grow list to the size of headers
        # Append to data frame
        dfo.loc[i, :] = val_list
    col_order = ['CPT-ID', 'groundlvl', 'Length', 'Easting', 'Northing', 'Pre-Drill:', 'Assumed GWL:', 'aratio',
                 'Date:', 'Object']
    # dfo = dfo[dfo_order]
    return dfo[col_order]


def save_df_to_excel(df, name="00_Header&Data.xlsx"):
    """

    Save a DataFrame to excel.
    
    
    Parameters
    ------------
    df : DataFrame
    name : str
        Name of file, defaults to "00_Header&Data.xlsx"

    Returns 
    ------------
    None    

    #TODO: Add output file location
    """

    excel_file = pd.ExcelWriter(name)
    df.to_excel(excel_file, sheet_name='df')
    excel_file.save()

    return None


def convert_to_dtype(df):
    """

    Convert different column types to their respective types,
    especially time to datetime type for future manipulation.

    Parameters
    -------------
    df : DataFrame
        
    Returns
    -------------
    None


    #TODO: Check to see if .astype(float) & .astype(str) is redundant

    """
    df['groundlvl'] = df['groundlvl'].astype(float)
    df['Date:'] = pd.to_datetime(df['Date:'])
    df['Assumed GWL:'] = df['Assumed GWL:'].astype(float)
    df['Pre-Drill:'] = df['Pre-Drill:'].astype(float)
    df['aratio'] = df['aratio'].astype(float)
    df['CPT-ID'] = df['CPT-ID'].astype(str)

    return None


def load_mpa_cpt_file(ffp, scf=1, delimiter=";", a_ratio_override=None):
    """
    scf - Shell Correction Factor, Defaults to 1.0
    """
    # import data from csv file
    folder_path, file_name = ntpath.split(ffp)
    file_name = file_name.split(".")[0]
    ncols = 4
    try:
        data = np.loadtxt(ffp, skiprows=24, delimiter=delimiter, usecols=(0, 1, 2, 3))
    except:
        ncols = 3
        data = np.loadtxt(ffp, skiprows=24, delimiter=delimiter, usecols=(0, 1, 2))
    depth = data[:, 0]
    q_c = data[:, 1] * 1e3 * scf  # convert to kPa
    f_s = data[:, 2] * 1e3  # convert to kPa
    if ncols == 4:
        u_2 = data[:, 3] * 1e3  # convert to kPa
    else:
        u_2 = np.zeros_like(depth)
    gwl = None
    a_ratio = 1.0
    pre_drill = None
    infile = open(ffp)
    lines = infile.readlines()
    for line in lines:
        if "Assumed GWL:" in line:
            gwl = line.split(delimiter)[1]
            if gwl == '-':
                gwl = None
            else:
                gwl = float(line.split(delimiter)[1])
        if "aratio" in line:
            try:
                a_ratio = float(line.split(delimiter)[1])
            except ValueError:
                pass
        if "Pre-Drill:" in line:
            val = line.split(delimiter)[1]
            if val != '':
                pre_drill = float(val)
        if "groundlvl" in line:
            val = line.split(delimiter)[1]
            if val != '':
                groundlvl = float(val)
    if a_ratio_override:
        a_ratio = a_ratio_override
    if pre_drill is not None:
        if depth[0] < pre_drill:
            indy = np.argmin(abs(depth - pre_drill))
            depth = depth[indy:]
            q_c = q_c[indy:]
            f_s = f_s[indy:]
            u_2 = u_2[indy:]
    return CPT(depth, q_c, f_s, u_2, gwl, groundlvl, a_ratio, folder_path=folder_path, file_name=file_name,
               delimiter=delimiter)


class CPT(object):
    def __init__(self, depth, q_c, f_s, u_2, gwl, groundlvl, a_ratio=None, folder_path="<path-not-set>",
                 file_name="<name-not-set>",
                 delimiter=";"):
        """
        A cone penetration resistance test

        Parameters
        ----------
        depth: array_like
            depths from surface, properties are forward projecting (i.e. start at 0.0 for surface)
        q_c: array_like, [kPa]
        f_s: array_like, [kPa]
        u_2: array_like, [kPa]
        gwl: float, [m]
            ground water level
        a_ratio: float,
            Area ratio
        """
        self.depth = depth
        self.q_c = q_c
        self.f_s = f_s
        self.u_2 = u_2
        self.gwl = gwl
        self.a_ratio = a_ratio
        self.folder_path = folder_path
        self.file_name = file_name
        self.delimiter = delimiter
        self.elevation = groundlvl - depth
        self._q_t = None
        self._r_f = None

    @property
    def q_t(self):
        """
        Pore pressure corrected cone tip resistance

        """
        # qt the cone tip resistance corrected for unequal end area effects, eq 2.3

        # lazy load of q_t
        if self._q_t is None:
            self._q_t = self.q_c + ((1 - self.a_ratio) * self.u_2)
        return self._q_t

    @property
    def r_f(self):
        if self._r_f is None:
            self._r_f = (self.f_s[1:] / self.q_t[1:]) * 100  # in percentages
            self._r_f = np.insert(self.r_f, 0, 0)
        return self._r_f

    # @q_t.setter
    # def q_t(self, q_t):
    #     self.q_c = q_t - ((1 - self.a_ratio) * self.u_2)

