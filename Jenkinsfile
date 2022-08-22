pipeline{
    agent any
    options {
        timestamps()
        timeout(time:7, unit: 'MINUTES')
        buildDiscarder(logRotator(
        numToKeepStr: '4',
        daysToKeepStr: '7',
        artifactNumToKeepStr: '30'))   
    }

    stages{
        stage("build"){
            steps{
                script{
                sh "docker build -t app:latest ."
                
                }
            }
        }

        stage("e2e"){
            steps{
                script{
                sh "docker-compose up -d"
                }
            }
        }

        stage("push"){
            steps{
                script{
                sh" echo ta mere"
                }
            }
        }
    }
    post{
        always{
            sh "docker-compose down "
        }
        success{
            echo "========pipeline executed successfully ========"
        }
        failure{
            echo "========pipeline execution failed========"
        }
    }
}