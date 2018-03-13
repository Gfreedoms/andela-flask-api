pipeline {
    agent any
    environment {
        DEBUG='True'
        CSRF_ENABLED='True'
        SQLALCHEMY_TRACK_MODIFICATIONS='False'
        DB='andela-flask-api'
        USER='postgres'
        PASSWORD='postgres'
        HOST='localhost'
        PORT=5432
        HEROKU_POSTGRESQL_CRIMSON_URL="postgresql://postgres:postgres@127.0.0.1:5432/andela-flask-api"
        WTF_CSRF_ENABLED='False'
        SECRET_KEY='youll-never-know-what-it-is-coz-its-secret'
        MAIL_SERVER='smtp.googlemail.com'
        MAIL_PORT=465
        MAIL_USE_TLS='False'
        MAIL_USE_SSL='True'
        MAIL_USERNAME="andelatestmail"
        MAIL_PASSWORD="andelatestmail1"
        MAIL_DEFAULT_SENDER="andelatestmail@gmail.com"
    }
    stages {
        stage('Build') { 
            steps {
                sh 'sudo apt-get install -y python python-pip python-virtualenv gunicorn nginx'
                sh 'pip install virtualenv'
                sh 'virtualenv --python=python3 .'
                sh 'source bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test'){
            steps {
                echo 'testingggg...ggg'
                sh 'py.test --cov=app app/tests/'
            }
        }
        stage('Deploy') {
            steps {
                echo 'deploying...'
            }
        }
    }
}