#!/bin/sh
#############Please put website   
curl -s -o /dev/null -I $1

exit_code=$?

echo $exit_code

if [ $exit_code -eq 0 ]
then
echo "success"
exit 0
else
echo "failed"
exit $exit_code
fi
