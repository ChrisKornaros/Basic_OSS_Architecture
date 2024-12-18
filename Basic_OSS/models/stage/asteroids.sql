-- Column names and data types taken from the API Exploration Notebook
WITH a_raw AS (
    SELECT *
    FROM main.asteroids
)

SELECT id, neo_reference_id, name, close_approach_date, close_approach_date_full, epoch_date_close_approach
    , absolute_magnitude_h, is_potentially_hazardous_asteroid, is_sentry_object    
    , kilometers_per_second, kilometers_per_hour, miles_per_hour, astronomical, lunar, kilometers, miles, orbiting_body
    , "estimated_diameter.kilometers.estimated_diameter_min" AS km_estimated_diameter_min
    , "estimated_diameter.kilometers.estimated_diameter_max"AS km_estimated_diameter_max                                                                                 
    , "estimated_diameter.meters.estimated_diameter_min" AS meters_estimated_diameter_min
    , "estimated_diameter.meters.estimated_diameter_max" AS meters_estimated_diameter_max
    , "estimated_diameter.miles.estimated_diameter_min" AS miles_estimated_diameter_min
    , "estimated_diameter.miles.estimated_diameter_max" AS miles_estimated_diameter_max      
    , "estimated_diameter.feet.estimated_diameter_min" AS feet_estimated_diameter_min    
    , "estimated_diameter.feet.estimated_diameter_max" AS feet_estimated_diameter_max
FROM a_raw