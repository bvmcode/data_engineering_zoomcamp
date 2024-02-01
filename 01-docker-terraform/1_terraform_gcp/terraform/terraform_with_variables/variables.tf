
variable "project" {
  description = "gcs project"
  default     = "ny-rides-412820"
}

variable "location" {
  description = "gcs location location"
  default     = "US"
}

variable "region" {
  description = "gcs reg"
  default     = "us-central1"
}

variable "bg_dataset_name" {
  description = "big query dataset name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "bucket name"
  default     = "terraform-demo-412420-bucket"

}

variable "gcs_storage_class" {
  description = "bucket storage class"
  default     = "STANDARD"

}