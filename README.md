# AWS-AMI-Data
A Python3 script to pull all active EC2 instances and their AMIs with one easy to run script.
> **Note:** This utilizes AWS CLI, learn more [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

## Installing:
### Start by cloning the repo
`git clone https://github.com/NotReached/AWS-AMI-Data.git`

### Make sure you're running Python3
`python -v`

### Create a python virtual environment
`python -m venv .venv`

### Connect to the virtual environment
`source .venv/bin/activate`

### Make sure the correct packages are installed
`pip install -r requirements.txt`

### Run main.py
`python main.py`

## Errors:

### No credentials detected in  ~/.aws/credentials
> Follow this guide [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

### You are not authorized to perform this operation. Please check with your IAM Administrator.
> You need to make sure the key you're utilizing has the correct IAM permissions within your AWS accounts to access EC2
