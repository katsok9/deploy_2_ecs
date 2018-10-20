[
{
"name": "${organization}-${deployment}-app",
"image": "${app_image}",
"cpu": ${fargate_cpu},
"memory": ${fargate_memory},
"networkMode": "awsvpc",
"logConfiguration": {
"logDriver": "awslogs",
"options": {
"awslogs-group": "/ecs/${organization}-${deployment}-app",
"awslogs-region": "${aws_region}",
"awslogs-stream-prefix": "ecs"
}
},
"portMappings": [
{
"containerPort": ${app_port},
"hostPort": ${app_port}
}
]
}
]