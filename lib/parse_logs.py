
import time
import sys
import pandas
import argparse
from datetime import datetime

def create_table(columns):
    # Creates pandas df 
    # Can be switch to SQLite or other DB in future
    _df = pd.Dataframe(columns=columns)
    return _df

########## TODO ##########
def parse_line(line):
    
    line_split = line.split(" ")
    # subject_idx = 
    create_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    # preproc_task = 
    # status = 

    return 

def insert_record(_df, parsed_row):
    # Add a row to pandas df 
    _df.loc[len(_df) + i] = parsed_row
    return _df


def main():
    #argparse
    parser = argparse.ArgumentParser(description = 'Code for parsing MR preproc logs')
    parser.add_argument('--user', required=True, help='user running the piepline')    
    parser.add_argument('--study', required=True, help='name of the study / project')    
    parser.add_argument('--data_dir', required=True, help='local dataset path')   
    parser.add_argument('--logfile', required=True, help='path for reading logfile')    
    parser.add_argument('--save_path', required=True, help='path for saving parsed-log dataframe')    

    args = parser.parse_args()

    # Req params    
    LOG_FILE_A = args.logfile
    df_save_path = args.save_path
    log_tags = ['study','user','subject_idx','log_created','preproc_task','command','status','comments']    


    # Create table to store parsed values 
    log_df = create_table()

    # read logs continuously 
    try:
        f_a = open(LOG_FILE_A, 'r')
        
        while True:
            where_a = f_a.tell()
            line_a = f_a.readline()
        
            if not line_a:
                time.sleep(1)
                f_a.seek(where_a)
                continue
            else:
                line = line_a
                line = line.strip()

                # Use the parse function
                parsed = parse_line(line)

                # Add parsed line as a row to the panda df 
                if len(parsed) > 0:
                    insert_record(line, parsed)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        f_a.close()
        log_df.to_pickle(df_save_path)
        print('saved parsed logs at: {}'.format(df_save_path))
        return 1 


if __name__ == '__main__':
    rc =  main()
    sys.exit( rc )
