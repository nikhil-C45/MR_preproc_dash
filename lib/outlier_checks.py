def find_reg_outliers(df,outlier_dirs,cols):
    """finds intra-subject (timepoints) outliers 
    Note: Overwrites outlier_param column value with the latest detected outlier
    """
    df['outlier'] = np.tile(False,len(df))
    df['outlier_param'] = np.tile([''],len(df))
    for subject_idx in df['subject_idx'].unique():
        for od in outlier_dirs: 
            sub_df = df[(df['subject_idx']==subject_idx)&(df['stx']==od)]
            for col in cols:
                reg_vals = np.array(sub_df[['tp', col]].values)
                outliers = outliers_iqr(reg_vals[:,1]) #Take only the reg col

                if len(outliers) > 0:
                    if len(outliers) > 1:
                        outlier_tp = list(np.squeeze(reg_vals[outliers,0]))
                    else:
                        outlier_tp = list(reg_vals[outliers,0][0]) #Avoid zero dimensional array

                    for o_tp in outlier_tp:
                        df.loc[((df['subject_idx']==subject_idx)
                                &(df['tp']==o_tp)&(df['stx']==od)),'outlier'] = True
                        df.loc[((df['subject_idx']==subject_idx)
                                &(df['tp']==o_tp)&(df['stx']==od)),'outlier_param'] += '{}_{}, '.format(od,col)

    return df

def outliers_iqr(ys):
    """ detect outliers based on IQR 
    """
    quartile_1, quartile_3 = np.percentile(ys, [25, 75])
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - (iqr * 1.5)
    upper_bound = quartile_3 + (iqr * 1.5)
    return np.argwhere((ys > upper_bound) | (ys < lower_bound))
