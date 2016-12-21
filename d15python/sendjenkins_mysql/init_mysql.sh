#!/bin/bash
#

PORT="3306"
USERNAME="root"
PASSWORD=""

/usr/bin/mysqld_safe >/dev/null 2>&1 &
sleep 2

SQL1="GRANT ALL ON *.* TO  'admin'@'localhost' identified by 'admin';"
SQL2="GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' IDENTIFIED BY 'admin' WITH GRANT OPTION;"
SQL3="flush privileges;"


/usr/bin/mysql -P${PORT}  -u${USERNAME} -p${PASSWORD} -e "${SQL1}"
/usr/bin/mysql -P${PORT}  -u${USERNAME} -p${PASSWORD} -e "${SQL2}"
/usr/bin/mysql -P${PORT}  -u${USERNAME} -p${PASSWORD} -e "${SQL3}"

mysql_safe_pid=`ps -ef | grep mysqld_safe | head -n1 |awk '{print $2}'`
mysql_pid=`ps -ef | grep /usr/libexec/mysqld | head -n1 |awk '{print $2}'`
kill $mysql_safe_pid
kill $mysql_pid

