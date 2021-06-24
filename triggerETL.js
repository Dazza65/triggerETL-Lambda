const AWSXRay = require('aws-xray-sdk-core');

const { S3Client, GetObjectCommand }  = require('@aws-sdk/client-s3');
const { GlueClient, StartJobRunCommand } = require("@aws-sdk/client-glue");

const s3Client = AWSXRay.captureAWSv3Client(new S3Client({region: process.env.AWS_REGION}));
const glueClient = AWSXRay.captureAWSv3Client(new GlueClient({region: process.env.AWS_REGION}));

const etl_job_map = [{dataFile: "JIRAdata.json", jobName: "kpi-job"}];

const triggerETL = async (s3Params) => {
    try {
        const jobName = etl_job_map.find(job => job.dataFile === s3Params.Key).jobName;

        const data = await s3Client.send(new GetObjectCommand(s3Params));

        if(data.ContentLength > 0) {
            const resp = await glueClient.send(new StartJobRunCommand({JobName: jobName}));
            return resp;
        }
    } catch (err) {
        console.log(message);
        throw new Error(message);
    }
}

exports.handler = async (event, context) => {

    const bucket = event.Records[0].s3.bucket.name;

    const key = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' '));
    const s3Params = {
        Bucket: bucket,
        Key: key,
    }; 
    
    if( key === 'JIRAdata.json') {
        const { JobRunId } = await triggerETL(s3Params);
        console.log(`ETL job trigger with ID: ${JobRunId}`)
    }

};
