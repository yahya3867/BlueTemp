# Third Party Imports
import pandas as pd
import numpy as np

def load_csv_data(file, COLUMNS_TO_KEEP):
    sensor_readings_df = pd.read_csv(file) # Load in file.

    # Step 0: Drop unnecessary columns and columns with a date not falling on the hour
    sensor_readings_df = _select_useful_columns(sensor_readings_df, COLUMNS_TO_KEEP)
    sensor_readings_df = sensor_readings_df[sensor_readings_df['date'].str.endswith(':00:00')]
    #print(sensor_readings_df)
    # Step 0.1: Ensure location remains the same
    mean_location = _get_mean_location(sensor_readings_df)
    sensor_readings_df['latitude'] = mean_location[0]
    sensor_readings_df['longitude'] = mean_location[1]

    # Step 1: Add is_original column and set to 1
    sensor_readings_df['is_original'] = 1

    # Step 2: Convert date column to date type
    sensor_readings_df['date'] = pd.to_datetime(sensor_readings_df['date'], format='%Y-%m-%d %H:%M:%S')
    sensor_readings_df = sensor_readings_df.sort_values(by='date').reset_index(drop=True)

    # Step 3: Create a complete date range
    full_range = pd.date_range(start=sensor_readings_df['date'].min(), end=sensor_readings_df['date'].max(), freq='H')
    full_df = pd.DataFrame(full_range, columns=['date'])

    # Step 4: Merge with the original dataframe
    merge_df = pd.merge(full_df, sensor_readings_df, on='date', how='left')
    merge_df['is_original'].fillna(0, inplace=True)  # Set is_original to 0 for new rows

    # Step 5: Fill other columns for new rows with NaN
    for col in set(merge_df.columns) - {'date', 'is_original'}:
        if col not in sensor_readings_df:
            continue
        merge_df[col] = merge_df[col].where(merge_df['is_original'] == 1)

    # Step 7: Mark large gaps in columns - latitude, longitude, sea_water_temperature, and date
    # Step 7.1: latitude
    lat_mark_df = _mark_large_gaps(merge_df, 'latitude', gap_threshold=5)

    # Step 7.2: longitude
    long_mark_df = _mark_large_gaps(lat_mark_df, 'longitude', gap_threshold=5)

    # Step 7.3: Sample measurement
    sea_temp_mark_df = _mark_large_gaps(long_mark_df, 'sea_water_temperature', gap_threshold=5)

    # Step 7.4: Date
    date_mark_df = _mark_large_gaps(sea_temp_mark_df, 'date', gap_threshold=5)

    # Step 7.4: Date
    date_mark_df = _mark_large_gaps(sea_temp_mark_df, 'platform', gap_threshold=5)

    # Step 8: Interpolate small gaps in the columns using linear interpolation
    interpolate_df = _interpolate_missing_values(date_mark_df, COLUMNS_TO_KEEP)

    # Step 9: remove all 24 row blocks with NaN values
    # IK not the best but were on a time crunch
    # Hello tech debt!
    interpolate_df = _cleanse_df_blocks(interpolate_df)

    # Step 10: add a column for future temperature data
    #interpolate_df['future_temp'] = interpolate_df['sea_water_temperature'].shift(-24)
    interpolate_df.drop(interpolate_df.tail(24).index, inplace=True)
    interpolate_df = _select_useful_columns(interpolate_df, COLUMNS_TO_KEEP)
    return interpolate_df

def _select_useful_columns(df, columns_to_keep):
    columns = [col for col in df.columns if col not in columns_to_keep]

    df = df.drop(columns=columns)

    return df


def _get_mean_location(df):
    mean_location = df[['latitude', 'longitude']].mean()

    # Convert to list
    mean_location = mean_location.to_list()

    return mean_location

def _run_length_encoding(df, column_name):
    # Apply RLE: Get run lengths and values
    n = len(df)
    y = np.array(df[f'{column_name}_is_nan'])
    starts = np.r_[0, np.flatnonzero(y[1:] != y[:-1]) + 1]
    lengths = np.diff(np.r_[starts, n])
    values = y[starts]
    return starts, lengths, values

def _mark_large_gaps(df, column_name, gap_threshold=5):
    # Ensure the column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"The column '{column_name}' does not exist in the DataFrame.")

     # Flag rows that are NaN
    df[f'{column_name}_is_nan'] = df[column_name].isna().astype(int)

    # Apply RLE on the column
    starts, lengths, values = _run_length_encoding(df, column_name)

    # Initialize the validity column with ones
    df[f'{column_name}_valid_sequence'] = 1

    # Identify the start positions of large NaN gaps and their lengths
    large_gaps = (values == 1) & (lengths > gap_threshold)

    # Set the validity of sequences following large gaps to 0
    for start, length in zip(starts[large_gaps], lengths[large_gaps]):
        df.loc[start:start+length-1, f'{column_name}_valid_sequence'] = 0

    df.drop([f'{column_name}_is_nan'], axis=1, inplace=True)

    return df

def _interpolate_missing_values(df, columns_to_interpolate):
    # Specify validation columns
    validation_columns = [f'{column}_valid_sequence' for column in columns_to_interpolate]

    # Determine rows eligible for interpolation
    # Only interpolate rows where all associated validation columns are 1
    df['interpolate_flag'] = df[validation_columns].all(axis=1)

    # Iterate over each column that needs interpolation
    for column in columns_to_interpolate:
        if column in df.columns:
            # Use 'mask' to isolate parts of the column that should be interpolated
            # This will replace values where interpolate_flag is 0 with NaN, which are then not interpolated
            mask = df['interpolate_flag'] == 1
            # Temporarily store the original data
            original_data = df[column].copy()
            # Replace data not to be interpolated with NaN
            df.loc[~mask, column] = np.nan
            # Interpolate missing (NaN) values only where the mask is True
            df[column] = df[column].interpolate(method='linear', limit_direction='both')
            # Replace the NaN values back with the original data to avoid affecting non-interpolated parts
            df.loc[~mask, column] = original_data[~mask]

    return df

def _cleanse_df_blocks(df, block_size = 24):
    num_rows = len(df)
    num_full_blocks = num_rows // block_size
    new_num_rows = num_full_blocks * block_size

    # Slice the DataFrame to keep only the rows up to 'new_num_rows'
    df = df.iloc[:new_num_rows]

    # Step 2: Reset the index to ensure it starts from 0 and is sequential
    df = df.reset_index(drop=True)

    # Step 3: Assign block numbers to each row
    df['block'] = df.index // block_size

    # Step 4: Remove blocks that contain any NaN values
    # This function returns True if the block has no NaN values, so it will be kept
    df_cleaned = df.groupby('block').filter(lambda x: not x.isnull().values.any())

    # Step 5: Drop the 'block' column if it's no longer needed
    df_cleaned = df_cleaned.drop(columns=['block'])

    return df_cleaned