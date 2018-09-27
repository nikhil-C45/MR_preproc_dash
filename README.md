# MR_preproc_dash
Dashboard to monitor MR image preproc pipeline status

**Basic workflow**
- run preproc status script anytime after preproc job has been submitted 
- status script
    - input:
        - data_path to preproc dir containing all the subject subdirectories
        - save_path to dump summary csv and dataframe pickle

    - output: status summary as a csv and a dataframe (or color coded dataframe and pairplots in notebook) 
    
- functionality 
    - checks preproc output directory tree for status "exists" or "missing". Note: this is a squential status overwritting process; i.e. "file missing" implies that the subject, timepoint and output directories exists but a particular file is missing. 
        - timepoint dirs (per subject)
        - MR output dirs (per timepoint)
        - MR mnc files (per output dir) 
        
    - extracts registration parameters by inverting registered image (stx, stx2) for each subject and looks for intra-subject (timepoints) outliers. 
    
**Code structure**
- ./lib : useful defs
- ./notebook/MR_preproc_dash_test_code.ipynb: test-run notebook (This will produce color-coded dataframes!!) 
- ./notebook/MR_preproc_dash_registration_metrics.ipynb: notebook for creating reg_param outlier pair-plots
- ./run_test.py command-line code (This will dump summary data to a csv and df pickle) 
    
**Examples**
```
- source /ipl/quarantine/experimental/2013-02-15/init.sh (at BIC) 
- run_test.py:  python run_test.py --data_dir /data/ipl/scratch03/nikhil/MR_preproc_dash/mahsa_preproc_test_data/ --save_path /data/ipl/scratch03/nikhil/MR_preproc_dash/preproc_dash
```
**Limitations**
- Does not QC or check contents of the file during directory tree search

**prerequisites** 
- python 2.7+ (3 preferred)  
- pandas 
- seaborn (for pairplot visuals) 
- https://github.com/vfonov/nist_mni_pipelines (needs iplPatient.py in PYTHONPATH)
