pipeline{
    agent {
			label 'gcp-agent-1'
		}

    environment {
        IMAGE_REFERENCE = "ghcr.io/ben4932042/ithome-crawler:latest"
    }

    stages{
        stage("Setup registry auth"){
            steps{
                withCredentials([usernamePassword(credentialsId: 'github-registry-secret', usernameVariable: 'USER', passwordVariable: 'TOKEN')]){
                    script{
                        sh "docker login docker.pkg.github.com -u docker-user -p docker-token"
                    }
                }
            }
        }
        stage("Setup virtual env"){
            steps{
                sh '''#!/bin/bash
                virtualenv venv
                source venv/bin/activate
                pip3 install -r requirements.txt
                pip3 install pylint
                pip3 install pytest
                '''
            }
        }                                               
        stage("Lint"){
            steps{
                sh '''
                source venv/bin/activate
                pylint --fail-under=10 src
                '''
            }
        }
        stage("Test"){
            steps{
                sh '''
                source venv/bin/activate
                pytest tests
                '''
            }
        }
        stage("Build"){
            steps{
                echo "docker build -t ${IMAGE_REFERENCE} ."
            }
        }
        stage("Push"){
            steps{
                sh "docker push ${IMAGE_REFERENCE}"
            }
        }
    }
    post{
        always{
            cleanWs()
        }
    }   
}
