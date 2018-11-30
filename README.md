# EBS-snapshot-deletion-Lambda
A lambda function in python that automates the process of deleting EBS snapshots on AWS

Тhis simple python script can be copied into a Lambda function and triggered through CloudWatch events. The code in this repo is set to delete snapshots that are older than 1 year and not made on the 1st or the 15th of the month. As a filter I use a list of snapshots that is owned by my AWS account ID only (of course :) ) and a certain string that is in the description.

Of course, you can edit out anything you want to change (conditions, filters) based on your needs.
