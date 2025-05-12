pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
    }

    stages {

        stage('Python venv') {
            steps {
                sh 'python3 -m venv $VENV_DIR'
                sh '. $VENV_DIR/bin/activate && pip install --upgrade pip'
            }
        }

        stage('Install requirements') {
            steps {
                sh '. $VENV_DIR/bin/activate && pip install -r producer/requirements.txt'
                sh '. $VENV_DIR/bin/activate && pip install -r validator/requirements.txt'
                sh '. $VENV_DIR/bin/activate && pip install -r processor/requirements.txt'
            }
        }

        stage('Build Docker (jeśli dostępny)') {
            when {
                expression {
                    return fileExists('docker/docker-compose.yml') && sh(script: 'command -v docker-compose', returnStatus: true) == 0
                }
            }
            steps {
                sh 'docker-compose -f docker/docker-compose.yml build'
            }
        }
    }

    post {
        always {
            echo '✅ Pipeline zakończony.'
        }
    }
}
