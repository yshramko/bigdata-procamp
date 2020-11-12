resource "google_composer_environment" "procamp_env" {
  provider = google-beta

  name   = "procamp-env"
  region = var.region
  labels = {
    bigdata-procamp = true
  }

  config {
    node_count = 3

    node_config {
      zone         = var.zone
      machine_type = "n1-standard-1"
      disk_size_gb = 50
    }

    software_config {
      image_version  = var.composer_image_version
      python_version = 3
    }
  }
}