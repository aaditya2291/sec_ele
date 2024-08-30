def get_decoded_df(random_dicts):
    """
        Import the base64 to binary hexadecimal conversion function, then binary hexadecimal to the respective datatypes decoding function
        and apply the conversions here. Then using the decoded data, a dataframe is prepared and returned.
    """
    import pandas as pd
    import random
    import numpy as np
    from idsr.base64_binary_conversion import base64_binary
    from idsr.binary_decode import decode_hex_string
    
    decoded_data = []
    if type(random_dicts) != list:
        random_dicts = [random_dicts]
    for i in random_dicts:
        decoded_data.append(decode_hex_string(base64_binary(i)))

    columns = ['log_type', 'can_bus_number', 'violation_rule_id', 'signal_start_bit', 'signal_length', 'raw_message_length', 'message_can_id', 'detection_time', 'detection_reason', 'duplication_number', 'reserved', 'raw_message_body', 'context_idsr', 'context_binary']
    df = pd.DataFrame(columns=columns)
    for i in decoded_data:
        temp = pd.DataFrame([i])
        df = pd.concat([df, temp])
    df = df.reset_index(drop=True)

    
    df_clean = df.copy()
#     df_clean['log_type'] = df_clean['log_type'].astype(str)
    df_clean['reserved'] = df_clean['reserved'].astype(str)
    df_clean['raw_message_body'] = df_clean['raw_message_body'].astype(str)
    df_clean['log_type'] = df_clean['log_type'].astype(str)
    for i in range(df_clean.shape[0]):
        timestamp = df_clean.loc[i, 'detection_time'].split('-')
        timestamp[0] = '2024'
        timestamp[1] = random.choice(['04', '05', '06'])
        date=str(np.random.randint(1, 30)).zfill(2)
        hour=str(np.random.randint(0, 24)).zfill(2)
        minute=str(np.random.randint(0, 59)).zfill(2)
        second=str(np.random.randint(0, 59)).zfill(2)
        timestamp[2] = f'{date} {hour}:{minute}:{second}'
        df_clean.loc[i, 'detection_time'] = '-'.join(timestamp)
        df_clean.loc[i, 'log_type'] = df_clean.loc[i, 'log_type'].zfill(8)
        df_clean.loc[i, 'violation_rule_id'] = np.random.randint(48, 59)
        df_clean.loc[i, 'signal_start_bit'] = np.random.randint(300, 600)
        df_clean.loc[i, 'duplication_number'] = np.random.randint(0, 50)
    df_clean['detection_time'] = pd.to_datetime(df_clean['detection_time'])
    df_clean = df_clean.sort_values(by='detection_time')
    return df_clean