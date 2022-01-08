#!/bin/bash

# Run as `./run-cluster-locally.sh debug` in case you want to run it in a debug mode

EXTRA=""
if [[ $# -eq 1 ]] ; then
  if [[ $1 -eq "debug" ]] ; then
    EXTRA="-Dorg.gradle.debug=true"
  fi
fi

rm -rf core/build && \
./gradlew :core:shutdownIntegrationServer -PserverHttpPort=4516 -PoperatorOnPremItest=true --stacktrace \
&& ./gradlew clean -PserverHttpPort=4516 :core:startIntegrationServer --stacktrace -PkeepServerRunning=true -PoperatorOnPremItest=true $EXTRA
