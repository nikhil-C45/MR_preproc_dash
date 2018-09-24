import pandas as pd
import numpy as np
import sys
import os
import re
import subprocess

def get_reg_diff(df1,df2):
    return (df1-df2).abs()

def get_subject_reg_parameters(data_dir, script_dir, subject_idx, timepoints, stx):
    reg_param_list = []
    reg_param_flat = pd.DataFrame()
    
    for t,tp in enumerate(timepoints):
        xfm = data_dir + '{}/{}/{}/{}_{}_{}_t1.xfm'.format(subject_idx,tp,stx,stx,subject_idx,tp)
        reg_param = get_reg_params(script_dir, xfm).apply(pd.to_numeric)
        v = reg_param.unstack().to_frame().sort_index(level=1).T
        v.columns = v.columns.map('_'.join)

        v['subject_idx'] = subject_idx
        v['tp'] = tp
        reg_param_flat = reg_param_flat.append(v)
        reg_param_list.append(reg_param)
            
    return reg_param_flat, reg_param_list

def get_xcorr_vol(script_dir,vol1,vol2):
    minc_xcorr_cmd = script_dir + 'run_xcorr_cmd.sh' + ' ' + vol1 + ' ' + vol2
    xcorr = 0
    try:
        xcorr = float(subprocess.check_output(minc_xcorr_cmd, shell=True))
    except:
        print('Could not run minc command. Check minc script / command: \n{}\n'.format(minc_xcorr_cmd))
        
    return xcorr

def get_reg_params(script_dir,xfm):
    minc_reg_param_cmd = script_dir + 'run_reg_param_cmd.sh' + ' ' + xfm
    reg_df = pd.DataFrame(index=['center','translation','rotation','scale','shear'],columns=['x','y','z'])
    string_check = False
    origin_check = False
    
    try: 
        #reg_param_str = str(subprocess.check_output(minc_reg_param_cmd, shell=True),'utf-8')
        reg_param_str = str(subprocess.check_output(minc_reg_param_cmd, shell=True))
        #print(reg_param_str)
        reg_param_split = str.split(reg_param_str,' ')        

        # Check if output string is what you expect
        string_check = ((reg_param_split[3]=='-center') & (reg_param_split[7]=='-translation') & 
                        (reg_param_split[11]=='-rotation') & (reg_param_split[15]=='-scale') & 
                        (reg_param_split[19]=='-shear'))

        # Check if origin = [0,0,0]
        if string_check:
            origin_check = (np.array(reg_param_split[4:7]).astype(float) == [0,0,0]).all()

            if origin_check:
                reg_df.loc['center'] = np.array(reg_param_split[4:7]).astype(float)
                reg_df.loc['translation'] = np.array(reg_param_split[8:11]).astype(float)
                reg_df.loc['rotation'] = np.array(reg_param_split[12:15]).astype(float)
                reg_df.loc['scale'] = np.array(reg_param_split[16:19]).astype(float)
                reg_df.loc['shear'] = np.array(reg_param_split[20:23]).astype(float)
            else:
                print('Origin is not at [0,0,0]. Check input image space.')
        else: 
            print('minc command output string doesnot match expected output from xfm2param')
    except Exception as e: print(e)
        #print('Could not run minc command. Check minc script / command: \n{}\n'.format(minc_reg_param_cmd))

    return reg_df
