# services/users/project/api/users.py
from flask import Blueprint, jsonify, request, render_template
from project.api.models import Losa
from project import db
from sqlalchemy import exc

canchas_blueprint = Blueprint('canchas', __name__)

canchas_blueprint = Blueprint('canchas', __name__,
                              template_folder='./templates')


@canchas_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        canchan = request.form['canchan']
        tipo = request.form['tipo']
        preciod = request.form['preciod']
        precion = request.form['precion']
        db.session.add(Losa(canchan=canchan, tipo=tipo,
                            preciod=preciod, precion=precion))
        db.session.commit()
    canchas = Losa.query.all()
    return render_template('index.html', canchas=canchas)


@canchas_blueprint.route('/canchas/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@canchas_blueprint.route('/canchas', methods=['POST'])
def add_canchas():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    canchan = post_data.get('canchan')
    tipo = post_data.get('tipo')
    preciod = post_data.get('preciod')
    precion = post_data.get('precion')

    try:
        cancha = Losa.query.filter_by(canchan=canchan).first()
        if not cancha:
            db.session.add(Losa(canchan=canchan, tipo=tipo,
                                preciod=preciod, precion=precion))
            db.session.commit()
            response_object['status'] = 'satisfactorio'
            response_object['message'] = f'{canchan}, a sido agregado!'
            return jsonify(response_object), 201
        else:
            response_object['estado'] = 'fallo'
            response_object['mensaje'] = 'Disculpe. Esta placa ya existe.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@canchas_blueprint.route('/canchas/<cancha_id>', methods=['GET'])
def get_single_auto(cancha_id):
    """Obtener detalles de auto único """
    response_object = {
        'estado': 'fallo',
        'mensaje': 'La cancha no existe'
    }
    try:
        cancha = Losa.query.filter_by(id=int(cancha_id)).first()
        if not cancha:
            return jsonify(response_object), 404
        else:
            response_object = {
                'estado': 'satisfactorio',
                'data': {
                    'id': cancha.id,
                    'canchan': cancha.canchan,
                    'tipo': cancha.tipo,
                    'preciod': cancha.preciod,
                    'precion': cancha.precion
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@canchas_blueprint.route('/canchas', methods=['GET'])
def get_all_cancha():
    """Obteniendo todos los usuarios"""
    response_object = {
        'estado': 'satisfactorio',
        'data': {
            'canchas': [cancha.to_json() for cancha in Losa.query.all()]
        }
    }
    return jsonify(response_object), 200