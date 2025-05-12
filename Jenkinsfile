pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
    }

    stages {

        stage('Klonowanie repozytorium') {
            steps {
                checkout scm
            }
        }

        stage('Utworzenie virtualenv') {
            steps {
                sh 'python3 -m venv $VENV_DIR'
                sh '. $VENV_DIR/bin/activate && pip install --upgrade pip'
            }
        }

        stage('Instalacja zależności') {
            steps {
                sh '. $VENV_DIR/bin/activate && pip install -r producer/requirements.txt'
                sh '. $VENV_DIR/bin/activate && pip install -r validator/requirements.txt'
                sh '. $VENV_DIR/bin/activate && pip install -r processor/requirements.txt'
            }
        }

        stage('Build Docker (opcjonalnie)') {
            steps {
                sh 'docker-compose -f docker/docker-compose.yml build'
            }
        }

        // Można dodać kolejne etapy: testy, lint, deploy
    }

    post {
        always {
            echo '✅ Pipeline zakończony.'
        }
    }
}
