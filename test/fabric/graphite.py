import re
from fabric.api import env, run, hide, task
from envassert import detect, file, package, port, process, service, user


def graphite_is_responding():
    with hide('running', 'stdout'):
        homepage = run("wget --no-check-certificate --quiet --output-document - https://localhost/")
        if re.search('Graphite Browser', homepage):
            return True
        else:
            return False


@task
def check():
    env.platform_family = detect.detect()

    assert package.installed("apache2")
    assert package.installed("memcached")
    assert file.is_dir("/opt/graphite")
    assert file.exists("/etc/sv/statsd")
    assert port.is_listening(443)
    assert port.is_listening(2003)
    assert port.is_listening(2004)
    assert port.is_listening(8126)
    assert user.exists("statsd")
    assert process.is_up("apache2")
    assert process.is_up("memcached")
    assert service.is_enabled("apache2")
    assert service.is_enabled("memcached")
    assert graphite_is_responding()
