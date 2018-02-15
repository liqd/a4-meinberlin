#!/bin/bash

set -e
BRANCH=${1:-"master"}
DOCKERTAG=${2:-"meinberlin:dev"}

URL=https://github.com/liqd/a4-meinberlin/archive/${BRANCH}.tar.gz
BASEDIR=a4-meinberlin-${BRANCH}

BUILDDIR=`mktemp -d`
wget -qO- ${URL} | tar xvz -C ${BUILDDIR}

docker build -f ${BUILDDIR}/${BASEDIR}/Dockerfile -t ${DOCKERTAG} ${BUILDDIR}/${BASEDIR}
rm -rf ${BUILDDIR}
