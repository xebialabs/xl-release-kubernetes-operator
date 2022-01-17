#!/bin/bash

# Run as `./run-cluster-locally.sh debug` in case you want to run it in a debug mode

EXTRA=""
if [[ $# -eq 1 ]] ; then
  if [[ $1 -eq "debug" ]] ; then
    EXTRA="-Dorg.gradle.debug=true"
  fi
fi

 ./gradlew :shutdownIntegrationServer -PoperatorOpenshiftItest=true --stacktrace $EXTRA \
&& ./gradlew clean :startIntegrationServer --stacktrace -PkeepServerRunning=true -PoperatorOpenshiftItest=true $EXTRA
