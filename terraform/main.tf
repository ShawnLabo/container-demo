resource "google_container_registry" "registry" {
    depends_on = [google_project_service.containerregistry]
}

resource "google_storage_bucket_iam_member" "viewer" {
    bucket = google_container_registry.registry.id
    role = "roles/storage.objectViewer"
    member = "allUsers"
}

resource "google_container_cluster" "demo-cluster" {
    name = "demo-cluster"
    location = var.region
    initial_node_count = 1

    depends_on = [google_project_service.container]
}