pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Mohan_GitHub', url: 'https://github.com/mohan-m21/simple-todo-3tier.git']])
            }
        }

        stage('Build') {              // ← This is the BUILD / "compilation equivalent" stage
            steps {
                sh 'docker-compose build'   // ← Here: builds all Docker images
                                            //    - Copies backend code + requirements.txt
                                            //    - Runs pip install inside the image
                                            //    - Builds frontend Nginx image (static files)
                                            // This replaces traditional "compile" or "npm build"
            }
        }

        stage('Run') {                // ← Temporary start for verification (common in simple pipelines)
            steps {
                sh 'docker-compose up -d'
                sleep 30              // Wait for MySQL + Flask to be ready
            }
        }

        stage('Check') {              // ← Very basic test/smoke test
            steps {
                sh '''
                    curl --fail http://localhost:5000/api/todos || exit 1
                    echo "Backend looks alive"
                '''
            }
        }

    }

    post {
        always {
            sh 'docker-compose down || true'   // Cleanup – very important on shared Jenkins agents
        }
    }
}
