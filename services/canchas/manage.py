# services/users/manage.py
import unittest
from flask.cli import FlaskGroup
import coverage

from project import create_app, db
from project.api.models import Losa


# configurando informes de covertura con coverage 4.5.1
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/test/*',
        'project/config.py',
    ]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def recreate_db():
        db.drop_all()
        db.create_all()
        db.session.commit()



@cli.command()
def test():
    """ Ejecuta las pruebas sin cobertura de codigo"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def seed_db():
    """Sembrado la base de datos."""
    db.session.add(Losa(canchan='Sintetico', tipo='7x7', preciod='40', precion='80'))
    db.session.add(Losa(canchan='Losa', tipo="5x5", preciod='35', precion='85'))
    db.session.commit()

@cli.command()
def cov():
    """Ejecuta las pruebas unitarias con covertura."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Resumen de covertura:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
        return 1

if __name__ == '__main__':
    cli()