pipeline {
    agent any

    environment {
        AZURE_CREDENTIALS_ID = 'python-service-principal'
        RESOURCE_GROUP = 'python-webapp-rg-2912'
        APP_SERVICE_NAME = 'python-webapp-service-2912'
        PYTHON_VERSION = '3.10'
        PYTHON_PATH = 'C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/vaish29github/PythonApiJenkins.git'
            }
        }

        stage('Build') {
            steps {
                powershell '''
                    $python = "%PYTHON_PATH%"
                    & $python --version
                    & $python -m pip install --upgrade pip
                    & $python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([azureServicePrincipal(credentialsId: AZURE_CREDENTIALS_ID)]) {
                    powershell '''
                        az login --service-principal `
                            --username "$env:AZURE_CLIENT_ID" `
                            --password "$env:AZURE_CLIENT_SECRET" `
                            --tenant "$env:AZURE_TENANT_ID"

                        az group create `
                            --name "$env:RESOURCE_GROUP" `
                            --location eastus

                        az appservice plan create `
                            --name "$env:APP_SERVICE_NAME-plan" `
                            --resource-group "$env:RESOURCE_GROUP" `
                            --sku B1 `
                            --is-linux

                        az webapp create `
                            --resource-group "$env:RESOURCE_GROUP" `
                            --plan "$env:APP_SERVICE_NAME-plan" `
                            --name "$env:APP_SERVICE_NAME" `
                            --runtime "PYTHON|$env:PYTHON_VERSION"

                        az webapp config set `
                            --resource-group "$env:RESOURCE_GROUP" `
                            --name "$env:APP_SERVICE_NAME" `
                            --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"

                        Compress-Archive -Path .\\* -DestinationPath .\\deploy.zip -Force

                        az webapp deploy `
                            --resource-group "$env:RESOURCE_GROUP" `
                            --name "$env:APP_SERVICE_NAME" `
                            --src-path .\\deploy.zip `
                            --timeout 1800
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Deployment Failed!'
        }
    }
}
