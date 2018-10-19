# provider.tf - Specify the provider and access details

provider "aws" {
  version = "~> 1.41"
  region = "${var.aws_region}"
}
