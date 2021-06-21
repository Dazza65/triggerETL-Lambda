import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'etl_output_bucket'])

output_bucket = args["etl_output_bucket"]

sc = SparkContext()
glueContext = GlueContext(sc)

spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
## @type: DataSource
## @args: [database = "devopskpi", table_name = "kpi_jiradata_json", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "devopskpi", table_name = "kpi_jiradata_json", transformation_ctx = "datasource0")
## @type: ApplyMapping
## @args: [mapping = [("id", "string", "id", "string"), ("key", "string", "key", "int"), ("summary", "string", "summary", "string"), ("datecreated", "string", "datecreated", "date"), ("dateresolved", "string", "dateresolved", "date")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("id", "string", "id", "int"), ("key", "string", "key", "string"), ("summary", "string", "summary", "string"), ("datecreated", "string", "datecreated", "date"), ("dateresolved", "string", "dateresolved", "date")], transformation_ctx = "applymapping1")

## @type: Map
## @args: [f = <function>, transformation_ctx = "<transformation_ctx>"]
## @return: <output>
## @inputs: [frame = <frame>]
def calc_lttd(r):
    r["lttd"] = (r["dateresolved"] - r["datecreated"]).days
    return r
    
newDf = Map.apply(frame = applymapping1, f = calc_lttd, transformation_ctx = "calc_lttd")

newDf.toDF().write.format("json").mode("Overwrite").save("s3://" + output_bucket + "/jira.json")

job.commit()