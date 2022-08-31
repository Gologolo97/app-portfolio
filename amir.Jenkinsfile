pipeline {
    
    triggers{
        pollSCM '* * * * *'
    }

    agent any

    options {
        timestamps()
        timeout(time:10, unit:'MINUTES')
     }

    environment {
        BRANCH="${env.GIT_BRANCH}"
        GIT_COMMIT_MSG = sh(script:"git log -1 --pretty=%B", returnStdout:true).trim()
        AWS_ACCOUNT_ID="644435390668"
        AWS_DEFAULT_REGION="eu-central-1"
        REPOSITORY_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
        IMAGE_REPO_NAME_BACKEND="amir-todo-backend"
        IMAGE_REPO_NAME_FRONTEND="amir-todo-front"
     }

    stages{

        stage('build') {
            steps {
                echo "========= build ========="
                sh "docker-compose build"
            }
        }

        stage('test') {
            steps {
                echo "========= test ========="
                sh "docker-compose up -d"
                sh "sleep 10"
                sh "docker network connect jenkinslab_default front_container"
                sh """
                    #!/bin/sh
                    set -e
                    
                    curl -s -o /dev/null -I -w "%{http_code}\n" "front"
                    TEST_CODE=\$?
                
                    if [ \$TEST_CODE -eq 0 ]; then
                        echo "Success, exit code: \$?"
                        exit 0
                    else 
                        echo "Test failed with exit code: \$?"
                        exit \$?
                    fi
                """
            }
        }

        stage('calculate-tag') {
            when { expression { BRANCH == "main" } }
            steps {
                echo "========= tag ========="
                script{
                    sshagent(credentials: ['jenkins_github']) {
                        sh "git fetch --all --tags"
                        TAG = sh(script: "git tag | sort -V | tail -1", returnStdout: true)
                        if (TAG.isEmpty() ) {
                            TAG =  "1.0.0"
                        } 
                        else {
                            (major, minor, patch) = TAG.tokenize(".")
                            patch = patch.toInteger() + 1
                            echo "${patch}"
                            TAG = "${major}.${minor}.${patch}"
                            echo "New Tag: ${TAG}"
                        }
                    }
                }
            }
        }

        stage(' ') {
            when { expression { BRANCH == "main" } }
            steps { 
                echo "========= publish ========="
                script {
                     withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws_develeap', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                        sh "aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin ${REPOSITORY_URI}"
                        sh "docker tag ${IMAGE_REPO_NAME_FRONTEND}:latest 644435390668.dkr.ecr.eu-central-1.amazonaws.com/${IMAGE_REPO_NAME_FRONTEND}:${TAG}"
                        sh "docker push 644435390668.dkr.ecr.eu-central-1.amazonaws.com/${IMAGE_REPO_NAME_FRONTEND}:${TAG}"
                        sh "docker tag ${IMAGE_REPO_NAME_BACKEND}:latest 644435390668.dkr.ecr.eu-central-1.amazonaws.com/${IMAGE_REPO_NAME_BACKEND}:${TAG}"
                        sh "docker push 644435390668.dkr.ecr.eu-central-1.amazonaws.com/${IMAGE_REPO_NAME_BACKEND}:${TAG}"
                    }
                }
            }
        }
        stage('git-tag') {
            when { expression { BRANCH == "main" } }
            steps {
                echo "========= tag ========="
               sshagent(credentials: ['jenkins_github']) {
                    sh "git clean -f"
                    sh "git tag ${TAG}"
                    sh "git push origin ${TAG}"
               }
            }
        }

        stage('deploy') {
            when { expression { BRANCH == "main" } }
            steps {
                echo "========= deploy ========="
                script {
                    sshagent(credentials: ['jenkins_github_all']) {
                        sh  """ #!/bin/bash
                            git clone git@github.com:Amir-Benyamini/gitops-farm-todo.git
                            cd gitops-farm-todo/
                            yq -i '.appVersion = "${TAG}"' todo-app/Chart.yaml
                            git commit -am "Updated new tag to version: ${TAG}"
                            git tag ${TAG}
                            git push origin ${TAG}
                            git push origin main
                            """
                    }
                }
            }
        }
    }

    post {
        always {
            sh "docker-compose down"
            script{
                if(BRANCH == "main"){
                    sh "docker rmi -f ${REPOSITORY_URI}/${IMAGE_REPO_NAME_BACKEND}:${TAG}"
                    sh "docker rmi -f ${REPOSITORY_URI}/${IMAGE_REPO_NAME_FRONTEND}:${TAG}"
                }
            }
            sh "docker rmi -f ${IMAGE_REPO_NAME_BACKEND}:latest"
            sh "docker rmi -f ${IMAGE_REPO_NAME_FRONTEND}:latest"
            cleanWs()
        }
        failure {
            emailext (
                subject: "${currentBuild.result}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """<p>${currentBuild.result}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                        <p>Check console output at <a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a></p>""",
                recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']])
        }
    }
}