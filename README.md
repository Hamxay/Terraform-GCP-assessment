# FastAPI Application Deployment with Terraform on Google Cloud Run

This project demonstrates how to deploy a FastAPI application using Terraform on Google Cloud Run.

## Overview

Google Cloud Run is a fully managed platform that automatically scales your containerized applications. Terraform is an infrastructure as code tool that allows you to define and provision infrastructure resources in a declarative way.

In this project, we use Terraform to provision the necessary infrastructure on Google Cloud Platform (GCP) and deploy a FastAPI application as a containerized service on Google Cloud Run.

## Project Structure

The project includes the following files:

- `main.tf`: Terraform configuration file defining the Google Cloud Run service.
- `provider.tf`: Terraform configuration file defining the provider and project settings.
- `variables.tf`: Terraform configuration file defining input variables.
- `Dockerfile`: Dockerfile for building the container image for the FastAPI application.
- `requirements.txt`: Python dependencies required for the FastAPI application.
- `main.py`: Main Python file containing the FastAPI application code.
- `README.md`: This README file providing an overview of the project.

## Prerequisites

Before running the deployment, ensure you have the following prerequisites:

- Google Cloud Platform account
- Google Cloud SDK installed locally
- Docker installed locally
- Terraform installed locally

### Enable APIs

Make sure to enable the following APIs in your Google Cloud Platform project:

- **Cloud Run**: This API allows you to deploy and manage containerized applications on Google Cloud Run.
- **Container Registry**: This API allows you to store, manage, and deploy Docker container images on Google Container Registry.

### Create Service Account

Create a service account with appropriate permissions to deploy resources on Google Cloud Platform. At a minimum, the service account should have the following roles:

- **Cloud Run Admin (roles/run.admin)**: Allows full access to Cloud Run resources.Allows full access to Cloud Run resources.
- **Storage Object Admin (roles/storage.objectAdmin)**: Allows full control of Google Cloud Storage objects.


## Terraform Configuration

### `variables.tf`

The `variables.tf` file contains the definition of input variables used in the Terraform configuration:

```hcl
variable "project_id" {
  description = "The ID of the Google Cloud Platform project"
  default     = "Add the value of your project ID here"
}

variable "region" {
  description = "The region where the Cloud Run service will be deployed"
  default     = "us-central1"
}

variable "repository" {
  description = "The name of the Google Container Registry repository"
  default     = "Add the value of your repository name here"
}
```

## Deployment Steps

To deploy the FastAPI application on Google Cloud Run, follow these steps:

1. Authenticate with Google Cloud Platform:

    ```bash
    gcloud auth login
    ```

2. Initialize Terraform:

    ```bash
    terraform init
    ```

3. Plan the infrastructure changes:

    ```bash
    terraform plan
    ```

4. Build the Docker image:

    ```bash
    docker build -t gcr.io/your-project-id/your-image .
    ```

5. Push the Docker image to Google Container Registry (GCR):

    ```bash
    docker push gcr.io/your-project-id/your-image
    ```


6. Apply the Terraform configuration:

    ```bash
    terraform apply
    ```

7. Access the Cloud Run service URL:

    The Cloud Run service URL will be displayed in the Terraform output after successful deployment. You can also find it in the Google Cloud Console under the Cloud Run section.
## Testing

To test the deployed FastAPI application, you can send HTTP requests to the Cloud Run service URL using tools like cURL, Postman, or a web browser.

## Cleanup

To avoid incurring unnecessary charges, make sure to clean up the resources after testing:

1. Remove the Cloud Run service:

    ```bash
    terraform destroy
    ```

2. Delete the container image from Google Container Registry (optional):

    ```bash
    gcloud container images delete gcr.io/your-project-id/your-image
    ```

## Resources

- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Terraform Documentation](https://learn.hashicorp.com/tutorials/terraform/google-cloud-run)

