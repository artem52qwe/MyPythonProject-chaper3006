FROM jenkins/jenkins:2.580.2-jdk21
USER root
RUN apt-get update && apt-get install -y python3 python3-flake8 git && apt-get clean
USER jenkins
COPY ci/init.groovy /usr/share/jenkins/ref/init.groovy.d/lab.groovy
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"
