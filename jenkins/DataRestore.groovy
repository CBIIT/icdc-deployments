
@Library('datacommons-jenkins-shared-library@v1.1') _

def getLabelForEnvironment(environment) {
	if (environment == "stage" || environment == "prod"){
		return "commons-docker-ncias-p3305-c"
	}else {
		return "slave-ncias-d2940-c"
	}
}


pipeline {
	agent {
		node {
			label getLabelForEnvironment(params.Environment)
		}
	}

	parameters {
    extendedChoice( 
        name: 'Environment', 
        defaultValue: 'dev', 
        description: 'Choose the environment to build', 
        type: 'PT_SINGLE_SELECT',
        value: 'dev,dev2,qa,stage,prod' )
    string(defaultValue: "", 
        description: 'Name of the dump file to use', 
        name: 'DumpFileName')
    
    }

  tools {
  	maven 'Default' 
    jdk 'Default' 
  }
 environment {
    DUMP_FILE = "${params.DumpFileName}"
	  TIER      = "${params.Environment}"
    SLACK_SECRET  = "icdc_slack_url"
    PROJECT       = "icdc"
    //S3_BUCKET     = "crdc-icdc-dev-neo4j-data-backup"
    S3_BUCKET     = "crdc-${env.PROJECT}-prod-neo4j-data-backup"
 }
  stages{

  	stage('create inventory'){
      agent {
        docker {
          image 'cbiitssrepo/cicd-ansible-8.0:latest'
          args '--net=host -u root -v /var/run/docker.sock:/var/run/docker.sock'
          reuseNode true
        }
      }
 		steps {
 		  wrap([$class: 'AnsiColorBuildWrapper', colorMapName: "xterm"]) {
			    ansiblePlaybook( 
                playbook: '${WORKSPACE}/ansible/hostfile.yml',
                inventory: '${WORKSPACE}/ansible/hosts',
                extraVars: [
                  tier: "${params.Environment}",
						      project_name: "${PROJECT}",
                  workspace: "$WORKSPACE"
						    ],
                colorized: true)
		  }
 		}
    
  }
  stage("download dump"){
    steps{
      wrap([$class: 'AnsiColorBuildWrapper', colorMapName: "xterm"]) {
			    ansiblePlaybook( 
                playbook: '${WORKSPACE}/ansible/download-dump.yml',
                inventory: '${WORKSPACE}/ansible/hosts',
                colorized: true)
		  }
    }
  }
	stage('restore data dump'){
		steps{			
			ansiblePlaybook( 
                playbook: '${WORKSPACE}/ansible/dump-restore.yml',
                inventory: '${WORKSPACE}/inventory/hosts',
                colorized: true)

		}
	}
	
  }
  post {
    always {
       notify(
            secretPath: "notification/slack",
            secretName: "${env.SLACK_SECRET}"
        ) 
      }
    cleanup {
      cleanWs()
      }
  }
}