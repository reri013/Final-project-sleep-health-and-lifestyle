-- The most common professions
SELECT occupation, COUNT(*) AS count
FROM person
GROUP BY occupation
ORDER BY count DESC;

-- Distribution of ages
SELECT age, COUNT(*) AS count
FROM person
GROUP BY age
ORDER BY age;

-- Distribution of gender
SELECT gender, COUNT(*) AS count
FROM person
GROUP BY gender;

-- AVG hours of sleep grouped by age.
SELECT p.age, ROUND(AVG(qs.sleep_duration), 2) AS avg_sleep_duration
FROM person p
INNER JOIN quality_sleep qs ON p.person_id = qs.person_id
GROUP BY p.age
ORDER BY avg_sleep_duration;

-- AVG quality and hours of sleep  grouped by gender
SELECT p.gender,  ROUND(AVG(qs.quality_of_sleep),2) AS quality_sleep, ROUND(AVG(qs.sleep_duration), 2) AS sleep_duration
FROM person p
INNER JOIN quality_sleep qs ON p.person_id = qs.person_id
GROUP BY p.gender
ORDER BY sleep_duration;

-- AVG quality and hours of sleep according to BMI
SELECT bi.category, ROUND(AVG(qs.quality_of_sleep),2) AS quality_sleep, ROUND(AVG(qs.sleep_duration), 2) AS sleep_duration
FROM quality_sleep qs
INNER JOIN factors f ON f.person_id = qs.person_id
INNER JOIN bmi_index bi ON bi.id_bmi = f.id_bmi
GROUP BY bi.category
ORDER BY quality_sleep DESC;

-- Creat view quality and hours of sleep according to occupation and stess level 
CREATE VIEW quality_sleep_by_occupation_and_stress_level AS
SELECT p.occupation, ROUND(AVG(f.stress_level),2) as avg_stress_level, ROUND(AVG(qs.quality_of_sleep),2) AS quality_sleep, ROUND(AVG(qs.sleep_duration), 2) AS sleep_duration
FROM person p
JOIN quality_sleep qs ON p.person_id = qs.person_id
JOIN factors f ON p.person_id = f.person_id
GROUP BY p.occupation;


-- Create view AVG quality and hours of sleep according to BMI 
CREATE VIEW quality_sleep_by_bmi AS
SELECT bi.category, ROUND(AVG(qs.quality_of_sleep),2) AS quality_sleep, ROUND(AVG(qs.sleep_duration), 2) AS sleep_duration
FROM quality_sleep qs
INNER JOIN factors f ON f.person_id = qs.person_id
INNER JOIN bmi_index bi ON bi.id_bmi = f.id_bmi
GROUP BY bi.category;

-- Quality of sleep according to sleep disorder
SELECT sleep_disorder, ROUND(AVG(quality_of_sleep), 2) AS quality_sleep, ROUND(AVG(sleep_duration), 2) AS sleep_duration
FROM quality_sleep
GROUP BY sleep_disorder
ORDER BY quality_sleep DESC;

--  the average quality of sleep for females who have a physical activity level greater than 40 minutes.
SELECT p.gender, ROUND(AVG(qs.quality_of_sleep), 2) AS avg_quality_of_sleep , ROUND(AVG(sleep_duration), 2) AS sleep_duration
FROM person p
JOIN quality_sleep qs ON p.person_id = qs.person_id
JOIN factors f ON p.person_id = f.person_id
WHERE p.gender = 'female' AND f.physical_activity_level > 40
GROUP BY p.gender;

-- the average quality of sleep and sleep duration for Doctors who have a stress level less than 5.
SELECT p.occupation, ROUND(AVG(qs.quality_of_sleep), 2) AS avg_quality_of_sleep, ROUND(AVG(qs.sleep_duration), 2) AS sleep_duration
FROM person p
JOIN quality_sleep qs ON p.person_id = qs.person_id
JOIN factors f ON p.person_id = f.person_id
WHERE p.occupation = 'Doctor' AND f.stress_level < 5
GROUP BY p.occupation;







