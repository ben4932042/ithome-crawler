pipeline{
    agent {
            label 'gcp-agent-1'
        }

    environment {
        IMAGE_REFERENCE = "docker.pkg.github.com/ben4932042/ithome-crawler/scrapy:${env.BRANCH_NAME}"
        IMAGE_LATEST = "docker.pkg.github.com/ben4932042/ithome-crawler/scrapy:latest"
    }

    stages{
        stage("Setup registry auth"){
            when {
                anyOf{
                    branch "main"
                    tag "*"
                }
            }            
            steps{
                withCredentials([usernamePassword(credentialsId: 'github-registry-secret', usernameVariable: 'USER', passwordVariable: 'TOKEN')]){
                    script{
                        sh "docker login docker.pkg.github.com -u ${USER} -p ${TOKEN}"
                    }
                }
            }
        }

        stage("build and test the project") {
            agent {
                docker { 
                        image "python:3.7-slim"
                        args '-u root'
                    }
            }
            stages {
               stage("Setup requirements") {
                   steps {
                       sh """
                        pip3 install -r requirements.txt
                        pip3 install pylint=='2.13.7'
                        pip3 install pytest=='7.1.2'
                       """
                   }
               }

               stage("Lint") {
                    steps{
                        sh """
                            export PYTHONPATH=${WORKSPACE}
                            pylint --fail-under=10 src
                        """
                    }
               }

               stage("Test") {
                   steps {
                       sh """              
                            export PYTHONPATH=${WORKSPACE}
                            pytest tests
                        """
                   }
               }
            }
        }

        stage("Build"){
            when {
                anyOf{
                    branch "main"
                    tag "*"
                }
            } 
            steps{
                sh "docker build -t ${IMAGE_REFERENCE} ."
            }
        }

        stage("Push"){
            when {
                anyOf{
                    branch "main"
                    tag "*"
                }
            } 
            steps{
                sh "docker push ${IMAGE_REFERENCE}"
            }
        }
        stage("Update Latest image"){
            when {
                tag "*"
            } 
            steps{
                sh """
                    docker tag ${IMAGE_REFERENCE} ${IMAGE_LATEST}
                    docker push ${IMAGE_LATEST}
                """
            }
        }        
    }
    post{
        always{
            cleanWs()
        }
    }
}
