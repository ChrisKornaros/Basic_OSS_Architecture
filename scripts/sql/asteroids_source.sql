-- Column names and data types taken from the API Exploration Notebook
CREATE TABLE asteroids (
    id VARCHAR,
    neo_reference_id VARCHAR,
    name VARCHAR,
    absolute_magnitude_h DOUBLE,
    is_potentially_hazardous_asteroid BOOLEAN,
    is_sentry_object BOOLEAN,
    estimated_diameter_kilometers_min DOUBLE,
    estimated_diameter_kilometers_max DOUBLE,
    estimated_diameter_meters_min DOUBLE,
    estimated_diameter_meters_max DOUBLE,
    estimated_diameter_miles_min DOUBLE,
    estimated_diameter_miles_max DOUBLE,
    estimated_diameter_feet_min DOUBLE,
    estimated_diameter_feet_max DOUBLE,
    close_approach_date VARCHAR,
    close_approach_date_full VARCHAR,
    epoch_date_close_approach BIGINT,
    kilometers_per_second VARCHAR,
    kilometers_per_hour VARCHAR,
    miles_per_hour VARCHAR,
    astronomical VARCHAR,
    lunar VARCHAR,
    kilometers VARCHAR,
    miles VARCHAR,
    orbiting_body VARCHAR
)


