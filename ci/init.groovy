import jenkins.model.Jenkins
import hudson.model.FreeStyleProject
import hudson.tasks.Shell
import hudson.security.HudsonPrivateSecurityRealm
import hudson.security.FullControlOnceLoggedInAuthorizationStrategy
def j = Jenkins.get()
def realm = new HudsonPrivateSecurityRealm(false)
realm.createAccount("lab-admin", UUID.randomUUID().toString())
j.setSecurityRealm(realm)
def auth = new FullControlOnceLoggedInAuthorizationStrategy()
auth.setAllowAnonymousRead(false)
j.setAuthorizationStrategy(auth)
j.setNumExecutors(1)
def project = j.createProject(FreeStyleProject, "workshop-lab")
project.setDescription("GitHub repository: https://github.com/artem52qwe/MyPythonProject-chaper3006.git; checkout from its local read-only mirror /source")
project.getBuildersList().add(new Shell(new File('/source/ci/build.sh').text))
project.save()
j.save()
Thread.start {
    try {
        sleep(8000)
        def results = []
        for (int i = 1; i <= 2; i++) {
            def build = project.scheduleBuild2(0).get()
            new File("/out/build-${i}.log").text = build.getLog(10000).join("\n")
            results.add([number: build.number, result: build.result.toString(), duration_ms: build.duration])
        }
        new File('/out/results.json').text = groovy.json.JsonOutput.toJson(results)
        new File('/out/done').text = 'complete'
    } catch (Throwable error) {
        new File('/out/failure.txt').text = error.toString()
    }
}
