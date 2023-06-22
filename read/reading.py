import os
import glob
import pandas as pd
import inspect
from miscellaneous import timed

# Globals
D_STR = "Depth (m)"
QC_STR = "qc (MPa)"
FS_STR = "fs (MPa)"
U2_STR = "u (MPa)"


def convert_file(ffp, out_fp, verbose=0):
    """

    Converts a CPT from different format into the standard liquepy format.
    This solves the problem of dealing with multiple different file formats
    by converting to a single format. The additional metadata is mostly
    maintained in the file.

    Algorithm explained
    -------------------
    Algorithm works by trial and error:
     - This algorithm cycles through each converter and tries to recognise the existing file format
        and then apply the conversion
     - if the file is different to the expected existing format then the conversion will fail and another converter is
        attempted
     - if successful, then the converter function name that was successful is returned
     - if unsuccessful, then 'NONE' is returned

    Liquepy CPT format
    ------------------
    The liquepy format is a simple standard format.
     - File is saved as a CSV
     - all units in metres and MPa.
     - CPT measurements start at line 25
     - Comma separation using ','
     - First 23 lines contain meta data
     - Pre-drill depth is defined in meta data as 'Pre-Drill:,<pre-drill depth>,'
     - Ground water level is defined in meta data as 'Assumed GWL:,<ground water depth>,'
     - Cone area ratio is defined in meta data as 'aratio,<cone area ratio>,'
     - Second line of metadata contains name of converter function (useful for debugging)

    Parameters
    ----------
    ffp : str
        Full file path to original CPT file
    out_fp : str
        Output folder path where formatted CPT file should be saved
    verbose: bool or int
        if true then print to algorithm steps to console

    Returns
    ----------
    None
    """

    fns = [convert_nmdc_to_csv_00, convert_nmdc_to_csv_01, convert_cs_to_csv_01, convert_cs_to_csv_02]
    for i, fn in enumerate(fns):
        if verbose:
            print(fn.__name__)
        res = fn(ffp, out_fp, verbose=verbose)
        if res == 1:
            return fn.__name__
        if i == len(fns) - 1:
            if verbose:
                print("NOT CONVERTED!")
            return "NONE"


@timed.timed
def convert_folder(in_fp, out_fp, verbose=0):
    """
    Reads through a folder of different CPT files and converts them to liquepy format.

    Parameters
    ----------
    in_fp: str
        Folder path of existing different CPT files
    out_fp: str
        Folder path where formatted different files should be saved
    verbose: int or bool
        if true then print to algorithm steps to console

    Returns
    ----------
    None
    """
    results = []
    ffps = glob.glob(in_fp + "*.xls*")  # Does not handle .csv and .txt
    ffps.sort()
    print(ffps)

    if not os.path.exists(out_fp):
        os.makedirs(out_fp)
    for ffp in ffps:
        if verbose:
            print(ffp)

        converter_name = convert_file(ffp, out_fp, verbose)
        fname = ffp.split(in_fp)[-1]

        results.append("{0},{1}".format(fname.split('/')[-1], converter_name))
    if verbose:
        print('SUMMARY: ')
        for line in results:
            print(line)
    ofile = open(out_fp + 'last_processed.txt', 'w')
    ofile.write("\n".join(results))
    ofile.close()
    return results


def trim_missing_at_end_data_df(df_data, neg_lim=None):
    """
    Removes rows at end of file that have empty data

    Parameters
    ----------
    df_data: DataFrame
        Current DataFrame to filter
    neg_lim:

    Returns
    ----------
    None
    """
    df_data = df_data.reset_index(drop=True)
    nan_rows = df_data[df_data.iloc[:, :3].isnull().T.any().T]
    nan_indexes = list(nan_rows.index)
    if len(nan_indexes):
        i_start = None
        i_end = None
        if nan_indexes[0] == 0:
            i_start = nan_indexes[-1] + 1
            for i in range(1, len(nan_indexes)):
                if nan_indexes[i] - nan_indexes[i - 1] > 1:
                    i_start = nan_indexes[i - 1] + 1
                    i_end = nan_indexes[i]
                    break
        else:
            i_end = nan_indexes[0]
        df_data = df_data[i_start:i_end]

    if neg_lim is not None:
        # remove large neg values
        neg_rows = df_data[df_data.iloc[:, 2] < neg_lim]
        neg_indexes = list(neg_rows.index)
        if len(neg_indexes):
            df_data = df_data[:neg_indexes[0]]

    return df_data


def convert_nmdc_to_csv_00(ffp, out_fp=None, verbose=0):
    """
    Converts NMDC CPT excel file type to liquepy format.
    Function works by first trying to see if the format
    is specific to this function else exits the function
    by returning 0. Many variables are specific to match
    this exact format like "d_str, qc_str".

    The way it converts the CPT excel to CSV is by splitting
    the Excel file into two DataFrames first, df_data & df_top.
    Performs operations on df_top searching for the necessary
    header information like "E,N,GWL,Pre-Drill etc".
    At the end, it will concatenate 4 DataFrames into a new one
    and save it directly to the CSV.

    DataFrames inside functions
    ----------
    df_data : DataFrame
        Holds the depth, q_c, f_s, u_2 info
    df_top : DataFrame
        Holds the header information
    df_z : DataFrame
        DataFrame to compensate for the number of lines
        required for the liquepy format. Index / Limit is
        22. On 23 we have str repr. of CPT data and on
        line 24 the values start
    df_headers : DataFrame
        Holds the 4 string representations of data_headers
        that are applied globally




    Parameters
    ----------
    ffp : str
        Full file path to original CPT file
    out_fp : str
        Folder path where formatted different files should be saved

    Returns
    ----------
    None

    """
    if "BTA" in ffp:
        cpt_num = ffp.split("BTA-")[-1]

    elif "PTA" in ffp:
        cpt_num = ffp.split("PTA-")[-1]

    elif "CPT" in ffp:
        cpt_num = ffp.split("CPT-")[-1]

    elif "HUD" in ffp:
        cpt_num = ffp.split("HUD-")[-1]

    else:
        cpt_num = ffp

    if ".xlsx" in cpt_num:
        cpt_num = cpt_num.split(".xlsx")[0]
    elif ".xls" in cpt_num:
        cpt_num = cpt_num.split(".xls")[0]

    #print(cpt_num)

    xf = pd.ExcelFile(ffp)
    if 'Header' in xf.sheet_names and 'Data' in xf.sheet_names:
        if verbose:
            print('found sheet names at convert_raw01_xlsx')
    else:
        return 0

    df = pd.read_excel(ffp, sheet_name='Data')

    d_str = 'Depth [m]'
    qc_str = 'Cone resistance (qc) in MPa'
    fs_str = 'Sleeve friction (fs) in MPa'
    u2_str = 'Dynamic pore pressure (u2) in MPa'

    cols = list(df)

    if cols[0] == d_str and cols[1] == qc_str and cols[2] == fs_str and cols[3] == u2_str:
        pass
    else:
        return 0
    # Cut the remaining columns from the original data sheet
    df_data = df.iloc[:, 0:4]
    df_data = trim_missing_at_end_data_df(df_data)
    # Create the dataFrame from the Header sheet
    df_top = pd.read_excel(ffp, sheet_name='Header')
    df_top = df_top.iloc[:, 0:4]  # I don't think it does much
    df_top.drop_duplicates(inplace=True, ignore_index=True)
    pp = len(df_top)
    limit = 22
    more = limit - pp
    gwl_row = None
    aratio_row = None
    predrill_row = None
    for i in range(len(df_top)):
        if df_top.iloc[i, 0] == "Predrill":
            df_top.iloc[i, 0] = 'Pre-Drill:'
            predrill_row = i
        if df_top.iloc[i, 0] == "Water level":
            df_top.iloc[i, 0] = 'Assumed GWL:'
            if df_top.iloc[i, 1] < 0:
                df_top.iloc[i, 1] *= -1
            gwl_row = i
        if df_top.iloc[i, 0] == "Alpha Factor":
            df_top.iloc[i, 0] = 'aratio'
            aratio_row = i
        if df_top.iloc[i, 0] == "E Coordinate":
            df_top.iloc[i, 0] = 'Easting'

        if df_top.iloc[i, 0] == "N Coordinate":
            df_top.iloc[i, 0] = 'Northing'

        if df_top.iloc[i, 0] == "Ground level":
            df_top.iloc[i, 0] = 'groundlvl'
        if df_top.iloc[i, 0] == "Date":
            df_top.iloc[i, 0] = 'Date:'

    if predrill_row is not None and predrill_row > limit:
        df_top.iloc[limit - 3, :] = df_top.iloc[predrill_row, :]
    if gwl_row is not None and gwl_row > limit:
        df_top.iloc[limit - 2, :] = df_top.iloc[gwl_row, :]
    if aratio_row is not None and aratio_row > limit:
        df_top.iloc[limit - 1, :] = df_top.iloc[aratio_row, :]
    if more < 0:
        df_top = df_top[:limit]
    n_cols = len(list(df_top))
    if n_cols < 4:
        for i in range(n_cols, 4):
            df_top["C%i" % i] = ""

    n_cols = len(list(df_top))
    if more < 0:
        df_top = df_top[:limit]
    zeros = [["", "", "", ""]] * more  # [[""]*n_data_cols] * more
    df_z = pd.DataFrame(zeros, columns=list(df_top))
    df_headers = pd.DataFrame([[D_STR, QC_STR, FS_STR, U2_STR]], columns=list(df_top))
    df_data.columns = list(df_top)
    df_top.iloc[0, -1] = inspect.stack()[0][3]
    df_new = pd.concat([df_top, df_z, df_headers, df_data])
    # df_new.to_csv(out_fp + "CPT_{0}.csv".format(cpt_num), index=False, sep=';')
    return df_new


def convert_nmdc_to_csv_01(ffp, out_fp=None, verbose=0):
    """
    Converts NMDC CPT excel file type to liquepy format.
    Function works by first trying to see if the format
    is specific to this function else exits the function
    by returning 0. Many variables are specific to match
    this exact format like "d_str, qc_str".

    The way it converts the CPT excel to CSV is by splitting
    the Excel file into two DataFrames first, df_data & df_top.
    Performs operations on df_top searching for the necessary
    header information like "E,N,GWL,Pre-Drill etc".
    At the end, it will concatenate 4 DataFrames into a new one
    and save it directly to the CSV.

    DataFrames inside functions
    ----------
    df_data : DataFrame
        Holds the depth, q_c, f_s, u_2 info
    df_top : DataFrame
        Holds the header information
    df_z : DataFrame
        DataFrame to compensate for the number of lines
        required for the liquepy format. Index / Limit is
        22. On 23 we have str repr. of CPT data and on
        line 24 the values start
    df_headers : DataFrame
        Holds the 4 string representations of data_headers
        that are applied globally




    Parameters
    ----------
    ffp : str
        Full file path to original CPT file
    out_fp : str
        Folder path where formatted different files should be saved

    Returns
    ----------
    None

    """
    if "BTA" in ffp:
        cpt_num = ffp.split("BTA-")[-1]
    elif "PTA" in ffp:
        cpt_num = ffp.split("PTA-")[-1]
    else:
        return 0
    cpt_num = cpt_num.split(".xlsx")[0]

    print(cpt_num)

    xf = pd.ExcelFile(ffp)
    if 'Header' in xf.sheet_names and 'Data' in xf.sheet_names:
        if verbose:
            print('found sheet names at convert_raw01_xlsx')
    else:
        return 0

    df = pd.read_excel(ffp, sheet_name='Data')

    d_str = 'Depth [m]'
    qc_str = 'Cone resistance (qc) in MPa'
    fs_str = 'Sleeve friction (fs) in MPa'
    u2_str = 'Dynamic pore pressure (u2) in MPa'

    cols = list(df)

    if cols[0] == d_str and cols[1] == qc_str and cols[2] == fs_str and cols[3] == u2_str:
        pass
    else:
        return 0
    # Cut the remaining columns from the original data sheet
    df_data = df.iloc[:, 0:4]
    df_data = trim_missing_at_end_data_df(df_data)
    # Create the dataFrame from the Header sheet
    df_top = pd.read_excel(ffp, sheet_name='Header')
    df_top = df_top.iloc[:, 0:4]  # I don't think it does much
    df_top.drop_duplicates(inplace=True, ignore_index=True)
    pp = len(df_top)
    limit = 22
    more = limit - pp
    gwl_row = None
    aratio_row = None
    predrill_row = None
    for i in range(len(df_top)):
        if df_top.iloc[i, 0] == "Predrill":
            df_top.iloc[i, 0] = 'Pre-Drill:'
            predrill_row = i
        if df_top.iloc[i, 0] == "Water level":
            df_top.iloc[i, 0] = 'Assumed GWL:'
            if df_top.iloc[i, 1] < 0:
                df_top.iloc[i, 1] *= -1
            gwl_row = i
        if df_top.iloc[i, 0] == "Alpha Factor":
            df_top.iloc[i, 0] = 'aratio'
            aratio_row = i
        if df_top.iloc[i, 0] == "E Coordinate":
            df_top.iloc[i, 0] = 'Easting'

        if df_top.iloc[i, 0] == "N Coordinate":
            df_top.iloc[i, 0] = 'Northing'

        if df_top.iloc[i, 0] == "Ground level":
            df_top.iloc[i, 0] = 'groundlvl'
        if df_top.iloc[i, 0] == "Date":
            df_top.iloc[i, 0] = 'Date:'

    if predrill_row is not None and predrill_row > limit:
        df_top.iloc[limit - 3, :] = df_top.iloc[predrill_row, :]
    if gwl_row is not None and gwl_row > limit:
        df_top.iloc[limit - 2, :] = df_top.iloc[gwl_row, :]
    if aratio_row is not None and aratio_row > limit:
        df_top.iloc[limit - 1, :] = df_top.iloc[aratio_row, :]
    if more < 0:
        df_top = df_top[:limit]
    n_cols = len(list(df_top))
    if n_cols < 4:
        for i in range(n_cols, 4):
            df_top["C%i" % i] = ""

    n_cols = len(list(df_top))
    if more < 0:
        df_top = df_top[:limit]
    zeros = [["", "", "", ""]] * more  # [[""]*n_data_cols] * more
    df_z = pd.DataFrame(zeros, columns=list(df_top))
    df_headers = pd.DataFrame([[D_STR, QC_STR, FS_STR, U2_STR]], columns=list(df_top))
    df_data.columns = list(df_top)
    df_top.iloc[0, -1] = inspect.stack()[0][3]
    df_new = pd.concat([df_top, df_z, df_headers, df_data])
    # df_new.to_csv(out_fp + "CPT_{0}.csv".format(cpt_num), index=False, sep=';')
    return df_new


def convert_cs_to_csv_01(ffp, out_fp=None, verbose=0):
    """

    Converts Capital Survey excel file format.
    --------------

    See also:
        convert_nmdc_to_csv_00
    """

    xf = pd.ExcelFile(ffp)
    if len(xf.sheet_names) > 1:
        return 0

    if "CPT" in ffp:
        cpt_num = ffp.split("CPT-")[-1]
    elif "HUD" in ffp:
        cpt_num = ffp.split("HUD-")[-1]
    else:
        return 0
    cpt_num = cpt_num.split(".xlsx")[0]

    df = pd.read_excel(ffp)
    df.head(32)

    ai, aii = 28, 6  # alpha index row + column
    di = 31  # index at which depth appears

    df_data = df.iloc[di:, 0:4]
    aratio = df.iat[ai, aii]  # find aratio at given index

    d_str = 'Depth [m]'
    qc_str = 'Qc [MPa]'
    fs_str = 'Fs [KPa]'
    u2_str = 'U2 [KPa]'

    cols = list(df.iloc[di, 0:4])  # Get columns # ['Depth [m]', 'Qc [MPa]', 'Fs [KPa]', 'U2 [KPa]']
    if cols[0] == d_str and cols[1] == qc_str and cols[2] == fs_str and cols[3] == u2_str:
        pass
    else:
        return 0
    df_data = df.iloc[di + 1:, 0:4]

    # df_data = trim_missing_at_end_data_df(df_data, neg_lim=-100)
    df_data.iloc[:, 2] = df_data.iloc[:, 2] / 1e3  # convert to MPa
    df_data.iloc[:, 3] = df_data.iloc[:, 3] / 1e3  # convert to MPa
    df_data = df_data.reset_index(drop=True)  # Reset index from 31 to 0

    df_top = df.iloc[:di - 1, 0:2]
    df_top = df_top.dropna().reset_index(drop=True)
    df_top.loc[len(df_top)] = ['aratio', aratio]
    df_top.drop_duplicates(inplace=True, ignore_index=True)
    pp = len(df_top)
    limit = 22
    more = limit - pp
    gwl_row = None
    aratio_row = pp
    predrill_row = None

    for i in range(len(df_top)):
        if df_top.iloc[i, 0] == "Prehole depth [cm]:":
            return 0
        if df_top.iloc[i, 0] == "Prehole depth [m]:":
            df_top.iloc[i, 0] = 'Pre-Drill:'
            predrill_row = i
        if df_top.iloc[i, 0] == "Hydrostatic line [m]:":
            df_top.iloc[i, 0] = 'Assumed GWL:'
            if df_top.iloc[i, 1] < 0:
                df_top.iloc[i, 1] *= -1
            gwl_row = i
        #     if df_top.iloc[i, 0] == "Alpha Factor":
        #         df_top.iloc[i, 0] = 'aratio'
        #         aratio_row = i
        if df_top.iloc[i, 0] == "Coords Easting:":
            df_top.iloc[i, 0] = 'Easting'
        if df_top.iloc[i, 0] == "Coords Northing:":
            df_top.iloc[i, 0] = 'Northing'
        if df_top.iloc[i, 0] == "Ground level [m]:":
            df_top.iloc[i, 0] = 'groundlvl'

    if predrill_row is not None and predrill_row > limit:
        df_top.iloc[limit - 3, :] = df_top.iloc[predrill_row, :]
    if gwl_row is not None and gwl_row > limit:
        df_top.iloc[limit - 2, :] = df_top.iloc[gwl_row, :]
    if aratio_row is not None and aratio_row > limit:
        df_top.iloc[limit - 1, :] = df_top.iloc[aratio_row, :]
    if more < 0:
        df_top = df_top[:limit]
    n_cols = len(list(df_top))
    if n_cols < 4:
        for i in range(n_cols, 4):
            df_top["C%i" % i] = ""

    n_cols = len(list(df_top))
    if more < 0:
        df_top = df_top[:limit]
    zeros = [["", "", "", ""]] * more  # [[""]*n_data_cols] * more
    df_z = pd.DataFrame(zeros, columns=list(df_top))
    df_headers = pd.DataFrame([[D_STR, QC_STR, FS_STR, U2_STR]], columns=list(df_top))
    df_data.columns = list(df_top)
    df_top.iloc[0, -1] = inspect.stack()[0][3]
    df_new = pd.concat([df_top, df_z, df_headers, df_data])
    # df_new.to_csv(out_fp + "CPT_{0}.csv".format(cpt_num), index=False, sep=';')
    return df_new


def convert_cs_to_csv_02(ffp, out_fp=None, verbose=0):
    """

    Converts Capital Survey excel file format.
    --------------

    See also:
        convert_nmdc_to_csv_00
        convert_nmdc_to_csv_00
    """

    xf = pd.ExcelFile(ffp)
    if len(xf.sheet_names) > 1:
        return 0

    if "CPT" in ffp:
        cpt_num = ffp.split("CPT-")[-1]
    elif "HUD" in ffp:
        cpt_num = ffp.split("HUD-")[-1]
    else:
        return 0
    cpt_num = cpt_num.split(".xlsx")[0]

    df = pd.read_excel(ffp)
    df.head(32)

    ai, aii = 28, 6  # alpha index row + column
    di = 31  # index at which depth appears

    df_data = df.iloc[di:, 0:4]
    aratio = df.iat[ai, aii]  # find aratio at given index

    d_str = 'Depth [m]'
    qc_str = 'Qc [MPa]'
    fs_str = 'Fs [KPa]'
    u2_str = 'U2 [KPa]'

    cols = list(df.iloc[di, 0:4])  # Get columns # ['Depth [m]', 'Qc [MPa]', 'Fs [KPa]', 'U2 [KPa]']
    if cols[0] == d_str and cols[1] == qc_str and cols[2] == fs_str and cols[3] == u2_str:
        pass
    else:
        return 0
    df_data = df.iloc[di + 1:, 0:4]

    # df_data = trim_missing_at_end_data_df(df_data, neg_lim=-100)
    df_data.iloc[:, 2] = df_data.iloc[:, 2] / 1e3  # convert to MPa
    df_data.iloc[:, 3] = df_data.iloc[:, 3] / 1e3  # convert to MPa
    df_data = df_data.reset_index(drop=True)  # Reset index from 31 to 0

    df_top = df.iloc[:di - 1, 0:2]
    df_top = df_top.dropna().reset_index(drop=True)
    df_top.loc[len(df_top)] = ['aratio', aratio]
    df_top.drop_duplicates(inplace=True, ignore_index=True)
    pp = len(df_top)
    limit = 22
    more = limit - pp
    gwl_row = None
    aratio_row = pp
    predrill_row = None

    for i in range(len(df_top)):
        if df_top.iloc[i, 0] == "Prehole depth [cm]:":
            df_top.iloc[i, 0] = 'Pre-Drill:'
            predrill_row = i
        if df_top.iloc[i, 0] == "Hydrostatic line [cm]:":
            df_top.iloc[i, 0] = 'Assumed GWL:'
            if df_top.iloc[i, 1] < 0:
                df_top.iloc[i, 1] *= -1
            gwl_row = i
        #     if df_top.iloc[i, 0] == "Alpha Factor":
        #         df_top.iloc[i, 0] = 'aratio'
        #         aratio_row = i
        if df_top.iloc[i, 0] == "Latitude:":
            df_top.iloc[i, 0] = 'Easting'
        if df_top.iloc[i, 0] == "Longitude:":
            df_top.iloc[i, 0] = 'Northing'
        if df_top.iloc[i, 0] == "Ground level [m]:":
            df_top.iloc[i, 0] = 'groundlvl'

    if predrill_row is not None and predrill_row > limit:
        df_top.iloc[limit - 3, :] = df_top.iloc[predrill_row, :]
    if gwl_row is not None and gwl_row > limit:
        df_top.iloc[limit - 2, :] = df_top.iloc[gwl_row, :]
    if aratio_row is not None and aratio_row > limit:
        df_top.iloc[limit - 1, :] = df_top.iloc[aratio_row, :]
    if more < 0:
        df_top = df_top[:limit]
    n_cols = len(list(df_top))
    if n_cols < 4:
        for i in range(n_cols, 4):
            df_top["C%i" % i] = ""

    n_cols = len(list(df_top))
    if more < 0:
        df_top = df_top[:limit]
    zeros = [["", "", "", ""]] * more  # [[""]*n_data_cols] * more
    df_z = pd.DataFrame(zeros, columns=list(df_top))
    df_headers = pd.DataFrame([[D_STR, QC_STR, FS_STR, U2_STR]], columns=list(df_top))
    df_data.columns = list(df_top)
    df_top.iloc[0, -1] = inspect.stack()[0][3]
    df_new = pd.concat([df_top, df_z, df_headers, df_data])
    # df_new.to_csv(out_fp + "CPT_{0}.csv".format(cpt_num), index=False, sep=';')
    return df_new



# in_fp = 'roshna/pre data/'
# out_fp = in_fp +'processed/'
# convert_folder(in_fp, out_fp, verbose=1)
