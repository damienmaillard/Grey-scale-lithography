#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 13:41:10 2024

@author: damienmaillard
"""

import MyFunctions as mf
    
# GS try 1 quadratic
mf.rings(2000, 1, ['quadratic', 2000000, -0.002], 120, 600, 'test1.gds')

# # GS try 1 sigmoid
# rings(2000, 2, ['sigmoid', 75, 13], 120, 550, 'test1.gds')

# GS try 2    
# rings(1000, 1, ['sigmoid', 35, 13], 218, 550, 'test.gds')

# save_file(np.column_stack((x_all, integer_y_all)), '/Users/damienmaillard/Library/CloudStorage/Box-Box/Fabrication/DM_FABRICATION/1_Clean room/1_StandardFabrication/GreyscaleTests/Test2_HR5/Th_Sigmoid186_550mJ')
# save_file(np.column_stack((x_all, dose_all)), '/Users/damienmaillard/Library/CloudStorage/Box-Box/Fabrication/DM_FABRICATION/1_Clean room/1_StandardFabrication/GreyscaleTests/Test2_HR5/Th_DoseSigmoid218_550mJ')
