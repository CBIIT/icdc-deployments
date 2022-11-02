## Accessing CBIIT's Approved Base Container Images

CBIIT maintains their lightweight Docker container images in a central account managed by the Cloud One team. Any account within NCI's OU structure has the necessary permissions to be able to pull the images from the central account ECR registry. If using an EC2 instance to pull images, ensure the `ec2-user` is a member of the docker group. 

### Step 1:
Ensure you have Docker and the AWS CLI installed. In theory, this could be performed from AWS CloudShell or from an integration server (EC2 instance) within the requesting account. 


### Step 2: 
An authorization token's permission scope matches that of the IAM principal used to retrieve the authentication token, which will be valid for 12 hours. A request that was successful will return a base64-encoded auth token. Retrieve an auth token using the `aws ecr get-login-password` command, which retrieves and decodes the token that you can pipe into the `docker login` command to authenticate. Run the following using an AWS CLI client:
<pre><code>aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 019211168375.dkr.ecr.us-east-1.amazonaws.com</code></pre>

You may need to retrieve an authentication token and authenticate your Docker client to your own registry to push the image. Run the following command using the AWS CLI:
<pre><code>aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin {account_id}.dkr.ecr.us-east-1.amazonaws.com</code></pre>
Be sure to replace {account_id} with your AWS account number where you're trying to push images to.


### Step 3:
Inspect the CBIIT account for existing repositories and images available in their ECR:
<pre><code>aws ecr describe-repositories</pre></code>
<pre><code>aws ecr describe-images --repository-name {repository_name}</pre></code>
Be sure to replace {repository_name} with the results of the first command executed in this step to view available images.


### Step 4: 
Pull the CBIIT-Managed base images by running the `docker pull` command on any of the available images. Examples include:
<pre><code>docker pull 019211168375.dkr.ecr.us-east-1.amazonaws.com/cbiit-base-docker-images:cbiit-amazon-linux-2
docker pull 019211168375.dkr.ecr.us-east-1.amazonaws.com/cbiit-base-docker-images:cbiit-alpine-linux
docker pull 019211168375.dkr.ecr.us-east-1.amazonaws.com/cbiit-base-docker-images:cbiit-oracle-linux-8
docker pull 019211168375.dkr.ecr.us-east-1.amazonaws.com/cbiit-base-docker-images:cbiit-ubuntu-20.04</code></pre>

