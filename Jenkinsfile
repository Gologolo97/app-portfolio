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
        
        stage("Build")
        {            
            steps{
                script{
                    image = docker.build("golo-portfolio")
                }
            }
        }

        stage("E2E Test"){
            steps{
                script{

                sh """
                #!/bin/bash

                docker-compose up --build -d
                chmod +x test.sh
                ./test.sh web:5000
                """
            }
        }

        }
        stage ("Calc and Release Tag") {
            when {
                    expression {BRANCH_NAME == "master" }
                }
            steps{
                script{
                    sshagent(['githun-private-key']){

                        echo "========= Calc Tag ========="

                        //sh "git fetch --all --tags"
                        LAST_TAG = sh (script: "git tag -l | sort -V | tail -1", returnStdout: true)
                        if (LAST_TAG.isEmpty() ) {
                            NEXT_TAG = "1.0.0"
                        }
                        else {
                            (major, minor, patch) = NEXT_TAG.tokenize(".")
                            patch = patch.toInteger() + 1
                            echo "Increment to ${patch}"
                            NEXT_TAG = "${major}.${minor}.${patch}"
                            echo "the next tag for Release is: ${NEXT_TAG}"
                        }

                        echo "========= Release Tag ========="

                        sh """
                        #!/bin/bash

                        git clean -f
                        git tag ${NEXT_TAG}
                        git push origin ${NEXT_TAG}

                        """
                    }
                }
            }
        }

        stage("Push"){
            when{
                expression {BRANCH_NAME == "master"  }
            }
            steps{
                script{
                docker.withRegistry("https://644435390668.dkr.ecr.us-east-2.amazonaws.com","ecr:us-east-2:aws-credentials"){
                    image.push("${NEXT_TAG}")}
                }
            }
        }

        stage ("Deploy"){
            when {
                    expression {BRANCH_NAME == "master" }
                }
            steps{
                script{
                    sshagent(['githun-private-key']){
                        val = sh(script: "echo ${NEXT_TAG}", returnStdout: true).trim()
                       
                        sh """
                        #!/bin/bash
                        #git commit -am"commit"
                        git checkout master
                      
                        
                        yq -i '.app.tag = "${val}"' flask-chart/values.yaml
                        git pull
                        git add .
                        git commit -am"Tag change"
                        git push 
                        """
                    }
                }
            }
        }


    }
    post{
        always{
            sh "docker-compose down "
        }
        success{
            mail to: "golovatylejb@gmail.com",
            subject: "Notification from Jenkins",
            body: "Everything worked"
        }

        failure{
            mail to: "golovatylejb@gmail.com",
            subject: "Notification from Jenkins",
            body: "Test failed"
        }
    }
}