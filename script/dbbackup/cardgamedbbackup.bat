SET backupFolderPrefix=e:/backup/
set time_hh=%time:~0,2%
if /i %time_hh% LSS 10 (set time_hh=0%time:~1,1%)
SET myDate=%date:~,4%%date:~5,2%%date:~8,2%_%time_hh%%time:~3,2%%time:~6,2%
mysqldbexport --server=root:123456@192.168.0.7 gamecard --export=both>e:/backup/%myDate%db.sql
