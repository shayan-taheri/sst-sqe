#!/bin/bash
# Run the sst-build utility
pushd buildsys
./sst-build.sh $1
popd