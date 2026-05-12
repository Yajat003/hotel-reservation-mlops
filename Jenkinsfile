pipeline{
    agent any

    stages{
        stage{'Cloning Github repository to Jenkins'}{
            steps{
                script{
                    echo 'Cloning Github repository to Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/Yajat003/hotel-reservation-mlops.git']])
                }
            }
        }
    }
}