pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages{
        stage('Cloning Github repository to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repository to Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/Yajat003/hotel-reservation-mlops.git']])
                }
            }
        }

        stage('Setting up the Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up Virtual Environment and Installing dependancies...'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

    }
}