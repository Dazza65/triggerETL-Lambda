while getopts p:b: flag
do
        case ${flag} in
                p) profile=${OPTARG};;
                b) bucket=${OPTARG};;
        esac

done

profile=${profile:-default}

if [ ${bucket} ]
then
    echo "Copying triggerETL.zip to S3 bucket ${bucket} for ${profile} profile..."
    aws s3 cp build/triggerETL.zip s3://${bucket}/triggerETL.zip 

    exit $?
else
    echo "Please specify the bucket.  Usage: upload.sh -b <bucket-name> [-p <profile>]"
    exit 1
fi