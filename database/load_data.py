# pip install psycopg2-binary --break-system-packages
#
# Loads touch_grass_map_data.json into the zones/trees/species tables.
# Run schema.sql FIRST to create the tables before running this.

import json
import psycopg2
from psycopg2.extras import execute_values

# ---- Update with your own connection details ----
# Supabase: Project Settings -> Database -> Connection string
# Cloud SQL: Console -> SQL -> your instance -> Overview (also needs your IP authorized,
#            or use the Cloud SQL Auth Proxy)
conn = psycopg2.connect(
    host="[YOUR_HOST]",
    port=5432,
    dbname="[YOUR_DB_NAME]",
    user="[YOUR_USER]",
    password="[YOUR_PASSWORD]"
)
cur = conn.cursor()

with open('touch_grass_map_data.json') as f:
    data = json.load(f)

# ---- Load zones (must load before trees, trees reference zones) ----
zone_rows = [
    (z['cluster_id'], z['center_lat'], z['center_lon'], z['tree_count'], z['precinct'])
    for z in data['zones']
]
execute_values(cur,
    "INSERT INTO zones (cluster_id, center_lat, center_lon, tree_count, precinct) VALUES %s",
    zone_rows
)

# ---- Load trees ----
tree_rows = [
    (t['com_id'], t['common_name'], t['scientific_name'], t['family'],
     t['family_display_category'], t['latitude'], t['longitude'],
     t['display_category'], t['useful_life_expectency'], t['year_planted_display'],
     t['polygon_id'], t['match_type'], t['cluster_id'], t['precinct'], t['located_in'])
    for t in data['trees']
]
execute_values(cur,
    """INSERT INTO trees (com_id, common_name, scientific_name, family,
       family_display_category, latitude, longitude, display_category,
       useful_life_expectency, year_planted_display, polygon_id, match_type,
       cluster_id, precinct, located_in) VALUES %s""",
    tree_rows
)

# ---- Load species (only needed once Epic 3 starts) ----
species_rows = [
    (s['scientific_name'], s['common_name'], s['family'], s['family_display_category'],
     s['display_category'], s['total_count'], json.dumps(s['zone_counts']))
    for s in data['species']
]
execute_values(cur,
    """INSERT INTO species (scientific_name, common_name, family,
       family_display_category, display_category, total_count, zone_counts) VALUES %s""",
    species_rows
)

conn.commit()
print(f"Loaded {len(zone_rows)} zones, {len(tree_rows)} trees, {len(species_rows)} species")
cur.close()
conn.close()
