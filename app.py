import os
from flask_script import Manager, Server
from permanode import init
from permanode.models import db

app = init('development')
flask_server = Manager(app)

port = os.getenv('PORT', '9080')
flask_server.add_command('dev', Server(host='0.0.0.0', port=int(port)))


@flask_server.command
def sync():
    """
    Sync database 
    """
    db.sync_db()


if __name__ == '__main__':
    flask_server.run()
