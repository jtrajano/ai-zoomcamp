# Deploying to Google Cloud Run (Artifact Registry)

This guide assumes you have the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) (`gcloud`) installed.

## 1. Login and Setup
```bash
gcloud auth login
gcloud config set project sublime-triode-480404-i4
```

## 2. Enable APIs
We need Artifact Registry and Cloud Run.
```bash
gcloud services enable artifactregistry.googleapis.com run.googleapis.com
```

## 3. Create a Repository
We will create a Docker repository named `coding-interview-repo` in region `asia-southeast1`.
```bash
gcloud artifacts repositories create coding-interview-repo --repository-format=docker --location=asia-southeast1 --description="Docker repository for Coding Interview Platform"
```

## 4. Configure Authentication
Configure Docker to authenticate with the new Artifact Registry domain (`asia-southeast1-docker.pkg.dev`).
```bash
gcloud auth configure-docker asia-southeast1-docker.pkg.dev
```

## 5. Build and Push
Tag your image for the new repository structure: `LOCATION-docker.pkg.dev/PROJECT-ID/REPO-NAME/IMAGE-NAME`

```bash
# Tag the image (Replace YOUR_PROJECT_ID)
docker build -t asia-southeast1-docker.pkg.dev/sublime-triode-480404-i4/coding-interview-repo/app .

# Push the image
docker push asia-southeast1-docker.pkg.dev/sublime-triode-480404-i4/coding-interview-repo/app
```

## 6. Deploy
Deploy the image from Artifact Registry to Cloud Run.

```bash
gcloud run deploy coding-interview --image asia-southeast1-docker.pkg.dev/sublime-triode-480404-i4/coding-interview-repo/app --platform managed --region asia-southeast1 --allow-unauthenticated --max-instances 1 --memory 512Mi --timeout 3600 --port 8000
```

### Explanation:
- `--max-instances 1`: Cost Control (Free Tier friendly).
- `--allow-unauthenticated`: Makes the app public.


## 7. Access the App
Once deployed, you can access your app at the URL provided by the `gcloud run deploy` command.
https://coding-interview-2b437a3vpa-as.a.run.app/

## 8. Clean Up
```bash
gcloud artifacts repositories delete coding-interview-repo --location=asia-southeast1
gcloud run services delete coding-interview --region asia-southeast1
gcloud auth revoke
```
