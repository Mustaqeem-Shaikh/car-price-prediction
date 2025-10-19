import boto3
import base64
import docker
import os

class ECRDeployBoto3:
    def __init__(self,image_name,aws_region,aws_account_id):
        self.image_name=image_name
        self.aws_region=aws_region
        self.aws_account_id=aws_account_id
        self.ecr_uri=f"{aws_account_id}.dkr.ecr.{aws_region}.amazon.com/{image_name}"
        self.ecr_client= boto3.client("ecr",region_name=aws_region)

    def login_ecr(self):
        token=self.ecr_client.get_authorization_token()
        username,password=base64.b64code(
            token['authoziationData'][0]["authoziationToken"]
        ).decode().split(":")
        ecr_url= token['authorizationData'][0]['proxyendpoint']

        #docker sdk login
        client=docker.from_env()
        client.login(username=username,password=password,registry=ecr_url)
        print(f"logged in to ecr: {ecr_url}")

    def build_and_push(self):
        client=docker.from_env()
        image,_=client.images.build(path=".",tag=self.image_name)
        image.tag(self.ecr_uri,tag="latest")
        client.images.push(self.ecr_uri,tag="latest")
        print(f" image pushed to {self.ecr_uri}:latest")


if __name__=="__main__":
    deploy=ECRDeployBoto3(
        image_name="car-price-prediction",
        aws_region=os.getenv("AWS_REGION"),
        aws_account_id=os.getenv("AWS_ACCOUNT_ID")
    )
    deploy.login_ecr()
    deploy.build_and_push()