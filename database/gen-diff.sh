#!/bin/bash

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <migrationName>"
  exit 1
fi

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 || exit ; pwd -P )"
cd "$SCRIPTPATH" || exit

NAME=$1

HCL_FILE=database.hcl
MIGRATION_DIR=./migrations

atlas migrate diff "$NAME" \
  --dir file://$MIGRATION_DIR \
  --to file://$HCL_FILE \
  --dev-url "docker://mysql/8/personal_cpa" \
  --format '{{ sql . "  " }}'