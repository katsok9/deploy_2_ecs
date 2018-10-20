# logs.tf

# Set up cloudwatch group and log stream and retain logs for 30 days
resource "aws_cloudwatch_log_group" "log_group" {
  name              = "/ecs/${var.organization}-${var.deployment}-app"
  retention_in_days = 30

  tags {
    Name = "${var.organization}-${var.deployment}-log-group"
  }
}

resource "aws_cloudwatch_log_stream" "cb_log_stream" {
  name           = "${var.organization}-${var.deployment}-log-stream"
  log_group_name = "${aws_cloudwatch_log_group.log_group.name}"
}