import pandas as pd
import sys
import os
import argparse
from lib.preproc_checks import *

preproc_pipeline_dir = '/data/ipl/scratch03/nikhil/MR_preproc_dash/code/nist_mni_pipelines/'
if preproc_pipeline_dir not in sys.path:
    sys.path.append(preproc_pipeline_dir)

def main():
    # Data paths (TODO: argparse)
    #proj_dir = '/data/ipl/scratch03/nikhil/MR_preproc_dash/'
    #data_dir = proj_dir + 'mahsa_preproc_test_data/'
    
    #argparse
    parser = argparse.ArgumentParser(description = 'Code for preproc checks on dir-tree and output files')
    parser.add_argument('--data_dir', required=True, help='local dataset path')

    args = parser.parse_args()

    # Req params    
    data_dir = args.data_dir
    
    # List of all subject subdirectory names
    subject_names = next(os.walk(data_dir))[1]
    print('number of subjects in the preproc pipeline: {}'.format(len(subject_names)))
    #subject_dir = data_dir + '052_S_4807/' #for local tests 

    # Expected output directories per timepoint    
    output_dirs = ['clp','clp2','stx','stx2','vbm','cls','add','vol','lng']
    task_file_names_dict = {}
    task_file_names_dict['clp'] = ['clp','den','nuc']
    task_file_names_dict['clp2'] = ['clp2']
    task_file_names_dict['cls'] = ['csl','lob']
    task_file_names_dict['stx'] = ['stx','nsstx']
    task_file_names_dict['stx2'] = ['stx2']
    
    # iterate thru all subjects 
    df_preproc = pd.DataFrame()
    for subject_name in subject_names:
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
        
    print('Lenth of df_preproc: {}'.format(len(df_preproc)))
    
if __name__ == '__main__':
    rc = main()
    sys.exit(rc)
    
    