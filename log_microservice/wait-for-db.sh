#!/bin/bash
# wait-for-db.sh

set -e

host="$1"
shift
user="$2"
shift
password="$3"
shift
cmd="$@"

until mysql -h "$host" -u "$user" -p"$password" -e "SELECT 1"; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"
exec $cmd