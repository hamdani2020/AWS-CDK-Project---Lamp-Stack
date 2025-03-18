# AWS CDK Project - Lamp Stack

## 📌 Project Description

This project provisions an **Amazon EC2 instance** using **AWS CDK (Python)**. It includes:

- A **publicly accessible EC2 instance**.
- **Monitoring, logging, and observability** using CloudWatch.
- **Automated SSH Key Pair creation** for secure access.

## 🚀 Prerequisites

Ensure you have the following installed:

- **AWS CLI** (Configured with your AWS credentials)
- **AWS CDK** (`npm install -g aws-cdk`)
- **Python 3.8+**
- **pip and virtualenv**
- **Git**

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/AWS-CDK-Project-Lamp-Stack.git
cd LampWatch
```

### 2️⃣ Create a Virtual Environment & Install Dependencies

```sh
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Bootstrap AWS CDK

```sh
cdk bootstrap aws://YOUR_AWS_ACCOUNT_ID/YOUR_AWS_REGION
```

### 4️⃣ Deploy the Stack

```sh
cdk deploy
```

## 🔄 Updating Your Code & Pushing to GitHub

### 1️⃣ Initialize Git (if not already initialized)

```sh
git init
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/AWS-CDK-Project-Lamp-Stack.git
```

### 2️⃣ Add & Commit Your Changes

```sh
git add .
git commit -m "Initial commit - AWS CDK EC2 Provisioning"
```

### 3️⃣ Push to GitHub

```sh
git branch -M main
git push -u origin main
```

## 🛠️ Common Issues & Fixes

### ❌ Error: "CDKToolkit failed creation"

**Solution:** Delete the existing S3 bucket and re-bootstrap.

```sh
aws s3 rb s3://cdk-hnb659fds-assets-YOUR_ACCOUNT-YOUR_REGION --force
cdk bootstrap
```

### ❌ Error: "LogGroup already exists"

**Solution:** Delete the conflicting log group manually in AWS CloudWatch.

```sh
aws logs delete-log-group --log-group-name /aws/ec2/lamp
cdk deploy
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For any inquiries or issues, reach out via hamdanialhassangandi2020\@gmail.com
