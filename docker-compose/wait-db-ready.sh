#!/bin/bash

set -e

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 || exit ; pwd -P )"
cd "$SCRIPTPATH" || exit

echo "MYSQL_DATABASE is $MYSQL_DATABASE"
echo "MYSQL_USERNAME is $MYSQL_USERNAME"
echo "MYSQL_PASSWORD is $MYSQL_PASSWORD"

MYSQL_DATABASE="$MYSQL_DATABASE"
MYSQL_USERNAME="$MYSQL_USERNAME"
MYSQL_PASSWORD="$MYSQL_PASSWORD"

until docker compose exec db-personal-cpa mysql -u"$MYSQL_USERNAME" -p"$MYSQL_PASSWORD" -e "USE $MYSQL_DATABASE; SELECT 1;" >/dev/null 2>&1; do
  echo 'waiting for DB to be ready...'
  sleep 2
done