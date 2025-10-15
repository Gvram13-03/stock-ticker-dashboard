pipeline {
    agent { label 'python313' }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                bat 'pytest -v'
            }
        }
        stage('Debug YFinance') {
            steps {
                bat 'python -c "import yfinance as yf; print(yf.Ticker(\'MSFT\').history(period=\'1d\'))" > yfinance_debug.txt'
            }
        }
        stage('Run') {
            steps {
                bat 'start /wait streamlit run streamlit_app.py --server.port 8502 --server.headless true --server.enableCORS false'
            }
        }
    }
    post {
        always {
            echo 'Pipeline complete.'
        }
        success {
            echo 'Tests and run passed! Trunk is releasable.'
        }
        failure {
            echo 'Tests or run failed.'
        }
    }
}