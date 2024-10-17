-- Lists all bands with 'Glam rock' as their main style, ranked by their longevity
-- Column names: 'band_name' and 'lifespan' (in years until 2022, use 2022 instead of YEAR(CURDATE())
-- Attributes for computing 'lifespan': 'formed' and 'split'
SELECT band_name, IFNULL(split, 2020) - IFNULL(formed, 0) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', style)
ORDER BY lifespan DESC;
