
# AI Blog Generator

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Clone the Repository](#clone-the-repository)
  - [Environment Variables](#environment-variables)
  - [Docker Setup](#docker-setup)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Accessing the Container](#accessing-the-container)
- [Managing Dependencies](#managing-dependencies)
  - [Adding or Removing Packages](#adding-or-removing-packages)
  - [Rebuilding the Docker Image](#rebuilding-the-docker-image)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The **AI Blog Generator** is an automated system that leverages LangChain, OpenAI's GPT-4, and Hugging Face's Inference APIs to generate blog articles based on the latest trends in the IT field. The workflow consists of the following steps:

1. **Trend Extraction**: Identifies the latest hot trends in the IT field.
2. **News Information Extraction**: Gathers relevant information for each trend.
3. **Article Generation**: Creates detailed and engaging blog articles for each trend.
4. **Image Generation**: Produces illustrative images for each blog article.

The entire workflow is orchestrated using Docker for seamless deployment and scalability.

## Features

- **Automated Trend Analysis**: Identifies and lists the latest trends in a specified topic.
- **Content Generation**: Produces well-structured and informative blog articles.
- **Image Creation**: Generates relevant images to accompany each blog post.
- **Dockerized Deployment**: Ensures easy setup and scalability using Docker and Docker Compose.
- **Environment Variable Management**: Securely handles API keys using environment variables.

## Prerequisites

Before setting up the AI Blog Generator, ensure you have the following installed on your system:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

## Setup

### Clone the Repository

```bash
git clone https://github.com/samugit83/ai_blog_generator.git
cd ai_blog_generator
```

### Environment Variables

The application requires API keys for OpenAI and Hugging Face. These should be stored securely using environment variables.

#### Create a `.env` File

In the root directory of the project, create a file named `.env`:

```bash
touch .env
```

#### Add Your API Keys

Open the `.env` file and add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACE_API_TOKEN=your_huggingface_api_token
```

Replace `your_openai_api_key` and `your_huggingface_api_token` with your actual API keys.

### Docker Setup

The application is containerized using Docker. Ensure Docker and Docker Compose are installed and running on your system.

## Usage

### Running the Application

#### Build the Docker Image

If this is your first time setting up the project or if you've changed the `Dockerfile` or `requirements.txt`, build the Docker image:

```bash
docker-compose build
```

#### Start the Docker Containers

Launch the application using Docker Compose:

```bash
docker-compose up -d
```

This command will start the container in detached mode.

### Accessing the Container

To execute the workflow or access the container's shell, follow these steps:

#### Enter the Container's Bash Shell

```bash
docker-compose exec blog_generator bash
```

#### Run the Application

Inside the container, execute the main script:

```bash
python main.py
```

This will initiate the workflow, generating trends, articles, and images based on the latest IT trends.

## Managing Dependencies

### Adding or Removing Packages

If you need to add or remove Python packages, modify the `requirements.txt` file accordingly.

#### Edit `requirements.txt`

Add or remove the necessary packages.

```bash
nano requirements.txt
```

Save and Exit.

After making changes, save the file and exit the editor.

### Rebuilding the Docker Image

Whenever you add or remove packages in `requirements.txt` or make changes to the Dockerfile, you need to rebuild the Docker image.

#### Stop and Remove Existing Containers

```bash
docker-compose down
```

#### Remove the Existing Docker Image

```bash
docker rmi blog_generator
```

#### Rebuild the Docker Image

```bash
docker-compose build
```

#### Start the Containers

```bash
docker-compose up -d
```

## Project Structure

```bash
blog-generator-workflow/
├── Dockerfile
├── docker-compose.yml
├── main.py
├── requirements.txt
├── .env
└── README.md
```

- **Dockerfile**: Defines the Docker image configuration.
- **docker-compose.yml**: Configures Docker services.
- **main.py**: The main Python script orchestrating the workflow.
- **requirements.txt**: Lists the Python dependencies.
- **.env**: Stores environment variables (API keys).
- **README.md**: Project documentation.

## Troubleshooting

- **API Key Errors**: Ensure that the `.env` file contains valid API keys for OpenAI and Hugging Face.
- **Docker Issues**: Verify that Docker and Docker Compose are correctly installed and running.
- **Image Generation Failures**: Check your Hugging Face API token and ensure you have access to the specified model (`black-forest-labs/FLUX.1-dev`).
- **Python Errors**: Ensure all dependencies are correctly installed by checking the `requirements.txt` and rebuilding the Docker image if necessary.

## License

This project is licensed under the MIT License.

**Note:** Replace `https://github.com/yourusername/blog-generator-workflow.git` with the actual repository URL if applicable.

## Additional Docker Commands

If you add or remove packages in `requirements.txt` or make changes to the Dockerfile, you need to rebuild the Docker image. Use the following commands:

```bash
docker-compose down
docker rmi blog_generator
docker-compose build
docker-compose up -d
```

To enter the container's bash shell and run the application:

```bash
docker-compose exec blog_generator bash
python main.py
```
