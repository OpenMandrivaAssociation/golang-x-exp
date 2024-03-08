#!/bin/bash
set -e

if [[ `grep -Es "%bcond_without\sbootstrap2" *.spec` ]]
then
	sh ./golang-package-dependencies.sh
fi
