from fabric.api import local
from fabric.api import lcd

manage_path = "~/Projects/post_generator/manage.py"

def migrate_db():
    local("python %s syncdb" % (manage_path))
    local("python %s migrate post_generator" % (manage_path))

def prepare_deployment(branch_name):
    local('python manage.py test post_generator')
    local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)


#def deploy():
#    with lcd('/path/to/my/prod/area/'):
#        local('git pull /my/path/to/dev/area/')
#        local('python manage.py migrate myapp')
#        local('python manage.py test myapp')
#        local('/my/command/to/restart/webserver')
