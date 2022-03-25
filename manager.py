from test_platform import create_app, db
from test_platform import models
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = create_app('dev')
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
