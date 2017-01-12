#!/bin/bash


prefix=$1

if [[ -n "$prefix" ]]; then

	postgresCmd="git clone http://github.com/postgres/postgres.git"
	apacheCmd="curl -o httpd.gz http://apache.cs.utah.edu//httpd/-2.4.25.tar.gz"


	if [ ! -d "$prefix" ]; then
		mkdir -p "$prefix"	
	fi

	( cd $prefix; $postgresCmd )
	( cd $prefix; $apacheCmd )

	echo -e "Running: \n$ $postgresCmd"
	echo -e "Running: \n$ $apacheCmd"

	echo -e "placing files in directory $prefix"
	exit 0
else
	echo "no directory prefix provided"
	exit 1 

fi
