from fabric.api import *


@hosts('alex@stylepix.net:2022')
def deploy():
    points = [
        'animals/',
        'announcements/',
        'blogs/',
        'clinics/',
        'content/',
        'exhibitions/',
        'meetings/',
        'news/',
        'nurseries/',
        'pharmacies/',
        'photoalbums/',
        'questions/',
        'system/',
        'templates/',
        'users/',
        'urls.py',
        'middleware.py'
    ]

    for name in points:
        local('rsync -e ssh --progress -rlcp /home/alex/projects/my/petsnet.in.ua/apps/%s stylepix:/var/www/petsnet/apps/%s' % (name, name))

    local('rsync -e ssh --progress -rlcp /home/alex/projects/my/petsnet.in.ua/static/css stylepix:/var/www/petsnet/static/css')

    #run(cd /var/www/shopping.info/apps; python manage.py syncdb')
    run('sudo service apache2 restart')
