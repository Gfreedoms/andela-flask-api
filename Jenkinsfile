pipeline {
    agent { dockerfile true }
    environment {
        DEBUG='True'
        CSRF_ENABLED='True'
        SQLALCHEMY_TRACK_MODIFICATIONS='False'
        DB='andela-flask-api'
        USER='postgres'
        PASSWORD=''
        HOST='localhost'
        PORT=5432
        HEROKU_POSTGRESQL_CRIMSON_URL="postgresql://${USER}:${PASSWORD}@${HOST}:5432/${DB}" 
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
                sh 'pip3 install --no-cache-dir -r requirements.txt'
            }
        }
        stage('Test'){
            steps {
                echo 'testingggg...ggg'
                sh 'psql -c "ALTER USER postgres WITH PASSWORD \'postgres\';" -U postgres'
                sh '#!/bin/bash \n '+
                'python3 -m pytest --cov=app app/tests/'
            }
        }
        stage('Deploy') {
            steps {
                echo 'deploying...'
            }
        }
    }
}