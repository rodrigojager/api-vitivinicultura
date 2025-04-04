#!/usr/bin/env bash
set -e

host="$1"
port="$2"
shift 2

until nc -z "$host" "$port"; do
  echo "Aguardando pelo serviço em $host:$port..."
  sleep 1
done

exec "$@"
