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
                bat 'py --version'
                bat 'py -m pip --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'py -m pip install -r requirements.txt'
            }
        }

        stage('Run Python Project') {
            steps {
                bat py image_caption_generator.py'
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