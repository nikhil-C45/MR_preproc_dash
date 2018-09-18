# MR_preproc_dash
dashboard to monitor MR image preproc pipelines

**Basic workflow**
- run_job_script: spawns 1) preproc code 2) monitoring script
- monitoring script
    - input: list of subjects
    - optional input: subject metadata, demographic info etc. 
    - list of commands (pipeline steps) 
    - log paths
- log parser 
    - read logs
    - store into panda df
- progress reports 
    - plots
    - suggestions on errors 
    - sync with master table of preproc history (study / dataset / user info) 

**prerequisites** 
- python 3+ 
- pandas 
