import pandas as pd
import sys
import os
import argparse
import re
from lib.preproc_checks import *

preproc_pipeline_dir = '/data/ipl/scratch03/nikhil/MR_preproc_dash/code/nist_mni_pipelines/'
if preproc_pipeline_dir not in sys.path:
    sys.path.append(preproc_pipeline_dir)

def main():
    # Data paths
    
    #argparse
    parser = argparse.ArgumentParser(description = 'Code for preproc checks on dir-tree and output files')
    parser.add_argument('--data_dir', required=True, help='local dataset path')
    parser.add_argument('--save_path', required=True, help='path for summary csv')

    args = parser.parse_args()

    # Req params    
    data_dir = args.data_dir
    save_path = args.save_path
    
    # List of all subject subdirectory names
    subject_names = next(os.walk(data_dir))[1]
    pattern = re.compile("([0-9]*_S_[0-9]*)")
    
    
    # iterate thru all subjects 
    df_preproc = pd.DataFrame()
    
    for subject_name in subject_names:
        if not pattern.match(subject_name):
            print('\ndirectory name {} does not match subject naming convention'.format(subject_name))
        else:
            subject_dir = data_dir + subject_name + '/'
            pipeline_data_pickle = pd.read_pickle(subject_dir + '{}.pickle'.format(subject_name))
            
            df = parse_pickle(pipeline_data_pickle,output_dirs)
            
            df, missing_tp, missing_dir = check_output_dirs(df,output_dirs,subject_dir)
            df, missing_file = check_output_files(df,task_file_names_dict,subject_dir)
            
            print('')
            print('---------------------------------------------------------------')
            print('subject: {}'.format(df['subject_idx'].values[0]))
            print('missing timepoints (# {}): \n{}'.format(len(missing_tp),missing_tp))
            print('')
            print('missing dirs (# {}): \n{}'.format(len(missing_dir), missing_dir)) 
            print('')
            print('missing files(# {}): \n{}'.format(len(missing_file),missing_file))
            
            df_preproc = df_preproc.append(df)
        
    print('')
    print('Lenth of df_preproc: {}'.format(len(df_preproc)))
    print('number of subjects: {}'.format(len(set(df_preproc['subject_idx'].values))))
    print('saving summary csv at {}'.format(save_path))
    df_preproc.to_csv(save_path)
    
if __name__ == '__main__':
    rc = main()
    sys.exit(rc)
    
    