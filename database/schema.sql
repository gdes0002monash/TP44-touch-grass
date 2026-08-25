-- Touch Grass database schema
-- Populated from touch_grass_map_data.json (see Tree_Canopy_DataWrangling.ipynb for how it was built)

-- Zones: one row per 100m grid zone
CREATE TABLE zones (
    cluster_id TEXT PRIMARY KEY,
    center_lat DOUBLE PRECISION NOT NULL,
    center_lon DOUBLE PRECISION NOT NULL,
    tree_count INTEGER NOT NULL,
    precinct TEXT NOT NULL
);

-- Trees: one row per individual tree
CREATE TABLE trees (
    com_id INTEGER PRIMARY KEY,
    common_name TEXT NOT NULL,
    scientific_name TEXT NOT NULL,
    family TEXT NOT NULL,
    family_display_category TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    display_category TEXT NOT NULL,
    useful_life_expectency TEXT,
    year_planted_display TEXT,
    polygon_id DOUBLE PRECISION,          -- nullable: 15 trees have no canopy match
    match_type TEXT NOT NULL,
    cluster_id TEXT REFERENCES zones(cluster_id),
    precinct TEXT NOT NULL,
    located_in TEXT NOT NULL
);

-- Species: one row per distinct species (pre-aggregated for Tree Explorer, Epic 3)
CREATE TABLE species (
    scientific_name TEXT PRIMARY KEY,
    common_name TEXT NOT NULL,
    family TEXT NOT NULL,
    family_display_category TEXT NOT NULL,
    display_category TEXT NOT NULL,
    total_count INTEGER NOT NULL,
    zone_counts JSONB NOT NULL             -- e.g. [{"cluster_id": "...", "count": 12}, ...]
);

-- Indexes for the filters/searches our epics actually use
CREATE INDEX idx_trees_precinct ON trees(precinct);
CREATE INDEX idx_trees_cluster_id ON trees(cluster_id);
CREATE INDEX idx_trees_display_category ON trees(display_category);
CREATE INDEX idx_zones_precinct ON zones(precinct);
