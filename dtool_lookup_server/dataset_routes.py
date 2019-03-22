from flask import (
    abort,
    Blueprint,
    jsonify,
    request,
)
from flask_jwt_extended import jwt_required, get_jwt_identity

from dtool_lookup_server.utils import (
    list_datasets_by_user,
    search_datasets_by_user,
)

bp = Blueprint("dataset", __name__, url_prefix="/dataset")


@bp.route("/list", methods=["GET"])
@jwt_required
def list_datasets():
    """List the dataset a user has access to."""
    username = get_jwt_identity()
    datasets = list_datasets_by_user(username)
    if datasets is None:
        abort(401)
    return jsonify(datasets)


@bp.route("/search", methods=["POST"])
@jwt_required
def search_datasets():
    """List the dataset a user has access to."""
    username = get_jwt_identity()
    query = request.get_json()
    datasets = search_datasets_by_user(username, query)
    if datasets is None:
        abort(401)
    return jsonify(datasets)
