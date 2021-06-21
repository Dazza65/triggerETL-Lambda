while getopts p:b: flag
do
        case ${flag} in
                p) profile=${OPTARG};;
        esac
done

profile=${profile:-default}
account=`aws sts --profile ${profile} get-caller-identity | jq --raw-output .Account`

echo "Copying ETL script jira-lttd.py to S3 bucket devopskpi-${account}-etlscript for ${profile} profile..."
aws s3 cp jira-lttd.py s3://devopskpi-${account}-etlscript/ 

exit $?