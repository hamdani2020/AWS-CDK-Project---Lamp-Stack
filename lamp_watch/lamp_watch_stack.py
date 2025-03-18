from aws_cdk import (
    Duration,
    Stack,  # Duration,
)
from aws_cdk import aws_cloudwatch as cloudwatch  # aws_sqs as sqs,
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_logs as logs
from constructs import Construct


class LampWatchStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "MyVPC", max_azs=2)

        # IAM Role for EC2 with CloudWatch and SSM permissions
        role = iam.Role(
            self,
            "EC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonSSMManagedInstanceCore"
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "CloudWatchAgentServerPolicy"
                ),
            ],
        )

        # Security Group for EC2
        security_group = ec2.SecurityGroup(
            self,
            "LampSG",
            vpc=vpc,
            description="Allow SSH and HTTP access",
            allow_all_outbound=True,
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH"
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP"
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(8080), "Allow HTTP"
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(8081), "Allow HTTP"
        )

        # EC2 Instance
        instance = ec2.Instance(
            self,
            "Lamp",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=security_group,
            role=role,
        )

        # CloudWatch Log Group
        log_group = logs.LogGroup(
            self,
            "EC2LogGroup",
            log_group_name="/aws/ec2/lamp",
            retention=logs.RetentionDays.ONE_WEEK,
        )

        # CloudWatch Metrics
        cpu_metric = cloudwatch.Metric(
            namespace="AWS/EC2",
            metric_name="CPUUtilization",
            dimensions_map={"InstanceId": instance.instance_id},
            period=Duration.minutes(5),
        )

        disk_metric = cloudwatch.Metric(
            namespace="CWAgent",
            metric_name="disk_used_percent",
            dimensions_map={
                "InstanceId": instance.instance_id,
                "device": "xvda1",
                "fstype": "ext4",
            },
            period=Duration.minutes(5),
        )

        # CloudWatch Dashboard
        dashboard = cloudwatch.Dashboard(
            self, "EC2Dashboard", dashboard_name="EC2MonitoringDashboard"
        )
        dashboard.add_widgets(
            cloudwatch.GraphWidget(title="CPU Utilization", left=[cpu_metric]),
            cloudwatch.GraphWidget(title="Disk Usage", left=[disk_metric]),
        )
