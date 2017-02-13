#!/bin/bash


prefix=$1

if [[ -n "$prefix" ]]; then
	postgresCmd="git clone http://github.com/postgres/postgres.git"
	apacheCmd="curl -o httpd.tar.gz http://mirror.symnds.com/software/Apache//httpd/httpd-2.4.25.tar.gz"

	
	store="store"
	if [ ! -d "$store" ]; then
		mkdir -p "$store"	
	fi

	cd $store

	echo "starting postgres subshell\n"

	(	
		
       		$postgresCmd
		cd "config/install-sh"



	)

	echo "start apache subshell\n"
	(
	       	$apacheCmd
		gzip -d httpd.tar.gz
		tar xvf httpd.tar
		cd httpd-2.4.25
		mkdir "$prefix/bin/apachectl"
		./configure --prefix=$PWD'/'$prefix

		make
		make install 
		#Prefix/bin/apachectl -k start
	)

	echo -e "Running: \n$ $postgresCmd"
	echo -e "Running: \n$ $apacheCmd"

	echo -e "placing files in directory $prefix"
	exit 0
else
	echo "no directory prefix provided"
	exit 1 

fi
