def tektronix_save(csv_file, save_path="", json_flag=False):
    """
    Save tektronix type data. 
    ------------------------
    csv_file : csv file to be cleaned.
    save_path : csv save path (without extension).
    json_flag : if True headers file stores as a json file.
    """
    header_dim = [17, 3]
    data_dim = [3, 5]

    dual_channel_offset = 6

    # csv file as dataframe
    df = pd.read_csv(csv_file, header=None)

    # empty lists
    headers = []
    dataframes = []

    channels_amount = len(df.columns)//dual_channel_offset

    for j in range(channels_amount):
        pointer = j*dual_channel_offset
        # create empty header dict
        headers.append({})
        # select some parts
        df_aux = df.iloc[0:header_dim[0],pointer:header_dim[1]+pointer]
        # drop empty rows
        df_aux = df_aux.dropna(how='all')

        for i in range(df_aux.shape[0]):
            # if NaN is found 
            if df_aux.iloc[i,:].isnull().values.any() == True:
                headers[j][df_aux.iloc[i,0]] = df_aux.iloc[i,1]
            else:
                headers[j][df_aux.iloc[i,0]] = [df_aux.iloc[i,1], df_aux.iloc[i,2]]

        # select some cols  
        final_df = df.iloc[:,data_dim[0]+pointer:data_dim[1]+pointer]
        # change cols index name
        final_df.columns = [f'Time ({headers[j]["Sample Interval"][1]})', headers[j]["Vertical Units"]]

        dataframes.append(final_df)

    # save part of the code
    if len(save_path) != 0: 
        for k, df in enumerate(dataframes):
            df.to_csv(f'{save_path}{k}.csv')
            if json_flag == True:
                for header in headers:
                    with open(f'{save_path}{k}.txt','w') as fp:
                            json.dump(header, fp)
            else: 
                for header in headers:
                    pd.DataFrame(headers).T.reset_index().to_csv(f'{save_path}{k}_headers.csv', header=False, index=False)
    return headers, dataframes