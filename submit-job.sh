gcloud dataproc jobs submit pyspark \
    --cluster $1 \
    search_job.py $2 $3 $4 $5


## Check the above is synchronous
#gcloud dataproc clusters delete my-dataproc-cluster-name
