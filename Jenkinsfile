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
    environment{
        
        BRANCH_NAME = "${env.GIT_BRANCH}"
        
    }

    stages{
        stage("build"){
            when {
                    expression {BRANCH_NAME ==~ /master(.*)/ }
                }
            steps{
                script{
                withCredentials([string(credentialsId: 'GITHUB_HOST_KEY', variable: 'GITHUB_HOST_KEY')]) {
                    sh 'mkdir ~/.ssh && echo "$GITHUB_HOST_KEY" >> ~/.ssh/known_hosts'
                }
                sshagent(['githun-private-key']){
                    git branch -r
                }

               
                sh "docker build -t app:${NEXT_TAG} ."
                
                
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