pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
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