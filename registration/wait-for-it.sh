#!/usr/bin/env bash
# wait-for-it.sh

set -e

host="$1"
port="$2"
shift 2

until nc -z "$host" "$port"; do
  echo "Esperando pelo serviço em $host:$port..."
  sleep 1
done

exec "$@"
