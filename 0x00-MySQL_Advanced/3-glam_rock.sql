-- Lists all bands with 'Glam rock' as their main style, ranked by their
-- longevity.
-- Column names: 'band_name' and 'lifespan'
-- (in years until 2022, use 2022 instead of YEAR(CURDATE())
-- Attributes for computing 'lifespan': 'formed' and 'split'
SELECT name AS band_name,
CASE WHEN split IS NULL THEN 2022 - formed ELSE split - formed
END AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
