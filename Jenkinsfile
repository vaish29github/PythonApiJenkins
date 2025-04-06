pipeline {
    agent any
    
    environment {
        AZURE_CREDENTIALS_ID = 'python-service-principal'
        RESOURCE_GROUP = 'python-webapp-rg-2912'
        APP_SERVICE_NAME = 'python-webapp-service-2912'
        PYTHON_VERSION = '3.12.8'
        PYTHON_PATH = 'C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        AZURE_CLI_PATH = 'C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az'  // Added Azure CLI path
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/vaish29github/PythonApiJenkins.git'
            }
        }
        
        stage('Build') {
            steps {
                bat '''
                    "%PYTHON_PATH%" --version
                    "%PYTHON_PATH%" -m pip install --upgrade pip
                    "%PYTHON_PATH%" -m pip install -r requirements.txt
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                withCredentials([azureServicePrincipal(credentialsId: AZURE_CREDENTIALS_ID)]) {
                    // Add Azure CLI to PATH
                    bat 'set PATH=%AZURE_CLI_PATH%;%PATH%'
                    
                    // Login to Azure
                    bat 'az login --service-principal -u "%AZURE_CLIENT_ID%" -p "%AZURE_CLIENT_SECRET%" --tenant "%AZURE_TENANT_ID%"'
                    bat 'az group create --name %RESOURCE_GROUP% --location eastus'
                    bat 'az appservice plan create --name %APP_SERVICE_NAME%-plan --resource-group %RESOURCE_GROUP% --sku B1 --is-linux'
                    bat 'az webapp create --resource-group %RESOURCE_GROUP% --plan %APP_SERVICE_NAME%-plan --name %APP_SERVICE_NAME% --runtime "PYTHON|%PYTHON_VERSION%"'
         
                    bat 'az webapp config set --resource-group %RESOURCE_GROUP% --name %APP_SERVICE_NAME% --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"'
                    
                    // Fixed the missing quote in the Compress-Archive command
                    bat 'powershell Compress-Archive -Path ./* -DestinationPath ./deploy.zip -Force'
  
                    bat 'az webapp deploy --resource-group %RESOURCE_GROUP% --name %APP_SERVICE_NAME% --src-path ./deploy.zip --timeout 1800'
                }
            }
        }
    }
}
