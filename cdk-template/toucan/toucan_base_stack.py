import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam

class ToucanBaseStack(cdk.Stack):

    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc = ec2.Vpc(
            self,
            "MyVPC",
            cidr="10.0.0.0/23",
            max_azs=3,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name='Public-Subnet',
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=26
                )
            ]
        )

        # Security Group
        security_group = ec2.SecurityGroup(
            self,
            "RedshiftSG",
            vpc=vpc,
            security_group_name="Redshift_Serverless_SG",
            description="Security group attached to the Redshift Serverless endpoints"
        )

        # Add the security group
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(5439),
            description="Access port 5439 from anywhere"
        )

        # Redshift Serverless IAM role
        redshift_role = iam.Role(
            self,
            'RedshiftRole',
            role_name="Redshift_Serverless_Role",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal('redshift.amazonaws.com'),
                iam.ServicePrincipal('redshift-serverless.amazonaws.com')
            ),
            managed_policies=[
                iam.ManagedPolicy.from_managed_policy_arn(self,'ManagedPolicy',managed_policy_arn='arn:aws:iam::aws:policy/AmazonRedshiftAllCommandsFullAccess'),
                iam.ManagedPolicy.from_managed_policy_arn(self,'ManagedPolicyS3',managed_policy_arn='arn:aws:iam::aws:policy/AmazonS3FullAccess')
            ]
        )

        # Outputs
        cdk.CfnOutput(self,
                      "RedshiftVpc",
                      value=vpc.vpc_id,
                      description="Redshift VPC ID"
                      )

        public_subnets = [subnet.subnet_id for subnet in vpc.public_subnets]
        count=1
        for subnet in public_subnets:
            cdk.CfnOutput(self,
                          f"PublicSubnet{count}",
                          value=subnet,
                          description=f"Public Subnet n°{count}"
                          )
            count += 1

        cdk.CfnOutput(self,
                      "RedshiftSecurityGroup",
                      value=security_group.security_group_id,
                      description="Redshift serverless endpoint security group ID"
                      )

        cdk.CfnOutput(self,
                      "RedshiftIAMRole",
                      value=redshift_role.role_name,
                      description="Redshift IAM role name"
                      )