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
        stage("build for release"){
            when {
                    expression {BRANCH_NAME ==~ /release(.+)/ }
                }
            steps{
                script{
                
                sshagent(['githun-private-key']){
                    sh "git fetch --all --tags"
                    TAG = BRANCH_NAME.split('\\/')
                        VERSION = TAG[1]
                        LAST_DIGIT_CHECK = sh (script: "git tag -l | tail -n 1 | tail -c 2", returnStdout: true)
                        LAST_DIGIT = sh (script: "git tag -l | sort -V | tail -1", returnStdout: true)
                        echo "Last digit: ${LAST_DIGIT}"
                        echo "Tag: ${TAG}"
                        if (LAST_DIGIT_CHECK.isEmpty()) {
                            NEXT_TAG = "${VERSION}.0"
                            echo "tag is ${NEXT_TAG}"
                        }
                        else {
                            (major, minor, patch) = LAST_DIGIT.tokenize(".")
                            patch = patch.toInteger() + 1
                            echo "Increment to ${patch}"
                            NEXT_TAG = "${major}.${minor}.${patch}"
                            echo "the next tag for Release is: ${NEXT_TAG}"
                        }
                }
                //sh "docker build -t app:${NEXT_TAG} ."  
                image = docker.build("golo-portfolio:${NEXT_TAG}")
              }  
            }
        }

        stage("build not for release")
        {
            when{
                expression {BRANCH_NAME == 'master' || BRANCH_NAME ==~ /feature(.+)/ }
            }
            steps{
                script{
                    //sh "docker build -t app:SNAPSHOT ."
                    image = docker.build("golo-portfolio:SNAPSHOT")
                    NEXT_TAG=""
                }
            }
        }

        stage("e2e"){
            steps{
                script{
                if (NEXT_TAG.isEmpty()){
                sh "VERSION=SNAPSHOT docker-compose up -d"
                }
                else{
                sh "VERSION=${NEXT_TAG} docker-compose up -d"
                }
                sh "chmod +x test.sh"
                sh "./test.sh web:5000"
                }
            }
        }

        stage("push"){
            when{
                expression {BRANCH_NAME ==~ /release(.+)/  }
            }
            steps{
                script{
                docker.withRegistry("https://644435390668.dkr.ecr.us-east-2.amazonaws.com","ecr:us-east-2:aws-credentials"){
                    image.push("${NEXT_TAG}")}
                }
            }
        }

        stage ("release TAG"){
            when {
                    expression {BRANCH_NAME ==~ /release(.+)/ }
                }
            steps{
                sshagent(['githun-private-key']){
                    sh "git clean -f"
                    sh "git tag ${NEXT_TAG}"
                    sh "git push origin ${NEXT_TAG}"
                }
            }
        }

        stage ("update version in GitOps for deploying"){
            when {
                    expression {BRANCH_NAME ==~ /release(.+)/ }
                }
            steps{
                script{
                    sshagent(['githun-private-key']){
                    
                        
                        sh '''
                        #!/bin/bash
                        
                        yq -i '.app.tag = "$NEXT_TAG"' flask-chart/values.yaml
                        git commit -am"Tag change"
                        git push origin HEAD:master 
                        '''
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