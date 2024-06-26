#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 16:13:14 2024

@author: damienmaillard
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import gdspy

#%% GREY-SCALE LITHOGRAPHY GDS GENERATION
def save_file(data, filename):
    # Data conversion to a pandas data frame
    df = pd.DataFrame(data)

    # Save the selected columns to a TXT file
    df.to_csv(filename + '.txt', sep = '\t', index=False, header=False)

def generate_concentric_rings(center, radii):
    # Setting up the library and the cells
    lib = gdspy.GdsLibrary(unit=1e-6, precision=1e-9)
    cell_name = 'CONCENTRIC_RINGS'
    cell = lib.new_cell(cell_name)
    
    # First disk at the center
    center_disk = gdspy.Round(center, radii[0], inner_radius=0, number_of_points=100, layer=255, datatype=0)
    cell.add(center_disk)
    
    # Assign each ring to a different layer
    for i in range(len(radii) - 1):
        # The layer is i (0, 1, 2, ...) and datatype is always 0
        ring = gdspy.Round(center, radii[i+1], inner_radius=radii[i], number_of_points=100, layer=255-i-1, datatype=0)
        cell.add(ring)
    
    return lib

# Function to find indices where the integer value changes
def find_change_indices(values):
    change_indices = []
    # Loop through the list from the second element to the end
    for i in range(1, len(values)):
        # Check if the current element is different from the previous element
        if values[i] != values[i - 1]:
            # If different, append the index of the change
            change_indices.append(i)
    return change_indices

def generate_save_gds(filename, lib):
    gdspy.current_library = gdspy.GdsLibrary()
    
    lib.write_gds(filename)  # Save the GDS file
    
    # Display all cells using the internal viewer.
    gdspy.LayoutViewer(lib)

# Define the sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-0.5*x))

# Define quadratic function
def quadratic(a, b, c, x):
    return a*x**2 + b*x + c

# Define a cubic function
def cubic(a, b, c, d, x):
    # Define the model function
    return a * x**3 + b * x**2 + c * x + d

def rings(cavity_radius, resol, function, grey_levels, nominal_dose, name):
    
    if function[0] == 'sigmoid':
        x_left = np.linspace(-cavity_radius, 0, int(cavity_radius / resol))
        x_right = np.linspace(0, cavity_radius, int(cavity_radius / resol))

        x_all = np.concatenate((x_left,x_right))
        
        y = sigmoid(x_left / function[1] + function[2])

        # Further scaling according the number of grey levels wanted
        scaled_y = - grey_levels * (y - 1) - 255 # grey level
    
    if function[0] == 'quadratic':
        # Define the x range: stretching from -2000 to 0
        x_left_1 = np.linspace(-cavity_radius, -cavity_radius / 2, int(cavity_radius / 2 / resol))
        x_left_2 = np.linspace(-cavity_radius / 2, 0, int(cavity_radius / 2 / resol))
        x_left = np.concatenate((x_left_1, x_left_2))
        x_right = np.linspace(0, cavity_radius , int(cavity_radius / resol))
        x_all = np.concatenate((x_left,x_right))

        # Compute the sigmoid function
        # Stretching: the "6" controls the stretch; smaller values make it stretch more.
        y1 = quadratic(-1 / function[1], function[2], -1, x_left_1)  # stretch and shift the function
        y2 = quadratic(1 / function[1], 0, 0, x_left_2)

        y = np.concatenate((y1, y2))

        # Scale the sigmoid function output from 0 to -50
        scaled_y = grey_levels * y - 255 
        # scaled_y = 255 * (y - 1)

    integer_y = [round(float(x)) for x in scaled_y]

    integer_y_all = np.concatenate((integer_y, integer_y[::-1]))

    # Scale the function for dose levels
    dose_all = integer_y_all * nominal_dose / 255
    
    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(x_all, integer_y_all, color='C0')
    plt.plot(x_all, dose_all, color='C1')
    plt.title('Sigmoid function')
    plt.xlabel('x (um)')
    plt.ylabel('Grey level')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    # Get the indices of changes
    indices_of_changes = find_change_indices(integer_y)
    indices_of_changes.insert(0,0)
    radii = np.abs(x_left[indices_of_changes])
    
    # Define radii for each layer of concentric rings
    # radii = np.abs(x[indices_of_changes])  # Outside radii for each of the layers, starting at 255 for the most inner one
    lib = generate_concentric_rings((0, 0), radii[::-1])
    generate_save_gds(name, lib)

#%% GREY-SCALE ANALYSIS AND CONTRAST CURVE
def remove_dose_points(profile_file, removed_begin, removed_end):
    xy_profile, z_profile = read_tab_separated_file(profile_file)
    profile = pd.DataFrame({'xy': xy_profile, 'z': z_profile})
    filtered_profile = profile[(profile['xy'] > profile['xy'].iloc[0] + removed_begin) & 
                               (profile['xy'] < profile['xy'].iloc[-1] - removed_end)]
    new_file = profile_file[:-4] + '_Truncated.txt'
    with open(new_file, 'w') as file:
        for index, row in filtered_profile.iterrows():
            # Create a formatted string for each row
            file.write(f"{row['xy']:3f}\t{row['z']:3f}\n")

def plot_profile_dose(profile_file, shift, dose_file, title, plots):
    xy_profile, z_profile = read_tab_separated_file(profile_file)
    profile = pd.DataFrame({'xy': xy_profile, 'z': z_profile})
    profile['z leveled'] = leveling(profile['xy'], profile['z'])
    profile['xy'] += shift
    if(plots == 1):
        fig1, ax1 = plt.subplots()
        ax1.plot(profile['xy'], profile['z leveled'], marker='.', markersize = 1, linestyle='-', label='Profile [nm]')
        ax1.set_ylabel('z dimension [nm]')
        ax1.set_xlabel('xy dimension [um]')
        plt.legend(loc='lower left')
        ax2 = ax1.twinx()
    xy_dose, dose_value = read_tab_separated_file(dose_file)
    dose = pd.DataFrame({'xy': xy_dose, 'value': dose_value})
    if(plots == 1):
        ax2.plot(dose['xy'], dose['value'], marker='.', markersize = 1, linestyle='-', color = 'black', label='Dose [mJ/cm2]')
        ax2.set_ylabel('Dose [mJ/cm2]')
        plt.title(title)
        plt.legend(loc='lower right')
        plt.grid(True, which='major', axis='both', linestyle='-', linewidth=0.5, alpha=0.5)
        # Set up major grid lines horizontally and vertically
        major_grid_x = np.arange(-2500, 3000, 1000)  # Major grid lines every unit on x-axis
        major_grid_y = np.arange(-600,50,50)  # Major grid lines every 50 on y-axis    
        plt.xticks(major_grid_x)
        plt.yticks(major_grid_y)
        plt.show()
    if(plots == 0):
        return profile, dose

def contrast_curve(filenames, title):
    fig, ax = plt.subplots()
    ax.set_xlabel('Dose [mJ/cm2]')
    ax.set_ylabel('Depth [nm]')
    for file in filenames:
        profile, dose = plot_profile_dose(file[0], file[1], file[2], file[3], 0)
        profile_interp = np.interp(dose['xy'], profile['xy'], profile['z leveled'])
        dose['value'] = [element * -1 for element in dose['value']]
        ax.plot(dose['value'], profile_interp, 'o', markersize = 1, label = file[3])
        ax.legend()
    ax.grid(True)
    ax.set_title(title)
    plt.show()
#%% STONEY EQUATION
def StressStoney(si_thick, film_thick, rad_init, rad_final):
    return 130E9/(6*(1-0.28))*si_thick**2/film_thick*(1/rad_final-1/rad_init)/1E6

#%% HSV ANALYSIS
def plot_csv_data(file_path, start_time, stop_time):
    """
    Reads a CSV file and plots the data from the 'time' column and three specified data columns.

    Parameters:
    - file_path: str, the path to the CSV file.
    - col1, col2, col3: str, the names of the three data columns to be plotted.
    """
    # Read the CSV file
    data = pd.DataFrame(pd.read_csv(file_path, sep=';'))
    
    [data['time (s)'] - start_time for element in data['time (s)']]
    
    # Plotting
    plt.figure(figsize=(10, 6))  # Set the figure size
    plt.plot(data['time (s)'].loc[data['time (s)'] < stop_time - start_time], data['Ch. A Voltage (V)'].loc[(data['time (s)'] > start_time) & (data['time (s)'] < stop_time)], label='Actuator A', linewidth=2)  # Plot the first column
    plt.plot(data['time (s)'].loc[data['time (s)'] < stop_time - start_time], data['Ch. B Voltage (V)'].loc[(data['time (s)'] > start_time) & (data['time (s)'] < stop_time)], label='Actuator B', linewidth=2)  # Plot the second column
    plt.plot(data['time (s)'].loc[data['time (s)'] < stop_time - start_time], data['Ch. C Voltage (V)'].loc[(data['time (s)'] > start_time) & (data['time (s)'] < stop_time)], label='Actuator C', linewidth=2)  # Plot the third column
    plt.xlabel('Time [s]', fontsize="20")  # Label for the x-axis
    plt.ylabel('Voltage [V]', fontsize="20")  # Label for the y-axis
    plt.title('Actuation sequence',fontsize="30")  # Title of the plot
    plt.legend(fontsize="20")  # Show the legend
    plt.xticks(fontsize="16")
    plt.yticks(fontsize="16")
    plt.tight_layout()  # Adjust layout to not overlap items
    plt.grid()
    plt.show()  # Display the plot

def read_tab_separated_file(filename):
    column1 = []
    column2 = []
    with open(filename, 'r') as file:
        for line in file:
            # Split each line into two columns based on tab ('\t') separator
            parts = line.strip().split('\t')
            # Append the first part to column1 and the second part to column2
            column1.append(float(parts[0]))
            column2.append(float(parts[1]))
    return column1, column2

#%% MECHANICAL PROFIMOMETRY
def leveling(x, z):
    # Extract the first and last range of elements
    new_x = pd.concat([x.head(100), x.tail(100)])
    new_z = pd.concat([z.head(100), z.tail(100)])
    coeffs = np.polyfit(new_x, new_z, 1)
    z_level = []
    for i in range(len(x)):
        z_level.append(z[i] - coeffs[0]*x[i] - coeffs[1])
    return pd.DataFrame({'z leveled':z_level})

def leveling_headonly(x, z):
    # Extract the first and last range of elements
    new_x = x.head(100)
    new_z = z.head(100)
    coeffs = np.polyfit(new_x, new_z, 1)
    z_level = []
    for i in range(len(x)):
        z_level.append(z[i] - coeffs[0]*x[i] - coeffs[1])
    return pd.DataFrame({'z leveled':z_level})

def plot_profiles(filenames, title, leveling_opt):
    plt.figure()
    for file in filenames:
        column1, column2 = read_tab_separated_file(file[0])
        data = pd.DataFrame({'xy': column1, 'z': column2})
        if len(file) > 2:
            data['xy'] += file[2]
        if(leveling_opt == 0):
            data['z leveled'] = leveling(data['xy'], data['z'])
        else:
            data['z leveled'] = leveling_headonly(data['xy'], data['z'])
            print('Etching depth = ',np.mean(data['z leveled'].iloc[-100:]))
        plt.plot(data['xy'], data['z leveled'], marker='.', markersize = 1, linestyle='-', label=file[1])
    plt.xlabel('xy dimension [um]')
    plt.ylabel('z dimension [nm]')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_entry_profile_comparison(filenames,title):
    plt.figure()
    for file in filenames:
        column1, column2 = read_tab_separated_file(file[0] + file[1])
        data = pd.DataFrame({'xy': column1, 'z': column2})
        data['z leveled'] = leveling(data['xy'], data['z'], 2)
        plt.plot(data['xy'].loc[(data['xy'] > 400) & (data['xy'] < 1000)], data['z leveled'].loc[(data['xy'] > 400) & (data['xy'] < 1000)], marker='.', markersize = 1, linestyle='-', label=file[2])
    plt.xlabel('xy dimension [um]')
    plt.ylabel('z dimension [nm]')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

def find_dip(values, threshold):
    dip_index = None
    for i in range(len(values)):
        # Check if current value is below the threshold and we haven't started tracking a dip yet
        if values[i] < threshold and dip_index is None:
            dip_index = i  # Start tracking the dip
    return dip_index

def profile_averaging(filenames, title):
    all_profiles = pd.DataFrame()
    for file in filenames:
        column1, column2 = read_tab_separated_file(file[0] + file[1])
        data = pd.DataFrame({'xy': column1, 'z': column2})
        data['z leveled'] = leveling(data['xy'], data['z'], 2)
        ind_move = find_dip(data['z leveled'], - 200) - 400
        data['z leveled'] = data['z leveled'].shift(periods=-ind_move)
        all_profiles = pd.concat([all_profiles, data['z leveled']], axis=1)
        ind_move_reversed = find_dip(data['z leveled'].to_list()[::-1], -200)
    
    # Calculate mean and standard deviation for each column
    means = all_profiles.mean(axis = 1)
    std_devs = all_profiles.std(axis = 1)
    mean_beg = float(means.loc[data['xy'] == 405])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5), sharey=True)
    ax1.plot(data['xy'].loc[(data['xy'] >= 405) & (data['xy'] <= 1000)], means.loc[(data['xy'] >= 405) & 
        (data['xy'] <= 1000)] - mean_beg, color='blue')
    ax1.errorbar(data['xy'].loc[(data['xy'] >= 405) & (data['xy'] <= 1000)], means.loc[(data['xy'] >= 405) & 
        (data['xy'] <= 1000)] - mean_beg, yerr=std_devs.loc[(data['xy'] >= 405) & (data['xy'] <= 1000)], alpha = 0.1, color='blue')
    ax1.set_title('Entry profile')
    ax1.grid()
    ax1.set_xlabel('XY dimension [um]')
    ax1.set_ylabel('Z dimension [nm]')
    
    mean_beg_reversed = float(means.loc[data['xy'] == len(means) - ind_move_reversed - 5])
    ax2.plot(data['xy'].loc[(data['xy'] >= len(means) - ind_move_reversed - 600) & (data['xy'] <= len(means) - ind_move_reversed - 4)], means.loc[(data['xy'] >= len(means) - ind_move_reversed - 600) & 
        (data['xy'] <= len(means) - ind_move_reversed - 4)] - mean_beg_reversed, color='blue')
    ax2.errorbar(data['xy'].loc[(data['xy'] >= len(means) - ind_move_reversed - 600) & (data['xy'] <= len(means) - ind_move_reversed - 4)], means.loc[(data['xy'] >= len(means) - ind_move_reversed - 600) & 
        (data['xy'] <= len(means) - ind_move_reversed -4)] - mean_beg_reversed, yerr=std_devs.loc[(data['xy'] >= len(means) - ind_move_reversed - 600) & (data['xy'] <= len(means) - ind_move_reversed - 4)], alpha = 0.1, color='blue')
    ax2.set_title('Exit profile')
    ax2.grid()
    ax2.set_xlabel('XY dimension [um]')
    ax2.set_ylabel('Z dimension [nm]')
    plt.suptitle(title)
    plt.tight_layout()
    # plt.show()
    return means, std_devs