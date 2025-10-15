pipeline {
    agent { label 'python313' }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Install') { steps { bat 'pip install -r requirements.txt' } }
        stage('Test') { steps { bat 'pytest -v' } }
        stage('Run') { steps { bat 'start /b streamlit run streamlit_app.py --server.port 8501' } }
    }
    post {
        always { echo 'Pipeline complete.' }
        success { echo 'Tests and run passed! Trunk is releasable.' }
        failure { echo 'Tests or run failed.' }
    }
