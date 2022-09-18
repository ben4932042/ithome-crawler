pipeline{
    agent {
			label 'gcp-agent-1'
		}

    environment {
        IMAGE_REFERENCE = "docker.pkg.github.com/ben4932042/ithome-crawler/scrapy:latest"
    }

    stages{
        stage("Setup registry auth"){
            steps{
                withCredentials([usernamePassword(credentialsId: 'github-registry-secret', usernameVariable: 'USER', passwordVariable: 'TOKEN')]){
                    script{
                        sh "docker login docker.pkg.github.com -u ${USER} -p ${TOKEN}"
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
                export PYTHONPATH=${PWD}
                pylint --fail-under=10 src
                '''
            }
        }
        stage("Test"){
            steps{
                sh '''
                source venv/bin/activate
                export PYTHONPATH=${PWD}
                pytest tests
                '''
            }
        }
        stage("Build"){
            steps{
                sh "docker build -t ${IMAGE_REFERENCE} ."
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
