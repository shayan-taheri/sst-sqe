#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------
# Function: dotests
# Description:
#   Purpose:
#       Based on build type and architecture, run tests
#   Input:
#       $1 (build type): kind of build to run tests for
#   Output: none
#   Return value: 0 if success

###-BEGIN-DOTESTS
def dotests(buildType, compilierType = None):
   
    # Build type is available as SST_BUILD_TYPE global, if
    # needed to be selective about the tests that are run.

    # NOTE: Bamboo does a fresh checkout of code each time, so there
    # are no residuals left over from the last build. The directories
    # initialized here are ephemeral, and not kept in CM/SVN.

    #  Want to remove the external environment variables that have been added
    #  in bamboo to the LD_LIBRARY_PATH.
    #  For the tests, they should come from the sst wrapper not from bamboo.sh!
    #    May 2015 - is believed only CHDL and hybridsim tests require the 
    #               SST_DEPS_INSTAL_xxxx `external element environment variables.

    #  Second parameter is compiler choice, if non-default.
    #  If it is Intel, Need a GCC library also
    #    Going to load the gcc-4.8.1 module for now
 
#    export JENKINS_PROJECT=`echo $WORKSPACE | awk -F'/' '{print $6}'`
#    export BAMBOO_SCENARIO=$1

#    echo " #####################################################"
#    echo "parameter \$2 is $2  "
#    echo " #####################################################"

#    if [[ ${SST_MULTI_THREAD_COUNT:+isSet} == isSet ]] ||
#       [[ ${SST_MULTI_RANK_COUNT:+isSet} == isSet ]] ; then
#    #    This subroutine is in test/include/testDefinitions.sh
#    #    (It is a subroutine, but testSubroutines is only sourced
#    #        into test Suites, not bamboo.sh.
#         multithread_multirank_patch_Suites
#    fi
    
#    #       Recover library path
#    export LD_LIBRARY_PATH=$SAVE_LIBRARY_PATH
#    export DYLD_LIBRARY_PATH=$LD_LIBRARY_PATH 
#
#    echo "     LD_LIBRARY_PATH includes:"
#    echo $LD_LIBRARY_PATH | sed 's/:/\n/g'
#    echo ' '

#    # Initialize directory to hold testOutputs
#    rm -Rf ${SST_TEST_OUTPUTS}
#    mkdir -p ${SST_TEST_OUTPUTS}
#
#    # Initialize directory to hold Bamboo-compatible XML test results
#    rm -Rf ${SST_TEST_RESULTS}
#    mkdir -p ${SST_TEST_RESULTS}
#
#    # Initialize directory to hold temporary test input files
#    rm -Rf ${SST_TEST_INPUTS_TEMP}
#    mkdir -p ${SST_TEST_INPUTS_TEMP}

#    if [[ $1 == *sstmainline_config_test_output_config* ]]
#    then
#        ./test/utilities/Build-output-config-check
#        pwd
#        ls -l run.for.output.config
#        ./run.for.output.config
#        return
#    fi
#
#    #   Enable the --output-config option in (most) tests
#    #      (activated by Environment Variable)
#
#    if [[ ${SST_TEST_OUTPUT_CONFIG:+isSet} == isSet ]] ; then
#        echo ' '; echo "Generating \"--output-config\" test" ; echo ' '
#        ./test/utilities/GenerateOutputConfigTest
#    fi

#    # Run test suites
#
#    # DO NOT pass args to the test suite, it confuses
#    # shunit. Use an environment variable instead.
#
#      if [ $1 == "sstmainline_config_all" ] ; then 
#
#         pushd ${SST_ROOT}/test/testSuites
#         echo \$SST_TEST_SUITES = $SST_TEST_SUITES
#         echo "     Content of file, SuitesToOmitFromAll"
#         cat SuitesToOmitFromAll
#         echo ' '
#         ## strip any comment off
#         cat SuitesToOmitFromAll | awk  '{print $1}' > __omitlist__        
#         echo "      Suites to explictly OMIT from the \"all\" scenario:"
#         ls testSuite_*sh | grep  -f __omitlist__
#         echo ' '
#         #   Build the Suite list for the "All" scenario
#         ls testSuite_*sh | grep -v -f __omitlist__ > Suite.list
#         echo "all() {" > files.for.all
#         sed  s\%^%\${SST_TEST_SUITES}/% Suite.list >> files.for.all
#         echo "}" >> files.for.all
#         . files.for.all               # Source the subroutine including list
#         popd
#         all
#         return
#    fi
#    
#    # New CHDL test
#    if [[ ${SST_DEPS_INSTALL_CHDL:+isSet} == isSet ]] ; then
#        ${SST_TEST_SUITES}/testSuite_chdlComponent.sh
#    fi
#
#    if [ $1 == "sstmainline_config_no_gem5" ] ; then
#        ${SST_TEST_SUITES}/testSuite_Ariel.sh
#    fi
#    #
#    #  Run only Streams test only
#    #
#    if [ $1 == "sstmainline_config_stream" ]
#    then
#        ${SST_TEST_SUITES}/testSuite_stream.sh
#        return
#    fi
#
#    #
#    #  Run only openMP 
#    #
#    if [ $1 == "sstmainline_config_openmp" ]
#    then
#        ${SST_TEST_SUITES}/testSuite_Sweep_openMP.sh
#        return
#    fi
#
#    #
#    #  Run only dirSweep3Cache
#    #
#    if [ $1 == "sstmainline_config_dir3cache" ]
#    then
#        ${SST_TEST_SUITES}/testSuite_dir3LevelSweep.sh
#        return
#    fi
#
#    #
#    #  Run only diropenMP 
#    #
#    if [ $1 == "sstmainline_config_diropenmp" ]
#    then
#        ${SST_TEST_SUITES}/testSuite_dirSweep.sh
#        return
#    fi
#
#    #
#    #  Run only dirSweepB
#    #
#    if [ $1 == "sstmainline_config_diropenmpB" ]
#    then
#        ${SST_TEST_SUITES}/testSuite_dirSweepB.sh
#        return
#    fi
#
#    #
#    #  Run only dirSweepI
#    #
#    if [ $1 == "sstmainline_config_diropenmpI" ]
#    then
#        ${SST_TEST_SUITES}/testSuite_dirSweepI.sh
#        return
#    fi
#
#    #
#    #  Run only dir Non Cacheable
#    #
#    if [ $1 == "sstmainline_config_dirnoncacheable" ]
#    then
#        ${SST_TEST_SUITES}/testSuite_dirnoncacheable_openMP.sh
#        return
#    fi
#
#    #
#    #  Run only openMP and memHierarchy 
#    #
#    if [ $1 == "sstmainline_config_memH_only" ]
#    then
#        ${SST_TEST_SUITES}/testSuite_openMP.sh
#        ${SST_TEST_SUITES}/testSuite_memHierarchy_bin.sh
#        return
#    fi
#
#    #
#    #   Test for the new memH via Ariel testing
#    #
#    #   With optional split into two tests
#    #
#    if [ $1 == "sstmainline_config_memH_Ariel" ]
#    then
#        GROUP=0
#        if [[ ${SST_SWEEP_SPLIT:+isSet} == isSet ]] ; then
#            GROUP=${SST_SWEEP_SPLIT}
#        fi
#        if [ $GROUP != 2 ] ; then
#            ${SST_TEST_SUITES}/testSuite_openMP.sh
#            ${SST_TEST_SUITES}/testSuite_diropenMP.sh
#            ${SST_TEST_SUITES}/testSuite_dirSweepB.sh
#            ${SST_TEST_SUITES}/testSuite_dirSweepI.sh
#            ${SST_TEST_SUITES}/testSuite_dirSweep.sh
#        fi
#        if [ $GROUP == 1 ] ; then 
#            return
#        fi
#        ${SST_TEST_SUITES}/testSuite_dirnoncacheable_openMP.sh
#        ${SST_TEST_SUITES}/testSuite_noncacheable_openMP.sh
#        ${SST_TEST_SUITES}/testSuite_Sweep_openMP.sh
#        ${SST_TEST_SUITES}/testSuite_dir3LevelSweep.sh
#        return
#    fi
#
#     #
#     #   Suites that used MemHierarchy, but not openMP
#     #
#
#    if [ $1 == "sstmainline_config_memH_wo_openMP" ]
#    then
#        if [[ $SST_ROOT == *Ariel* ]] ; then
#            pushd ${SST_TEST_SUITES}
#            ln -s ${SST_TEST_SUITES}/testSuite_Ariel.sh testSuite_Ariel_extra.sh
#            ${SST_TEST_SUITES}/testSuite_Ariel_extra.sh
#            popd
#        fi
#        export SST_BUILD_PROSPERO_TRACE_FILE=1
#        pushd ${SST_TEST_SUITES}
#          ln -s ${SST_TEST_SUITES}/testSuite_prospero.sh testSuite_prospero_pin.sh
#          ${SST_TEST_SUITES}/testSuite_prospero_pin.sh
#          unset SST_BUILD_PROSPERO_TRACE_FILE
#        popd
#        ${SST_TEST_SUITES}/testSuite_SiriusZodiacTrace.sh
#        ${SST_TEST_SUITES}/testSuite_embernightly.sh
#        ${SST_TEST_SUITES}/testSuite_BadPort.sh
#        ${SST_TEST_SUITES}/testSuite_memHierarchy_sdl.sh
#        ${SST_TEST_SUITES}/testSuite_memHSieve.sh
#        ${SST_TEST_SUITES}/testSuite_hybridsim.sh
#        ${SST_TEST_SUITES}/testSuite_miranda.sh
#        ${SST_TEST_SUITES}/testSuite_cassini_prefetch.sh
#        ${SST_TEST_SUITES}/testSuite_prospero.sh
#        ${SST_TEST_SUITES}/testSuite_Ariel.sh
#        return
#    fi
#
#    if [ $kernel != "Darwin" ]
#    then
#        # Only run if the OS *isn't* Darwin (MacOS)
#        ${SST_TEST_SUITES}/testSuite_qsimComponent.sh
#    fi
#
#    #  
#    #    Only if macsim was requested
#    #
#    if [ -d ${SST_ROOT}/sst/elements/macsimComponent ] ; then
#         ${SST_TEST_SUITES}/testSuite_macsim.sh
#    fi
#
#    ${SST_TEST_SUITES}/testSuite_Ariel.sh
#    ${SST_TEST_SUITES}/testSuite_hybridsim.sh
#    ${SST_TEST_SUITES}/testSuite_SiriusZodiacTrace.sh
#    ${SST_TEST_SUITES}/testSuite_memHierarchy_sdl.sh
#    ${SST_TEST_SUITES}/testSuite_memHSieve.sh
#
#
#    ${SST_TEST_SUITES}/testSuite_simpleComponent.sh
#    ${SST_TEST_SUITES}/testSuite_simpleLookupTableComponent.sh
#    ${SST_TEST_SUITES}/testSuite_cacheTracer.sh
#    ${SST_TEST_SUITES}/testSuite_miranda.sh
#    ${SST_TEST_SUITES}/testSuite_BadPort.sh
#    ${SST_TEST_SUITES}/testSuite_scheduler.sh
#    ${SST_TEST_SUITES}/testSuite_scheduler_DetailedNetwork.sh
#
#    # Add other test suites here, i.e.
#    # ${SST_TEST_SUITES}/testSuite_moe.sh
#    # ${SST_TEST_SUITES}/testSuite_larry.sh
#    # ${SST_TEST_SUITES}/testSuite_curly.sh
#    # ${SST_TEST_SUITES}/testSuite_shemp.sh
#    # etc.
#
#    ${SST_TEST_SUITES}/testSuite_merlin.sh
#    ${SST_TEST_SUITES}/testSuite_embernightly.sh
# 
#    ${SST_TEST_SUITES}/testSuite_simpleDistribComponent.sh
#    ${SST_TEST_SUITES}/testSuite_EmberSweep.sh
#
#    if [ $1 != "sstmainline_config_no_mpi" ] ; then
#        #  Zoltan test requires MPI to execute.
#        #  sstmainline_config_no_gem5 deliberately omits Zoltan, so must skip test.
#        if [ $1 != "sstmainline_config_linux_with_ariel" ] ; then
#            ${SST_TEST_SUITES}/testSuite_zoltan.sh
#            ${SST_TEST_SUITES}/testSuite_partitioner.sh
#        fi
#    fi
#    ${SST_TEST_SUITES}/testSuite_simpleRNGComponent.sh
#    ${SST_TEST_SUITES}/testSuite_simpleStatisticsComponent.sh
#      
#    if [[ ${INTEL_PIN_DIRECTORY:+isSet} == isSet ]] ; then
#        export SST_BUILD_PROSPERO_TRACE_FILE=1
#        pushd ${SST_TEST_SUITES}
#          ln -s ${SST_TEST_SUITES}/testSuite_prospero.sh testSuite_prospero_pin.sh
#          ${SST_TEST_SUITES}/testSuite_prospero_pin.sh
#          unset SST_BUILD_PROSPERO_TRACE_FILE
#        popd
#    fi
#    ${SST_TEST_SUITES}/testSuite_prospero.sh
##
#    ${SST_TEST_SUITES}/testSuite_check_maxrss.sh
#    ${SST_TEST_SUITES}/testSuite_cassini_prefetch.sh
#    ${SST_TEST_SUITES}/testSuite_simpleMessageGeneratorComponent.sh
#    ${SST_TEST_SUITES}/testSuite_VaultSim.sh
#
#    # Purge SST installation
#    if [[ ${SST_RETAIN_BIN:+isSet} != isSet ]]
#    then
#        rm -Rf ${SST_INSTALL}
#    fi

###-END-DOTESTS

################################################################################
# Run this module as a Test Suite
if __name__ == '__main__':
    pass
