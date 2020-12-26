#!/bin/bash

gitroot=`git rev-parse --show-toplevel`

if [[ $1 == "" ]]; then
	echo "Specify full arn"
	exit
else
	arn="$1"
	region=`echo $arn | cut -d: -f4`
fi

url=$(aws lambda --region $region get-function --function-name $arn | grep Location |  cut -d'"' -f4)
wget -O /tmp/aws.zip "$url"
unzip -o /tmp/aws.zip lambda_function.py -d $gitroot
rm /tmp/aws.zip





