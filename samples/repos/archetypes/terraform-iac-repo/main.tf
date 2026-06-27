resource "local_file" "release_marker" {
  filename = "${path.module}/release-${var.environment}.txt"
  content  = "release proof marker"
}
