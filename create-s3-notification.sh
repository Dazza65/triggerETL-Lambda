while getopts p:b: flag
do
        case ${flag} in
                p) profile=${OPTARG};;
        esac
done

profile=${profile:-default}
account=`aws sts --profile ${profile} get-caller-identity | jq --raw-output .Account`

bucketName="devopskpi-${account}-input"

echo ${bucketName}

aws s3api put-bucket-notification-configuration --bucket ${bucketName} --cli-input-json '{ 
    "NotificationConfiguration": {
        "LambdaFunctionConfigurations": [
            {
                "LambdaFunctionArn": "arn:aws:lambda:ap-southeast-2:346327484579:function:DevOpsKpiTriggerETL",
                "Events": [
                    "s3:ObjectCreated:Put"
                ]
            }
        ]
    }
}'

