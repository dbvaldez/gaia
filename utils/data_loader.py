from astroquery.gaia import Gaia
import pandas as pd

def fetch_gaia_data(limit=1000):
    query = f"""
    SELECT TOP {limit}
        ra, dec, parallax, phot_g_mean_mag, pmra, pmdec, bp_rp
    FROM gaiadr3.gaia_source
    WHERE parallax > 1 AND bp_rp IS NOT NULL AND pmra IS NOT NULL AND pmdec IS NOT NULL
    """
    job = Gaia.launch_job(query)
    df = job.get_results().to_pandas()
    df['distance_pc'] = 1000 / df['parallax']
    return df
