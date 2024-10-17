-- Lists all bands with 'Glam rock' as their main style, ranked by their longevity
-- Column names: 'band_name' and 'lifespan' (in years until 2022, use 2022 instead of YEAR(CURDATE())
-- Attributes for computing 'lifespan': 'formed' and 'split'
SELECT band_name, ifnull(split, 2020)-ifnull(formed, 0) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC
