-- List Glam rock bands ranked by longevity
SELECT band_name, 
       IFNULL(
	   CASE
	       WHEN spilt IS NOT NULL split - formed
	       ELSE 2022 - formed
	   END,
       0) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', style) > 0
ORDER BY lifespan DESC;
