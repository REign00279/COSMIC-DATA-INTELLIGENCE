
import pandas as pd
import requests
from io import StringIO
from pathlib import Path
from datetime import datetime, timezone

# ------------------------------------------
# COSMIC DATA INTELLIGENCE: NASA ETL PIPELINE
# ------------------------------------------

NASA_API_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
OUTPUT_FILE = Path("exoplanet_dashboard_data.csv")
LOG_FILE = Path("pipeline_log.txt")

QUERY = """
SELECT TOP 5000
    pl_name,
    hostname,
    discoverymethod,
    disc_year,
    pl_rade,
    pl_bmasse,
    pl_orbper
FROM ps
WHERE default_flag = 1
ORDER BY disc_year DESC
"""

def log(message):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{timestamp}] {message}"
    print(line)

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(line + "\n")


def extract_data():
    log("Starting NASA data extraction.")

    response = requests.get(
        NASA_API_URL,
        params={"query": QUERY, "format": "csv"},
        timeout=90
    )
    response.raise_for_status()

    if not response.text.strip():
        raise ValueError("NASA returned an empty response.")

    df = pd.read_csv(StringIO(response.text))

    if df.empty:
        raise ValueError("NASA returned no planet records.")

    log(f"Extracted {len(df)} records from NASA.")
    return df


def transform_data(df):
    log("Starting data cleaning and transformation.")

    df = df.copy()

    # Standardise column names for the dashboard.
    df = df.rename(columns={
        "pl_name": "planet_name",
        "hostname": "host_star_name",
        "discoverymethod": "discovery_method",
        "disc_year": "discovery_year",
        "pl_rade": "planet_radius_earth",
        "pl_bmasse": "planet_mass_earth",
        "pl_orbper": "orbital_period_days"
    })

    # Clean text fields.
    for column in [
        "planet_name",
        "host_star_name",
        "discovery_method"
    ]:
        df[column] = df[column].astype("string").str.strip()
        df[column] = df[column].replace("", pd.NA)

    # Convert measurements to numeric values.
    numeric_columns = [
        "discovery_year",
        "planet_radius_earth",
        "planet_mass_earth",
        "orbital_period_days"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Remove records without essential identifying information.
    df = df.dropna(
        subset=["planet_name", "host_star_name", "discovery_method"]
    )

    # Remove duplicate planet records.
    df = df.drop_duplicates(subset=["planet_name"], keep="first")

    # Invalid measurements become missing rather than zero.
    for column in [
        "planet_radius_earth",
        "planet_mass_earth",
        "orbital_period_days"
    ]:
        df.loc[df[column] <= 0, column] = pd.NA

    # Add descriptive planet-radius categories.
    def radius_category(radius):
        if pd.isna(radius):
            return "Unknown"
        if radius < 0.8:
            return "Sub-Earth"
        if radius <= 1.25:
            return "Earth-sized"
        if radius <= 4:
            return "Super-Earth / Neptune-sized"
        return "Large-radius planet"

    df["radius_category"] = df["planet_radius_earth"].apply(
        radius_category
    )

    # Ensure a valid dataset is available before publishing.
    if len(df) < 100:
        raise ValueError(
            f"Only {len(df)} valid records remain; refusing to publish."
        )

    if df["planet_name"].duplicated().any():
        raise ValueError("Duplicate planet names remain after cleaning.")

    # Keep a consistent column order for the dashboard.
    columns = [
        "planet_id",
        "planet_name",
        "host_star_name",
        "discovery_method",
        "discovery_year",
        "planet_radius_earth",
        "planet_mass_earth",
        "orbital_period_days",
        "radius_category"
    ]

    # Generate a fresh ID for each row in this dataset.
    df = df.reset_index(drop=True)
    df.insert(0, "planet_id", range(1, len(df) + 1))
    df = df[columns]

    log(f"Transformation complete: {len(df)} valid records.")
    log(
        "Missing masses: "
        f"{df['planet_mass_earth'].isna().sum()}"
    )
    log(
        "Missing radii: "
        f"{df['planet_radius_earth'].isna().sum()}"
    )

    return df


def load_data(df):
    log(f"Writing dashboard data to {OUTPUT_FILE}.")
    df.to_csv(OUTPUT_FILE, index=False)
    log(f"Pipeline succeeded. Published {len(df)} records.")


def main():
    try:
        raw_data = extract_data()
        cleaned_data = transform_data(raw_data)
        load_data(cleaned_data)

    except Exception as error:
        log(f"PIPELINE FAILED: {error}")
        raise


if __name__ == "__main__":
    main()
