"""Route for retrieving the readme of a dataset"""
from flask import (
    abort,
    jsonify,
    current_app
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from dtool_lookup_server import UnknownURIError
from dtool_lookup_server.blueprint import Blueprint
from dtool_lookup_server.schemas import ReadmeSchema
import dtool_lookup_server.utils_auth
from dtool_lookup_server.utils import (
    url_suffix_to_uri,
    get_readme_from_uri_by_user
)

bp = Blueprint("readmes", __name__, url_prefix="/readmes")


@bp.route("/<path:uri>", methods=["GET"])
@bp.response(200, ReadmeSchema)
@bp.alt_response(401, description="Not registered")
@bp.alt_response(403, description="No permissions")
@bp.alt_response(404, description="Not found")
@jwt_required()
def readme(uri):
    """Request the dataset readme."""
    username = get_jwt_identity()
    if not dtool_lookup_server.utils_auth.user_exists(username):
        # Unregistered users should see 401.
        abort(401)

    uri = url_suffix_to_uri(uri)
    if not dtool_lookup_server.utils_auth.may_access(username, uri):
        # Authorization errors should return 400.
        abort(403)

    try:
        readme = get_readme_from_uri_by_user(username, uri)
    except UnknownURIError:
        current_app.logger.info("UnknownURIError")
        abort(404)

    return {"readme": readme}