import pandas as pd

def apply_proper_motion(df, start_year=2025, end_year=2125, step=10):
    frames = []
    years = list(range(start_year, end_year + 1, step))

    for year in years:
        delta_yr = year - start_year
        df_copy = df.copy()
        df_copy['ra_shifted'] = df['ra'] + (df['pmra'] * delta_yr / 3.6e6)
        df_copy['dec_shifted'] = df['dec'] + (df['pmdec'] * delta_yr / 3.6e6)
        df_copy['year'] = year
        frames.append(df_copy)

    return pd.concat(frames)
