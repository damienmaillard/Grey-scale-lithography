#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 11:36:09 2024

@author: damienmaillard
"""

import MyFunctions as mf

main_folder = '/Users/damienmaillard/Library/CloudStorage/Box-Box/Fabrication/DM_FABRICATION/1_Clean room/1_StandardFabrication/GreyscaleTests/Test1_HR2/'

list_files = [[main_folder + 'Quadratic120_550mJ.txt', '120 layers - 550 mJ'],
              [main_folder + 'Quadratic120_600mJ.txt', '120 layers - 600 mJ'],
              [main_folder + 'Quadratic255_550mJ.txt', '255 layers - 550 mJ', 500],
              [main_folder + 'Quadratic255_600mJ.txt', '255 layers - 600 mJ', 500]]
mf.plot_profiles(list_files, 'Greyscale 1 profiles - Quadratic function', 0)

list_files = [[main_folder + 'Sigmoid120_550mJ.txt', '210 layers - 550 mJ'],
              [main_folder + 'Sigmoid120_600mJ.txt', '120 layers - 600 mJ'],
              [main_folder + 'Sigmoid255_550mJ.txt', '255 layers - 550 mJ', 500],
              [main_folder + 'Sigmoid255_600mJ.txt', '255 layers - 600 mJ', 500]]
mf.plot_profiles(list_files, 'Greyscale 1 profiles - Sigmoid function', 0)

#%%
main_folder = '/Users/damienmaillard/Library/CloudStorage/Box-Box/Fabrication/DM_FABRICATION/1_Clean room/1_StandardFabrication/GreyscaleTests/Test1_HR2/'

mf.plot_profile_dose(main_folder + 'Sigmoid255_600mJ.txt', -2060, main_folder + 'Th_DoseSigmoid255_600mJ.txt', 'Greyscale profiles - Sigmoid function, 255 layers, 600 mJ/cm2 base dose', 1)
mf.plot_profile_dose(main_folder + 'Sigmoid120_600mJ.txt', -2500, main_folder + 'Th_DoseSigmoid120_600mJ.txt', 'Greyscale profiles - Sigmoid function, 120 layers, 600 mJ/cm2 base dose', 1)
mf.plot_profile_dose(main_folder + 'Sigmoid255_550mJ.txt', -1990, main_folder + 'Th_DoseSigmoid255_550mJ.txt', 'Greyscale profiles - Sigmoid function, 255 layers, 550 mJ/cm2 base dose', 1)
mf.plot_profile_dose(main_folder + 'Sigmoid120_550mJ.txt', -2520, main_folder + 'Th_DoseSigmoid120_550mJ.txt', 'Greyscale profiles - Sigmoid function, 120 layers, 550 mJ/cm2 base dose', 1)

#%%
mf.plot_profile_dose(main_folder + 'Quadratic255_600mJ.txt', -2010, main_folder + 'Th_DoseQuadratic255_600mJ.txt', 'Greyscale profiles - Quadratic function, 255 layers, 600 mJ/cm2 base dose', 1)
mf.plot_profile_dose(main_folder + 'Quadratic120_600mJ.txt', -2400, main_folder + 'Th_DoseQuadratic120_600mJ.txt', 'Greyscale profiles - Quadratic function, 120 layers, 600 mJ/cm2 base dose', 1)
mf.plot_profile_dose(main_folder + 'Quadratic255_550mJ.txt', -2035, main_folder + 'Th_DoseQuadratic255_550mJ.txt', 'Greyscale profiles - Quadratic function, 255 layers, 550 mJ/cm2 base dose', 1)
mf.plot_profile_dose(main_folder + 'Quadratic120_550mJ.txt', -2415, main_folder + 'Th_DoseQuadratic120_550mJ.txt', 'Greyscale profiles - Quadratic function, 120 layers, 550 mJ/cm2 base dose', 1)

#%% compute contrast curve from dose and depth profile
main_folder = '/Users/damienmaillard/Library/CloudStorage/Box-Box/Fabrication/DM_FABRICATION/1_Clean room/1_StandardFabrication/GreyscaleTests/Test1_HR2/'

mf.contrast_curve([
    [main_folder + 'Sigmoid255_600mJ.txt', -2060, main_folder + 'Th_DoseSigmoid255_600mJ.txt', 'L255, nom600'],
    [main_folder + 'Sigmoid255_550mJ.txt', -1990, main_folder + 'Th_DoseSigmoid255_550mJ.txt', 'L255, nom550'],
    [main_folder + 'Sigmoid120_600mJ.txt', -2500, main_folder + 'Th_DoseSigmoid120_600mJ.txt', 'L120, nom600'],
    [main_folder + 'Sigmoid120_550mJ.txt', -2520, main_folder + 'Th_DoseSigmoid120_550mJ.txt', 'L120, nom550']
    ], 'Sigmoid contrast curve')


#%%
mf.contrast_curve([
    [main_folder + 'Quadratic255_600mJ.txt', -2010, main_folder + 'Th_DoseQuadratic255_600mJ.txt', 'L255, nom600'],
    [main_folder + 'Quadratic255_550mJ.txt', -2035, main_folder + 'Th_DoseQuadratic255_550mJ.txt', 'L255, nom550'],
    [main_folder + 'Quadratic120_600mJ.txt', -2400, main_folder + 'Th_DoseQuadratic120_600mJ.txt', 'L120, nom600'],
    [main_folder + 'Quadratic120_550mJ.txt', -2415, main_folder + 'Th_DoseQuadratic120_550mJ.txt', 'L120, nom550']
    ], 'Quadratic contrast curve')

#%%
main_folder = '/Users/damienmaillard/Library/CloudStorage/Box-Box/Fabrication/DM_FABRICATION/1_Clean room/1_StandardFabrication/GreyscaleTests/Test1_HR2/'

mf.contrast_curve([
    # [main_folder + 'Sigmoid255_600mJ.txt', -2060, main_folder + 'Th_DoseSigmoid255_600mJ.txt', 'L255, nom600'],
    # [main_folder + 'Sigmoid255_550mJ.txt', -1990, main_folder + 'Th_DoseSigmoid255_550mJ.txt', 'L255, nom550'],
    [main_folder + 'Sigmoid120_600mJ.txt', -2500, main_folder + 'Th_DoseSigmoid120_600mJ.txt', 'L120, nom600'],
    [main_folder + 'Sigmoid120_550mJ.txt', -2520, main_folder + 'Th_DoseSigmoid120_550mJ.txt', 'L120, nom550'],
    # [main_folder + 'Quadratic255_600mJ.txt', -2025, main_folder + 'Th_DoseQuadratic255_600mJ.txt', 'L255, nom600'],
    # [main_folder + 'Quadratic255_550mJ.txt', -2035, main_folder + 'Th_DoseQuadratic255_550mJ.txt', 'L255, nom550'],
    [main_folder + 'Quadratic120_600mJ.txt', -2400, main_folder + 'Th_DoseQuadratic120_600mJ.txt', 'L120, nom600'],
    [main_folder + 'Quadratic120_550mJ.txt', -2415, main_folder + 'Th_DoseQuadratic120_550mJ.txt', 'L120, nom550']
    ], 'Greyscale test 1 - sigmoid and quadratic contrast curve 120 layers')


#%% Try 2
main_folder = '/Users/damienmaillard/Library/CloudStorage/Box-Box/Fabrication/DM_FABRICATION/1_Clean room/1_StandardFabrication/GreyscaleTests/Test2_HR5/'

# mf.plot_profile_dose(main_folder + '186Layers_defocus-10.txt', -1275, main_folder + 'Th_DoseSigmoid186_550mJ.txt', 'Greyscale profiles - Sigmoid function, 186 layers, 550 mJ/cm2 base dose', 1)
# mf.plot_profile_dose(main_folder + '186Layers_defocus-5.txt', -1245, main_folder + 'Th_DoseSigmoid186_550mJ.txt', 'Greyscale profiles - Sigmoid function, 186 layers, 550 mJ/cm2 base dose', 1)
# mf.plot_profile_dose(main_folder + '186Layers_defocus0.txt', -1250, main_folder + 'Th_DoseSigmoid186_550mJ.txt', 'Greyscale profiles - Sigmoid function, 186 layers, 550 mJ/cm2 base dose', 1)
# mf.plot_profile_dose(main_folder + '186Layers_defocus+5.txt', -1265, main_folder + 'Th_DoseSigmoid186_550mJ.txt', 'Greyscale profiles - Sigmoid function, 186 layers, 550 mJ/cm2 base dose', 1)
# mf.plot_profile_dose(main_folder + '186Layers_defocus+10.txt', -1255, main_folder + 'Th_DoseSigmoid186_550mJ.txt', 'Greyscale profiles - Sigmoid function, 255 layers, 550 mJ/cm2 base dose', 1)

mf.plot_profiles([
    # [main_folder + '186Layers_defocus-10.txt', '-10 defocus'],
    [main_folder + '186Layers_defocus-5.txt', '-5 defocus'],
    # [main_folder + '186Layers_defocus0.txt', '0 defocus'],
    # [main_folder + '186Layers_defocus+5.txt', '+5 defocus'],
    [main_folder + '186Layers_defocus+10.txt', '+10 defocus'],
    ], 'Greyscale 2 profiles - Sigmoid function with 186 layers - Defocus', 0)

mf.contrast_curve([
    [main_folder + '186Layers_defocus-10.txt', -1275, main_folder + 'Th_DoseSigmoid186_550mJ.txt', 'L186 nom550, defoc-0'],
    [main_folder + '186Layers_defocus-5.txt', -1245, main_folder + 'Th_DoseSigmoid186_550mJ.txt', 'L186, nom550, defoc-5'],
    [main_folder + '186Layers_defocus0.txt', -1250, main_folder + 'Th_DoseSigmoid186_550mJ.txt', 'L186, nom550, defoc0'],
    [main_folder + '186Layers_defocus+5.txt', -1265, main_folder + 'Th_DoseSigmoid186_550mJ.txt', 'L186, nom550, defoc+5'],
    [main_folder + '186Layers_defocus+10.txt', -1255, main_folder + 'Th_DoseSigmoid186_550mJ.txt', 'L186, nom550, defoc+10'],
    ], 'Try 2 Sigmoid contrast curve  186 layers')

#%%
main_folder = '/Users/damienmaillard/Library/CloudStorage/Box-Box/Fabrication/DM_FABRICATION/1_Clean room/1_StandardFabrication/GreyscaleTests/Test2_HR5/'

# mf.plot_profile_dose(main_folder + '218Layers_defocus-10.txt', -1262, main_folder + 'Th_DoseSigmoid218_550mJ.txt', 'Greyscale profiles - Sigmoid function, 218 layers, 550 mJ/cm2 base dose', 1)
# # mf.plot_profile_dose(main_folder + '218Layers_defocus-5.txt', -1258, main_folder + 'Th_DoseSigmoid218_550mJ.txt', 'Greyscale profiles - Sigmoid function, 218 layers, 550 mJ/cm2 base dose', 1)
# # mf.plot_profile_dose(main_folder + '218Layers_defocus0.txt', -1270, main_folder + 'Th_DoseSigmoid218_550mJ.txt', 'Greyscale profiles - Sigmoid function, 218 layers, 550 mJ/cm2 base dose', 1)
# # mf.plot_profile_dose(main_folder + '218Layers_defocus+5.txt', -1260, main_folder + 'Th_DoseSigmoid218_550mJ.txt', 'Greyscale profiles - Sigmoid function, 218 layers, 550 mJ/cm2 base dose', 1)
# # mf.plot_profile_dose(main_folder + '218Layers_defocus+10.txt', -1273, main_folder + 'Th_DoseSigmoid218_550mJ.txt', 'Greyscale profiles - Sigmoid function, 218 layers, 550 mJ/cm2 base dose', 1)

mf.plot_profiles([
    [main_folder + '218Layers_defocus-10.txt', '-10 defocus'],
    [main_folder + '218Layers_defocus-5.txt', '-5 defocus'],
    [main_folder + '218Layers_defocus0.txt', '0 defocus'],
    [main_folder + '218Layers_defocus+5.txt', '+5 defocus'],
    [main_folder + '218Layers_defocus+10.txt', '+10 defocus'],
    ], 'Greyscale 2 profiles - Sigmoid function with 218 layers - Defocus', 0)

mf.contrast_curve([
    [main_folder + '218Layers_defocus-10.txt', -1262, main_folder + 'Th_DoseSigmoid218_550mJ.txt', 'L186 nom550, defoc-10'],
    [main_folder + '218Layers_defocus-5.txt', -1258, main_folder + 'Th_DoseSigmoid218_550mJ.txt', 'L186, nom550, defoc-5'],
    [main_folder + '218Layers_defocus0.txt', -1270, main_folder + 'Th_DoseSigmoid218_550mJ.txt', 'L186, nom550, defoc0'],
    [main_folder + '218Layers_defocus+5.txt', -1260, main_folder + 'Th_DoseSigmoid218_550mJ.txt', 'L186, nom550, defoc+5'],
    [main_folder + '218Layers_defocus+10.txt', -1273, main_folder + 'Th_DoseSigmoid218_550mJ.txt', 'L186, nom550, defoc+10'],
    ], 'Try 2 Sigmoid contrast curve  218 layers')

#%% All the data superimposed
main_folder1 = '/Users/damienmaillard/Library/CloudStorage/Box-Box/Fabrication/DM_FABRICATION/1_Clean room/1_StandardFabrication/GreyscaleTests/Test1_HR2/'
main_folder2 = '/Users/damienmaillard/Library/CloudStorage/Box-Box/Fabrication/DM_FABRICATION/1_Clean room/1_StandardFabrication/GreyscaleTests/Test2_HR5/'
mf.contrast_curve([
    [main_folder1 + 'Sigmoid255_600mJ.txt', -2060, main_folder1 + 'Th_DoseSigmoid255_600mJ.txt', ''],
    [main_folder1 + 'Sigmoid255_550mJ.txt', -1990, main_folder1 + 'Th_DoseSigmoid255_550mJ.txt', ''],
    # [main_folder1 + 'Sigmoid120_600mJ.txt', -2500, main_folder1 + 'Th_DoseSigmoid120_600mJ.txt', ''],
    # [main_folder1 + 'Sigmoid120_550mJ.txt', -2520, main_folder1 + 'Th_DoseSigmoid120_550mJ.txt', ''],
    [main_folder1 + 'Quadratic255_600mJ.txt', -2025, main_folder1 + 'Th_DoseQuadratic255_600mJ.txt', ''],
    [main_folder1 + 'Quadratic255_550mJ.txt', -2035, main_folder1 + 'Th_DoseQuadratic255_550mJ.txt', ''],
    # [main_folder1 + 'Quadratic120_600mJ.txt', -2400, main_folder1 + 'Th_DoseQuadratic120_600mJ.txt', ''],
    # [main_folder1 + 'Quadratic120_550mJ.txt', -2415, main_folder1 + 'Th_DoseQuadratic120_550mJ.txt', ''],
    # [main_folder2 + '186Layers_defocus0.txt', -1250, main_folder2 + 'Th_DoseSigmoid186_550mJ.txt', ''],
    [main_folder2 + '218Layers_defocus0.txt', -1270, main_folder2 + 'Th_DoseSigmoid218_550mJ.txt', ''],
    ], 'Sigmoid and quadratic contrast curve all layers')



