set -e

VAL=`psql -d qai -U user -t <<_EOF
SELECT 1 FROM information_schema.tables WHERE table_name = 'M_Setting';
_EOF`

if [ $VAL = 1 ]; then
  echo "skip init db"
else
  echo "start db init"
  psql -d qai -U user -f /docker-entrypoint-initdb.d/sql/01_ddl.sql
  psql -d qai -U user -f /docker-entrypoint-initdb.d/sql/02_dml_main.sql
  psql -d qai -U user -f /docker-entrypoint-initdb.d/sql/03_dml_sub.sql
fi

echo "end db init"
