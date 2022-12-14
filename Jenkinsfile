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
            steps{
                sh "docker build -t ${IMAGE_REFERENCE} ."
            }
        }

        stage("Push"){
            steps{
                sh "docker push ${IMAGE_REFERENCE}"
            }
        }
        stage("Update Latest image"){
            when {
                branch "main"
            } 
            steps{
                sh """
                    docker tag ${IMAGE_REFERENCE} ${IMAGE_LATEST}
                    docker push ${IMAGE_LATEST}
                """
            }
        }
        stage("Deploy to kubernetes"){
            when {
                tag "*"
            } 
            steps{
                build(
                    job: 'ithome-crawler-cd',
                    parameters: [
                        string(name: 'K8S_NAMESPACE', value: 'prod'),
                        string(name: 'IMAGE_TAG', value: ${env.BRANCH_NAME}),
                        string(name: 'K8S_CRONJOB', value: '0 16 * * *'),
                    ]
                )
            }
        }        
    }
    post{
        always{
            cleanWs()
        }        
        failure{
            script {
                withCredentials([string(credentialsId: 'ithome-telegram-bot-token', variable: 'TOKEN')]){
                    withCredentials([string(credentialsId: 'ithome-telegram-notification-group', variable: 'GROUP_ID')]){                
                    sh '''
                        message="[Failed] Pipeline ${JOB_BASE_NAME}.\nBranch Name: ${env.BRANCH_NAME}\n ${BUILD_URL}"
                        curl -X GET https://api.telegram.org/bot${TOKEN}/sendMessage -d "chat_id=${GROUP_ID}&text=${message}"
                    '''
                    }
                }
            }
        }

    }
}
