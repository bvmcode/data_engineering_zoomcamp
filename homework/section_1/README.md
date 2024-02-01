# Question 1

```
docker run --help | grep "remove the container when it exits"
```

### Question 2

```
docker run -it python:3.9 pip list | grep wheel
```

# Questions 3-6

I created the docker services with `docker-compose up -d` in directory `./01-docker-terraform/2_docker_sql`. <br>
I am running this on a GCP box, and my VS Code does auto port forwarding so I had access to pgadmin on 127.0.0.1:8080. <br>

I ran my version of `./01-docker-terraform/2_docker_sql/ingest_data.py` that is capable of using parquet instead of csv.

```
python ingest_data.py \
    -u=root \
    -p=root \
    -H=localhost \
    -P=5432 \
    -d=ny_taxi \
    -t=yellow_taxi_data \
    -U=https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-09.parquet
```

And then the zones data 

```
python ingest_data.py \
    -u=root \
    -p=root \
    -H=localhost \
    -P=5432 \
    -d=ny_taxi \
    -t=zones \
    -U=https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv \
    -e=csv
```


### Question 3

```sql
select count(*)
from public.yellow_taxi_data as td
where cast(lpep_pickup_datetime as date) = '2019-09-18'
and cast(lpep_dropoff_datetime as date) = '2019-09-18';
```

### Question 4

```sql
SELECT lpep_pickup_datetime
FROM public.yellow_taxi_data as td
	 inner join
	 public.zones as p on p."LocationID" = td."PULocationID"
order by trip_distance desc
limit 1;
```

### Question 5

```sql
SELECT p."Borough", sum(total_amount) as total_amount
FROM public.yellow_taxi_data as td
	 inner join
	 public.zones as p on p."LocationID" = td."PULocationID"
where cast(lpep_pickup_datetime as date) = '2019-09-18'
group by  p."Borough"
order by total_amount desc
limit 3;
```

### Question 6

```sql
SELECT d."Zone"
FROM public.yellow_taxi_data as td
	 inner join
	 public.zones as p on p."LocationID" = td."PULocationID"
	 inner join
	 public.zones as d on d."LocationID" = td."DOLocationID"
where  p."Zone" = 'Astoria'
order by tip_amount desc
limit 1;
```

# Question 7

Setup creds on the box with `./gcloud_creds.sh`

```
export GOOGLE_APPLICATION_CREDENTIALS="/home/barry/data-engineering-zoomcamp/keys/creds.json"
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```

Ran the following from `./01-docker-terraform/1_terraform_gcp/terraform/terraform_with_variables`

```
terraform plan
terraform apply
terraform destroy
```


Output from terraform apply

```
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "demo_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = "ny-rides-412820"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.terraform-demo will be created
  + resource "google_storage_bucket" "terraform-demo" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "terraform-demo-412420-bucket"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + rpo                         = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.demo_dataset: Creating...
google_storage_bucket.terraform-demo: Creating...
google_bigquery_dataset.demo_dataset: Creation complete after 1s [id=projects/ny-rides-412820/datasets/demo_dataset]
google_storage_bucket.terraform-demo: Creation complete after 1s [id=terraform-demo-412420-bucket]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```