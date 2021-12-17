#!/bin/bash

# Run as `./run-cluster-locally.sh debug` in case you want to run it in a debug mode

EXTRA=""
if [[ $# -eq 1 ]] ; then
  if [[ $1 -eq "debug" ]] ; then
    EXTRA="-Dorg.gradle.debug=true"
  fi
fi

 ./gradlew :core:shutdownIntegrationServer -PserverHttpPort=5516 -PoperatorOnpremItest=true --stacktrace \
&& ./gradlew clean -PserverHttpPort=5516 :core:startIntegrationServer --stacktrace  -PkeepServerRunning=true -PoperatorOnpremItest=true $EXTRA

