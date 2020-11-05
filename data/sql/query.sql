-- Query for analysis

SELECT 
	year,
	may,
	jun,
	jul,
	ago,
	sep
	
FROM temperatures
WHERE state_id=1;

SELECT 
	year,
	may,
	jun,
	jul,
	ago,
	sep
	
FROM temperatures
WHERE state_id=1;

SELECT * FROM yearly_crop_production
ORDER BY year ASC;

SELECT 
	bb.year,
	bb.value,
	aa.feb,
	aa.mar,
	aa.apr,
	aa.may,
	aa.jun,
	aa.jul,
	aa.ago,
	aa.sep
FROM "temperatures" aa
LEFT JOIN "yearly_crop_production" bb ON aa.state_id=bb.state_id;
ORDER BY bb.year ASC;

SELECT * FROM "yearly_crop_production"
WHERE state_id=1
ORDER BY year ASC;

SELECT * FROM temperatures
WHERE state_id=1
ORDER BY year ASC;


SELECT 
	bb.year,
	bb.value,
	aa.feb,
	aa.mar,
	aa.apr,
	aa.may,
	aa.jun,
	aa.jul,
	aa.ago,
	aa.sep
FROM "temperatures" aa
LEFT JOIN "yearly_crop_production" bb ON aa.state_id=bb.state_id
WHERE aa.state_id=1 AND bb.crop_id=1
ORDER BY year ASC;	

SELECT 
	year,
	feb,
	mar,
	apr,
	may,
	jun,
	jul,
	ago,
	sep
FROM "temperatures" 
WHERE state_id=1
ORDER BY year ASC;

SELECT year, value 
FROM "yearly_crop_production"
WHERE state_id=1 AND crop_id=1
AND year>=2001 
ORDER BY year ASC;
