echo "beginning the Docker test Suite"
pwd
mkdir -p $SST_BASE/build/workspace/test
mkdir -p $SST_BASE/build/workspace/test/testOutputs
cd $SST_BASE/build/workspace

pushd test

cp $SST_REFERENCE_ELEMENTS/simpleElementExample/tests/test_simpleRNGComponent_marsaglia.py .
cp $SST_REFERENCE_ELEMENTS/simpleElementExample/tests/refFiles/test_simpleRNGComponent_marsaglia.out .

## elements/simpleElementExample/tests/test_simpleRNGComponent_marsaglia.py
## test_simpleRNGComponent_marsaglia.out

cp $SST_REFERENCE_ELEMENTS/memHierarchy/tests/testIncoherent.py .
ls -l testIncoherent.py
cp  $SST_REFERENCE_ELEMENTS/memHierarchy/tests/refFiles/test_memHA_Incoherent.out .
cp $SST_TEST_ROOT/testInputFiles/rightWay .

popd


docker run -i -t -v $SST_BASE/build/workspace/test:/build/workspace/test -e LOCAL_USER_ID=`id -u $USER` jwilso/sstalphacontainer:latest /build/workspace/test/rightWay

