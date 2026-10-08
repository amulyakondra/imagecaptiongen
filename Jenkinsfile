pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t image-caption-generator .'
            }
        }

        stage('Run Python Project') {
            steps {
                bat 'docker run --rm image-caption-generator'
            }
        }
    }

    post {
        success {
            echo 'Image Caption Generator executed successfully!'
        }

        failure {
            echo 'Build or execution failed.'
        }
    }
}