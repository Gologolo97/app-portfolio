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
                echo "========test========"
            }
            post{
                always{
                    echo "========always========"
                }
                success{
                    echo "========A executed successfully========"
                }
                failure{
                    echo "========A execution failed========"
                }
            }
        }
    }
    post{
        always{
            echo "========always========"
        }
        success{
            echo "========pipeline executed successfully ========"
        }
        failure{
            echo "========pipeline execution failed========"
        }
    }
}