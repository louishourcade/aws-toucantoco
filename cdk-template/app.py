#!/usr/bin/env python3
import os

import aws_cdk as cdk

from toucan.toucan_base_stack import ToucanBaseStack

# Variables
aws_acccount = "389737950289"
region = "eu-west-1"


app = cdk.App()

ToucanBaseStack(
    app,
    "ToucanStack",
    env=cdk.Environment(account=aws_acccount, region=region),
    tags={"Project": "RedshiftServerlessToucanBlog"}
    )

app.synth()
