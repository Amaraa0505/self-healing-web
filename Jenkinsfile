pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Amaraa0505/self-healing-web.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker compose build'
            }
        }
        stage('Deploy Cluster') {
            steps {
                sh 'docker compose up -d'
            }
        }
        stage('Verify Health') {
            steps {
                sh 'sleep 3 && curl -f http://localhost:5050/health || exit 1'
            }
        }
    }
}