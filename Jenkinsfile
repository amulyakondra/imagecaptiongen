pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                bat 'python --version'
                bat 'python -m pip --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Python Project') {
            steps {
                bat 'python image_caption_generator.py'
            }
        }
    }

    post {
        success {
            echo 'Project executed successfully!'
        }

        failure {
            echo 'Project execution failed!'
        }
    }
}