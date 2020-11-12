#!/bin/bash

# This script installs GlobalLogic BigData ProCamp files on a Google Cloud
# Dataproc cluster.

set -euxo pipefail

PROCAMP_DIR=/opt/gl-bigdata-procamp
BITSTAMP_TRUSTSTORE_URL="https://storage.googleapis.com/procamp-infra/initialization-actions/bigdata-procamp/bitstamp.truststore"

function install_and_configure() {
    mkdir ${PROCAMP_DIR}
    chmod 775 ${PROCAMP_DIR}
    wget -P ${PROCAMP_DIR} ${BITSTAMP_TRUSTSTORE_URL}
    chmod 644 ${PROCAMP_DIR}/bitstamp.truststore
}

function main() {
  local role
  role="$(/usr/share/google/get_metadata_value attributes/dataproc-role)"

  # Only run the installation on master nodes
  if [[ "${role}" == 'Master' ]]; then
    install_and_configure
  fi
}

main