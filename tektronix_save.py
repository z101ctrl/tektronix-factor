def tektronix_save(csv_file, save_path="", json_flag=False):
  """
  Save tektronix type data. 
  ------------------------
  csv_file : csv file to be cleaned.
  save_path : csv save path (without extension).
  json_flag : if True headers file stores as a json file.
  """
  # hardcoded
  rows = 17
  columns = 3

  headers = {}

  # csv file as dataframe
  df = pd.read_csv(csv_file, header=None)

  # select some parts
  df_aux = df.iloc[0:rows,0:columns]
  # drop empty rows
  df_aux = df_aux.dropna(how='all')
  # iter by row of my new df
  for i in range(df_aux.shape[0]):
    # if NaN is found 
    if df_aux.iloc[i,:].isnull().values.any() == True:
      headers[df_aux.iloc[i,0]] = df_aux.iloc[i,1]
    else:
      headers[df_aux.iloc[i,0]] = [df_aux.iloc[i,1], df_aux.iloc[i,2]]

  
  # select some cols  
  final_df = df.iloc[:,3:5]
  # change cols index name
  final_df.columns = [f'Time ({headers["Sample Interval"][1]})', headers["Vertical Units"]]

  # save the files
  if len(save_path) != 0: 
    final_df.to_csv(f'{save_path}.csv')
    if json_flag == True:
      with open(f'{save_path}.txt','w') as fp:
        json.dump(headers, fp)
    else: 
      pd.DataFrame(headers).T.reset_index().to_csv(f'{save_path}_headers.csv', header=False, index=False)
  return headers, final_df
