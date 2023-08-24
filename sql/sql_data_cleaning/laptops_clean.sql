-- DATA CLEANING OF LAPTOPS DATASETS

USE clean;
SELECT * FROM laptops;

CREATE TABLE backup_laptops AS
SELECT * FROM backup_laptops;

ALTER TABLE laptops
DROP COLUMN `Unnamed: 0`;

UPDATE laptops
SET Company = LOWER(Company);
SELECT * FROM laptops;
set sql_safe_updates = 0;

SELECT DISTINCT TypeName FROM laptops;
SELECT * FROM laptops WHERE TypeName = 'Notebook';

SELECT Cpu, SUBSTRING_INDEX(Cpu, " ",1) AS "first",REPLACE(SUBSTRING_INDEX(Cpu, " ", -1),"GHz","") AS "words",
REPLACE(Cpu,SUBSTRING_INDEX(Cpu, " ",-1),"") FROM laptops;

ALTER TABLE laptops ADD COLUMN cpu_type VARCHAR(40) AFTER ScreenResolution;

UPDATE laptops SET processor_brand = SUBSTRING_INDEX(Cpu, " ",1);

SELECT DATA_LENGTH FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = "clean";

SELECT * FROM laptops WHERE Price IS NULL;
ALTER TABLE laptops ADD COLUMN processor VARCHAR(40) AFTER processor_brand, ADD COLUMN processor_speed DECIMAL(10,2) AFTER processor;
ALTER TABLE laptops DROP COLUMN processor_speed, DROP COLUMN processor;
ALTER TABLE laptops RENAME COLUMN cpu_type TO processor_brand;

UPDATE laptops
SET processor = REPLACE(Cpu,SUBSTRING_INDEX(Cpu, " ",-1),""),
processor_speed =REPLACE(SUBSTRING_INDEX(Cpu, " ", -1),"GHz","");

SELECT ScreenResolution, SUBSTRING_INDEX(ScreenResolution," ",-1) FROM laptops;
ALTER TABLE laptops ADD COLUMN resolution VARCHAR(40) AFTER Inches;
UPDATE laptops SET resolution = SUBSTRING_INDEX(ScreenResolution," ",-1);
ALTER TABLE laptops DROP COLUMN ScreenResolution, DROP COLUMN Cpu;

SELECT Ram ,REPLACE(Ram, "GB","")FROM laptops;
ALTER TABLE laptops MODIFY COLUMN Ram INteger;
UPDATE laptops SET Ram = REPLACE(Ram, "GB","");

SELECT * FROM laptops;
SELECT DISTINCT Memory FROM laptops;

SELECT * FROM
	(SELECT Memory, SUBSTRING_INDEX(Memory, " ",1) AS 'ram',
	REPLACE(SUBSTRING_INDEX(Memory, "+",-1),SUBSTRING_INDEX(SUBSTRING_INDEX(Memory, "+",-1)," ",-1),"") AS "rom" FROM laptops) t;
        
WITH top_sub AS 
(SELECT Memory,ram,
CASE
    WHEN rom = ram THEN NULL
    ELSE rom
END AS rom
FROM 
(SELECT Memory, SUBSTRING_INDEX(Memory, " ",1) AS 'ram', SUBSTRING_INDEX(TRIM(SUBSTRING_INDEX(Memory,"+",-1))," ",1) as rom FROM laptops) t)
SELECT * FROM top_sub;

ALTER TABLE laptops ADD COLUMN ram VARCHAR(40) AFTER Memory,
ADD COLUMN rom VARCHAR(255) AFTER ram;

SELECT * FROM laptops;
SELECT Memory FROM laptops;

SELECT Memory, SUBSTRING_INDEX(Memory, " ",1) AS 'ram', SUBSTRING_INDEX(TRIM(SUBSTRING_INDEX(Memory,"+",-1))," ",1) as rom FROM laptops;

ALTER TABLE laptops
ADD COLUMN storage_hdd VARCHAR(40) AFTER Memory, ADD COLUMN storage_sdd VARCHAR(255) AFTER storage_hdd;

SELECT Memory , 
	CASE 
	    WHEN Memory LIKE '%SSD%' THEN SUBSTRING_INDEX(Memory, " ",1)
            ELSE NULL
	END AS "memory_type"
FROM laptops;
  
SELECT Memory,storage_sdd, 
CASE
     WHEN TRIM(SUBSTRING_INDEX(Memory,"+",-1)) LIKE '%SSD' THEN NULL 
     ELSE SUBSTRING_INDEX(TRIM(SUBSTRING_INDEX(Memory,"+",-1))," ",1)
END AS "HDD"
FROM laptops;
  
  UPDATE laptops
  SET storage_sdd = CASE 
			WHEN Memory LIKE '%SSD%' THEN SUBSTRING_INDEX(Memory, " ",1)
			ELSE NULL
		     END;
                    
UPDATE laptops
  SET storage_hdd = CASE
			WHEN TRIM(SUBSTRING_INDEX(Memory,"+",-1)) LIKE '%SSD' THEN NULL 
			ELSE SUBSTRING_INDEX(TRIM(SUBSTRING_INDEX(Memory,"+",-1))," ",1)
		     END;

SELECT * FROM laptops;
SELECT Gpu, SUBSTRING_INDEX(Gpu," ",1) AS "gpu_brand" FROM laptops;
ALTER TABLE laptops
ADD COLUMN gpu_brand VARCHAR(50) AFTER storage_sdd;

UPDATE laptops
SET gpu_brand = SUBSTRING_INDEX(Gpu," ",1);
UPDATE laptops
SET gpu_brand = LOWER(gpu_brand);

SELECT DISTINCT OpSys FROM laptops;

SELECT OpSys,
CASE
    WHEN OpSys LIKE '%mac%' THEN 'mac'
    WHEN OpSys LIKE '%Window%' THEN 'windows'
    WHEN OpSys LIKE '%Chrome%' THEN 'chrome'
    WHEN OpSys LIKE '%Android%' THEN 'android'
    WHEN OpSys LIKE '%Linux%' THEN 'linux'
    ELSE 'other'
END AS "operating_sys"
FROM laptops;

UPDATE laptops 
SET OpSys = CASE
		WHEN OpSys LIKE '%mac%' THEN 'mac'
		WHEN OpSys LIKE '%Window%' THEN 'windows'
		WHEN OpSys LIKE '%Chrome%' THEN 'chrome'
		WHEN OpSys LIKE '%Android%' THEN 'android'
		WHEN OpSys LIKE '%Linux%' THEN 'linux'
		ELSE 'other'
	      END;
            
SELECT * FROM laptops;

SELECT Weight,REPLACE(Weight,"kg","") FROM laptops;
UPDATE laptops
SET Weight = REPLACE(Weight,"kg","");

SELECT storage_hdd,storage_sdd,
CASE
    WHEN storage_hdd LIKE '%TB%' THEN REPLACE(storage_hdd,"TB","")*1024
    ELSE REPLACE(storage_hdd,"GB","")
END AS "hdd_format",
CASE
    WHEN storage_sdd LIKE '%TB%' THEN REPLACE(storage_sdd,"TB","")*1024
    ELSE REPLACE(storage_sdd,"GB","")
END AS "ssd_format"
FROM laptops;

UPDATE laptops
SET storage_hdd = CASE
			WHEN storage_hdd LIKE '%TB%' THEN REPLACE(storage_hdd,"TB","")*1024
			ELSE REPLACE(storage_hdd,"GB","")
		   END,
storage_sdd = CASE
		   WHEN storage_sdd LIKE '%TB%' THEN REPLACE(storage_sdd,"TB","")*1024
		   ELSE REPLACE(storage_sdd,"GB","")
	      END;

SELECT * FROM laptops;
SHOW DATABASES;

UPDATE laptops
SET storage_hdd = 0 WHERE storage_hdd IS NULL;
UPDATE laptops
SET storage_sdd = 0 WHERE storage_sdd IS NULL;
UPDATE laptops
SET Weight = 0 WHERE Weight = '?';
UPDATE laptops
SET storage_hdd = 0 WHERE storage_hdd = '?';

SELECT COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = "clean" AND TABLE_NAME = 'laptops';

ALTER TABLE laptops 
MODIFY COLUMN Company VARCHAR(255),
MODIFY COLUMN Gpu VARCHAR(255),
MODIFY COLUMN OpSys VARCHAR(255),
MODIFY COLUMN TypeName VARCHAR(255),
MODIFY COLUMN Weight DECIMAL(4,2),
MODIFY COLUMN Inches DECIMAL(3,1),
MODIFY COLUMN Price INTEGER,
MODIFY COLUMN storage_hdd INTEGER,
MODIFY COLUMN storage_sdd INTEGER;

SELECT * FROM laptops;
SELECT TABLE_NAME,DATA_LENGTH/1024 FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = "clean";