#!/bin/sh
# Needed for second stage bootstrapping (first stage bootstrap is installing
# from the binary package): This script builds maven in online mode, creating
# a local repository with all the dependencies (including those that need to
# be built with maven).
#
# (c) 2020 Bernhard Rosenkraenzer <bero@lindev.ch>
# (c) 2024 mandian <mandian@tutanota.com>
# Released under the terms of the GPLv3

cd "`dirname $0`"
NAME="`grep ^Name golang-x-exp.spec |cut -d: -f2- |xargs echo`"
VERSION="`grep ^Version golang-x-exp.spec |cut -d: -f2- |xargs echo`"
URL="`grep ^URL golang-x-exp.spec |cut -d: -f2- |xargs echo`"
SOURCE="`grep ^Source0 golang-x-exp.spec |cut -d: -f2- |sed -e "s,%{name},$NAME,g; s,%{version},$VERSION,g;" |xargs echo`"
MAJOR="`echo $VERSION |cut -d. -f1`"

PKG="`echo $SOURCE |sed -e "s,.*\/,," |xargs echo`"
DIR="`echo $PKG |sed -e "s,\.tar.*,," |xargs echo`"

#export VENDOR=`pwd`/vendor
#rm -rf $VENDOR

[ -e $PKG ] || wget $SOURCE
tar xf $PKG

pushd $DIR 1>/dev/null
go mod vendor

find vendor
tar cf ../vendor.tar vendor
zstd --ultra -22 --rm -f ../vendor.tar

popd 1>/dev/null
rm -rf repository $DIR

exit 0
