import numpy as np
import matplotlib.pyplot as plt
import datetime
import json

import liquepy as lq
from calc.liquefaction import run_rw1997


def create_soil_params(layers):
    mask = np.where((layers[1:] - layers[:-1]) != 0)  # Mask, condition is true where there is a change in soil type.
    mask = mask[0]  # Remove the tuple

    if layers.size not in mask:
        soil_indexes = np.append(mask, layers.size - 1)
        # layers = np.append(layers, layers[-1])
        # pass

    soil_type = layers[soil_indexes]
    soil_layers = soil_indexes[1:] - soil_indexes[:-1]
    soil_layers = np.insert(soil_layers, 0, 0)

    return soil_type, soil_layers, soil_indexes


# i_c, depth = np.loadtxt('abc.txt', delimiter=',', skiprows=1)

soils = ['Gravelly sand to dense sand',
         'Clean sand to silty sand', 'Silty sand to sandy silt',
         'Clayey silt to silty clay', 'Clays - silty clay to clay',
         'Oranic soils - clav']

# Create a dictionary with 1...5 as keys and the soil types as values
COLORS_IC = ['#f19e45', '#b8a365', '#76c0a2', '#469186', '#4d567c', '#bb6639']


def color_filter(ics):
    colors = np.empty(len(ics), dtype='U30')
    # given the indexes, color_filter the ics based on colors
    # where ics is less than 1.31 -> red
    colors[ics == 1] = COLORS_IC[0]
    colors[ics == 2] = COLORS_IC[1]
    colors[ics == 3] = COLORS_IC[2]
    colors[ics == 4] = COLORS_IC[3]
    colors[ics == 5] = COLORS_IC[4]
    colors[ics == 6] = COLORS_IC[5]

    return colors


def ic_absorption_reduce(soil_indexes, soil_layers, soil_type, layers=None, absorption=20):
    """
        Reduces the soil layers (thickness) values  based on a threshold.

        Parameters:
            soil_indexes (numpy.ndarray): An array containing the indexes of the soil layers.
            soil_layers (numpy.ndarray): An array containing the thickness of each soil layer.
            soil_type (numpy.ndarray): An array containing the soil type for each layer.
            absorption (int, optional): The absorption threshold. Default is 20.

        Returns:
            tuple: A tuple containing the following arrays:
                - soil_array_types (numpy.ndarray): An array with the soil types for each layer, after reducing absorption.
                - soils (numpy.ndarray): An array containing the original soil types.
                - start (numpy.ndarray): An array containing the start indexes for each reduced absorption section.
                - end (numpy.ndarray): An array containing the end indexes for each reduced absorption section.
    """
    # Create an array with the absorption values for each layer
    # Keys:  0,   7,  63,  68,  90, 104,107, 116, 125, 156, 157, 221,
    # Values:        7,  56,   5,  22,  14,      3,     9,     9,   31,   1,    64,
    mask = np.where(soil_layers >= absorption)
    start = soil_indexes[mask]
    end = soil_indexes[mask]

    soils = soil_type[mask]

    start = np.insert(start, 0, 0)
    end = np.append(end, layers.size - 1)
    soils = np.append(soils, soils[-1])

    # Fill an array with values between the indexes indeces with the soils values
    soil_array_types = np.zeros(len(layers), dtype=int)
    # Replace the zeros with the soil types
    for i in range(len(soils)):
        soil_array_types[start[i]:end[i] + 1] = soils[i]

    return soil_array_types, (soils, start, end)


def map_soil_index(arr):
    # Map the soil index array to the soil types
    layers = np.empty(len(arr), dtype=int)
    layers[arr < 1.31] = 1
    layers[(1.31 <= arr) & (arr < 2.05)] = 2
    layers[(2.05 <= arr) & (arr < 2.6)] = 3
    layers[(2.6 <= arr) & (arr < 2.95)] = 4
    layers[(2.95 <= arr) & (arr < 3.6)] = 5
    layers[arr >= 3.6] = 6
    return layers


def map_soil_dict():
    return {1: 'Gravelly Sand to Dense Sand',
            2: 'Clean Sand to Silty Sand',
            3: 'Silty Sand to Sandy Silt',
            4: 'Clayey Silt to Silty Clay',
            5: 'Silty Clay to Clay',
            6: 'Oranic Soils - Clay'}


def create_soil_profile(i_c, absorption=20):
    """
        Creates a soil profile from an array of i_c values with a threshold for absorption.
        Defaults to 20. That means all layers with a thickness of <20cm
        will be absorbed into the layer above.


        Parameters:
        -------------
            i_c (numpy.ndarray): An array containing the i_c values.
            absorption (int, optional): The absorption threshold. Default is 20.

        Returns:
        -------------
            tuple: A tuple containing the following arrays:
                - soil_array_types (numpy.ndarray): An array with the soil types for each layer, after  absorption.
                - soils (numpy.ndarray): An array containing the original soil types.
                - start (numpy.ndarray): An array containing the start indexes for each reduced absorption section.
                - end (numpy.ndarray): An array containing the end indexes for each reduced absorption section.
    """
    layers = map_soil_index(i_c)  # Map the soil index array to the soil types [1.....6]
    mask = np.where((layers[1:] - layers[:-1]) != 0)  # Mask, condition is true where there is a change in soil type.
    mask = mask[0]  # Remove the tuple

    if layers.size not in mask:
        soil_indexes = np.append(mask, layers.size - 1)
        # layers = np.append(layers, layers[-1])
        # pass

    soil_type = layers[soil_indexes]
    soil_layers = soil_indexes[1:] - soil_indexes[:-1]
    soil_layers = np.insert(soil_layers, 0, 0)

    ic_absorbed, soil_tuple = ic_absorption_reduce(soil_indexes, soil_layers, soil_type, layers=layers,
                                                   absorption=absorption)

    soils, start, end = remove_adjacent_values(*soil_tuple)

    return ic_absorbed, soils, start, end


def remove_adjacent_values(soils, start, end):
    """
    Removes adjacent duplicate values in an array.It then stiches the last index so we are
    not only modifying the soil array  but start and end indexes too

    Parameters
    ----------
    soils:  array
        Soil types
    start: array
        Start indexes
    end: array
        End indexes

    Input Example:
    -----------
    array([1, 1, 2, 2, 3, 4, 3, 4, 1, 2, 2, 2])
    array([  0,  63,  90, 156, 221, 265, 298, 345, 390, 468, 609, 672]
    array([ 63,  90, 156, 221, 265, 298, 345, 390, 468, 609, 672, 683]

    Output:
    -----------
    array([1, 2, 3, 4, 3, 4, 1, 2])
    array([  0,  90, 221, 265, 298, 345, 390, 468]
    array([ 90, 221, 265, 298, 345, 390, 468, 683]

    Returns:
    -----------
    soils, start, end : tuple
    """

    cond = np.diff(soils) != 0
    stard_cond = np.insert(cond, 0, True)  # Stich the first index
    start = start[stard_cond]

    # mask2 = np.diff(soils) !=0
    end_cond = np.append(cond, True)  # Stich the last index
    end = end[end_cond]

    reduced_soil = soils[1:] - soils[:-1]
    reduced_soil = np.insert(reduced_soil, 0, soils[0])

    mask = np.where(reduced_soil != 0)
    soils = soils[mask]

    return soils, start, end


def create_dictionary_for_sql():
    createdon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    createdby = 'map-soil-index-dgs'
    soil_dict = map_soil_dict()
    sql_dict = {}

    for i, (soil, ss, ee) in enumerate(zip(soils, start, end)):
        sql_dict[i] = {'SoilLayer': soil_dict[soil],
                       'ElevationStart': ss / 100,
                       'ElevationEnd': ee / 100,
                       'CreatedOn': createdon,
                       'CreatedBy': createdby,
                       'AbsorptionRate': 20}
    return sql_dict


def plot_sp_from_obj(sp):
    colors = color_filter(sp.i_c_abs)
    fig, ax = plt.subplots(figsize=(6, 12))
    ax.set_aspect('equal')
    ax.barh(-sp.depth, sp.i_c_abs, height=0.01, color=colors, alpha=0.75)
    for soil, y1, y2 in zip(sp.soils, sp.start / 100, sp.end / 100):
        ax.annotate(sp.soil_dict[soil], xy=(1, -(y1 + y2) / 2), fontsize=12)
    ax.set_xlabel('IC (%)')
    ax.set_ylabel('Depth (m)')
    ax.set_title('Soil Profile')
    plt.show()


def plot_ic_single(ic_absorbed, soils, start, end):
    colors = color_filter(ic_absorbed)
    soil_dict = map_soil_dict()
    fig, ax = plt.subplots(figsize=(6, 12))
    ax.set_aspect('equal')
    ax.barh(-depth, ic_absorbed, height=0.01, color=colors, alpha=0.75)
    # Annotate the soil type on the plot
    for soil, y1, y2 in zip(soils, start / 100, end / 100):
        ax.annotate(soil_dict[soil], xy=(1, -(y1 + y2) / 2), fontsize=12)
    ax.set_xlabel('IC (%)')
    ax.set_ylabel('Depth (m)')
    ax.set_title('IC profile')
    plt.show()


def plot_ic_multiple():
    layers = map_soil_index(i_c)
    fig, axs = plt.subplots(2, 3, figsize=(10, 10), sharex=True, sharey=True)
    axs = axs.flatten()
    # ax.set_aspect('equal')
    abs_layers = [1, 5, 10, 15, 20, 45]
    for i, x in enumerate(abs_layers):
        generate_ax_soil_at_absorbtion(axs[i], x, layers)
    plt.show()


def generate_ax_soil_at_absorbtion(ax, absorption, layers):
    ic_absorbed, soils, start, end = create_soil_profile(i_c=i_c, absorption=absorption)
    # ic_absorbed, soils, start, end = ic_absorption_reduce(soil_indexes, soil_layers, soil_type, absorption=absorption)
    colors = color_filter(ic_absorbed)
    ax.barh(-depth, ic_absorbed, height=0.01, color=colors, alpha=0.75)
    # remove in the soils array any consectuive value but save the first. Remove duplicates of the same layer if any
    trial = soils[1:] - soils[:-1]
    trial = np.insert(trial, 0, soils[0])
    mask = np.where(trial != 0)
    soils = soils[mask]
    start = start[mask]
    end = end[mask]
    end[-1] = i_c.size - 1
    # soils,start,end

    for soil, y1, y2 in zip(soils, start / 100, end / 100):
        ax.annotate(soil, xy=(1, -(y1 + y2) / 2), fontsize=12)

    x1 = layers.size
    # ic_random = np.random.randint(1, 6, size=layers.size)
    # ic_random = np.ones(layers.size)
    # x2 = layers - ic_random
    x2 = layers - ic_absorbed

    x2 = x2[x2 == 0].size

    ax.set_xlabel('IC (%)')
    ax.set_ylabel('Depth (m)')
    ax.set_title(f'Absorption: {absorption}, Accuracy:{np.round(x2 / x1 * 100, 2)}')


class SoilProfile():
    def __init__(self, obj):
        self.obj = obj
        self.i_c = obj.i_c
        self.depth = obj.depth
        self.i_c_layered = map_soil_index(self.i_c)
        self.soil_types, self.soil_layers, self.soil_index = create_soil_params(self.i_c_layered)
        self.i_c_abs, soil_tuple = ic_absorption_reduce(self.soil_index, self.soil_layers,
                                                        self.soil_types, layers=self.i_c_layered)
        self.soils, self.start, self.end = remove_adjacent_values(*soil_tuple)
        self.soil_dict = map_soil_dict()

        self._unit_wt = None
        self._phi = None
        self._elastic_modulus = None
        self._s_u = None

    def __repr__(self):
        return f'SoilProfile({self.soils}, {self.start},{self.end})'

    @property
    def unit_wt(self):
        if self._unit_wt is None:
            self._unit_wt = np.zeros(self.soils.size)
            for i, (start, end) in enumerate(zip(self.start, self.end)):
                self.unit_wt[i] = np.average(self.obj.unit_wt[start:end])
        return self._unit_wt

    @property
    def phi(self):
        if self._phi is None:
            self._phi = np.zeros(self.soils.size)
            for i, (start, end) in enumerate(zip(self.start, self.end)):
                self._phi[i] = np.average(self.obj.phi[start:end])
        return self._phi

    @property
    def s_u(self):
        if self._s_u is None:
            self._s_u = np.zeros(self.soils.size)
            for i, (start, end) in enumerate(zip(self.start, self.end)):
                self._s_u[i] = np.average(self.obj.s_u[start:end])
                self._s_u[self.soils <= 2] = 0
        return self._s_u

    @property
    def elastic_modulus(self):
        if self._elastic_modulus is None:
            self._elastic_modulus = np.zeros(self.soils.size)
            for i, (start, end) in enumerate(zip(self.start, self.end)):
                self._elastic_modulus[i] = np.average(self.obj.elastic_modulus[start:end])
        return self._elastic_modulus

    def plot_sp(self):
        pass

    def to_csv(self):
        pass

    def to_json(self):
        template = {}
        vars = ['soils', 'start', 'end', 'unit_wt', 'phi', 's_u', 'elastic_modulus']
        for var in vars:
            template[var] = getattr(self, var)

        json_ready = serialize(template)

        with open('sp.json', 'w', ) as fp:
            json.dump(template, fp)

    def to_latex(self):
        pass


def serialize(temp):
    for key, value in temp.items():
        if isinstance(value, np.ndarray):
            temp[key] = value.tolist()
    return temp




cpt = lq.field.load_mpa_cpt_file('C:/Users/dragos/PycharmProjects/cptspy/calc/CPT_H15d.csv', delimiter = ';')
rw1997 = run_rw1997(cpt, pga=0.20, m_w=6.0, gwl=8)
print(rw1997.i_c)
sp = SoilProfile(rw1997)

sp.to_json()

print(sp.soils)