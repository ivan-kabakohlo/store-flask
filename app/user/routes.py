from app.user import bp


@bp.route('/users', methods=['GET'])
def users():
    return 'Users'
