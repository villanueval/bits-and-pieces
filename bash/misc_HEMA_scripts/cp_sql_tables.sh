#/bin/bash

mysqldump -u root -p soundsrecs Sample > Sample.sql
mysql -u root -p Scores2009 < Sample.sql
mysql -u root -p Queue < Sample.sql
mysqldump -u root -p soundsrecs Deployment > Dep.sql
mysql -u root -p Scores2009 < Dep.sql 

rm Dep.sql
rm Sample.sql
