import pandas as pd
import numpy as np
import sys
import os

# Parse subject -> timepoint info
def parse_pickle(pkl, output_dirs):
    # the task columns represent the current state of the task (na/expected/completed/failed)
    info_cols = ['subject_idx','subject_dir','tp_idx','denoise','mask_N3','advanced_N4','mri3T','model_name',
                'beast_dir','run_skull_registration','beastresolution','number_of_timepoints','pipeline_version',
                'donl','dolngcls','nuc','den','lob','nsstx','qc_dir']
    
    subject_df = pd.DataFrame(columns=info_cols+output_dirs)
    number_of_tp = len(pkl)
    for t, tp in enumerate(pkl.keys()):
    	#Subject sepcific info extracted from pickle 
        subject_df.loc[t,'subject_idx'] = pkl.id
        subject_df.loc[t,'subject_dir'] = pkl.patientdir 
        subject_df.loc[t,'tp_idx'] = tp
        subject_df.loc[t,'denoise'] = pkl.denoise
        subject_df.loc[t,'mask_N3'] = pkl.mask_n3
        subject_df.loc[t,'advanced_N4'] = pkl.n4
        subject_df.loc[t,'donl'] = pkl.donl
        subject_df.loc[t,'dolngcls'] = pkl.dolngcls
        subject_df.loc[t,'mri3T'] = pkl.mri3T
        subject_df.loc[t,'beast_dir'] = pkl.beastdir
        subject_df.loc[t,'model_name'] = pkl.modelname
        subject_df.loc[t,'run_skull_registration'] = pkl.skullreg
        subject_df.loc[t,'beastresolution'] = pkl.beastresolution
        subject_df.loc[t,'number_of_timepoints'] = number_of_tp
        subject_df.loc[t,'pipeline_version'] = pkl.pipeline_version

        #QC dir 
        subject_df.loc[t,'qc'] = True
        
        #Commonly done preproc tasks for each timepoint
        subject_df.loc[t,'nuc'] = True
        subject_df.loc[t,'den'] = True
        subject_df.loc[t,'clp'] = True
        subject_df.loc[t,'clp2'] = True
        subject_df.loc[t,'stx'] = True
        subject_df.loc[t,'nsstx'] = True
        subject_df.loc[t,'stx2'] = True
        subject_df.loc[t,'vbm'] = True
        subject_df.loc[t,'cls'] = True
        subject_df.loc[t,'lob'] = True
        subject_df.loc[t,'add'] = True
        subject_df.loc[t,'vol'] = True
        subject_df.loc[t,'lng'] = True
        
        subject_df = subject_df.replace({True:'expected',False:'na'})
        
    return subject_df
    

# Check diretory tree created at the beginning of the pipeline (catch permission failures)
def check_output_dirs(subject_df,output_dirs,subject_dir):
    #subject_dir = subject_df['subject_dir'].values[0] # on BIC system
    #subject_dir = data_dir + '052_S_4807/' #for local tests 
    
    missing_tp = []
    missing_dir = []

    if os.path.isdir(subject_dir+'qc'):
        subject_df['qc'] = np.tile('qc_exists',len(subject_df))
    else:
        subject_df['qc'] = np.tile('qc_missing',len(subject_df))
        
    for tp in subject_df['tp_idx'].values:
        if os.path.isdir(subject_dir+tp):
            for out_dir in output_dirs:
                if os.path.isdir(subject_dir+tp+'/'+out_dir):
                    subject_df.loc[subject_df['tp_idx']==tp,out_dir] = 'dir_exists'
                else:
                    subject_df.loc[subject_df['tp_idx']==tp,out_dir] = 'dir_missing'
                    missing_dir.append(tp + '/' + out_dir)
        else:
            missing_tp.append(tp)
            subject_df.loc[subject_df['tp_idx']==tp,output_dirs] = 'timepoint_missing'
    
    return subject_df, missing_tp, missing_dir

# Check output files creates at each stage of the pipeline (catch processing errors)
def check_output_files(subject_df,task_file_names_dict,subject_dir):
    missing_file = []
    #subject_dir = subject_df['subject_dir'].values[0] # on BIC system
    #subject_dir = data_dir + '052_S_4807/' #for local tests 
    subject_idx = subject_df['subject_idx'].values[0]
    for tp in subject_df['tp_idx'].values:    
        if os.path.isdir(subject_dir+tp):
            for out_dir in task_file_names_dict.keys():
                expected_files = task_file_names_dict[out_dir]
                for f in expected_files:
                    file_name = '{}_{}_{}_t1.mnc'.format(f,subject_idx,tp) 
                    if os.path.isfile(subject_dir+tp+'/'+out_dir+'/'+file_name):
                        subject_df.loc[subject_df['tp_idx']==tp,out_dir] = 'file_exists'
                    else:
                        subject_df.loc[subject_df['tp_idx']==tp,out_dir] = 'file_missing'
                        missing_file.append(tp + '/' + out_dir + '/' + file_name) 
    return subject_df, missing_file


# Styling for visualization 
def highlight_missing_tp(s):
    '''
    highlight the missing timepoints.
    '''
    is_missing = s == 'timepoint_missing'
    return ['background-color: darkorange' if v else '' for v in is_missing]

def color_missing_dir(val):
    """
    highlight the missing dirs.
    """
    color = 'red' if val in ['dir_missing','file_missing','qc_missing'] else 'black'
    return 'color: %s' % color