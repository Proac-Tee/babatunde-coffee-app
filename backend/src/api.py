from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

# create and configure the app
app = Flask(__name__)
setup_db(app)

# CORS app setup
CORS(app, resource={"/": {"origins": "*"}})
# CORS Headers
@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


# db_drop_and_create_all()

# ROUTES


# GET /drinks endpoint implemented as specified in drinks.service.ts at the frontend
@app.route("/drinks")
def available_drinks():

    # get all drinks
    selections = Drink.query.Order_by(Drink.id).all()

    # returns the succes value and the short data representartion of drinks as specified in the drinks models table
    return jsonify(
        {
            "success": True,
            "drinks": [drink.short() for drink in selections],
        }
    )


# GET /drinks-detail endpoint implemented as specified in the drinks.service.ts at the frontend
@app.route("/drinks-detail")
@requires_auth("get:drinks-detail")
def available_drinks_detail(payload):

    # get all drinks
    selections = Drink.query.Order_by(Drink.id).all()

    # returns the succes value and the long data representartion of drinks as specified in the drinks models table
    return jsonify(
        {
            "success": True,
            "drinks": [drink.long() for drink in selections],
        }
    )


# POST /drinks-detail endpoint implemented as specified in the drinks.service.ts at the frontend
@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def create_new_drink(payload):

    # get the body from frontend input as json
    body = request.get_json()

    try:

        # input data from the frontend
        req_title = body.get("title", None)
        req_recipe = body.get("recipe", None)

        # Post the update to the front end
        drink = Drink(title=req_title, recipe=req_recipe)

        # persists data in database
        drink.insert()

        # returns the succes value and the long data representartion of drinks as specified in the drinks models table
        print(drink.long())
        return jsonify(
            {
                "success": True,
                "drinks": [drink.long()],
            }
        )
    except Exception:
        abort(422)


# PATCH /drinks/<drinks_id> endpoint implemented as specified in the drinks.service.ts at the frontend
@app.route("/drinks/<int:drink_id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def patch_selected_drink(drink_id, payload):

    # get the body from frontend input as json
    body = request.get_json()

    try:
        # fetch drinks by fithering by the drink_id
        selection = Drink.query.filter(Drink.id == drink_id).one_or_none()

        # input data from the frontend
        selection.title = body.get("title", None)
        selection.recipe = body.get("recipe", None)

        if selection is None:
            abort(404)

        # Patch the selected drink_id in the front end and persists data in database
        selection.update()

        # returns the succes value and the long data representartion of drinks as specified in the drinks models table
        print(selection.long())
        return jsonify(
            {
                "success": True,
                "drinks": [selection.long()],
            }
        )

    except Exception:
        abort(422)


# DELETE /drinks/<drinks_id> endpoint implemented as specified in the drinks.service.ts at the frontend
@app.route("/drinks/<int:drink_id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(payload, drink_id):

    try:
        # fetch drinks by fithering by the drink_id
        selection = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if selection is None:
            abort(404)

        # delete the selected drink_id in the front end and persists data in database
        selection.delete()

        selection = Drink.query.order_by(Drink.id).all()

        # returns the succes value and the long data representartion of drinks as specified in the drinks models table
        print(selection.id)
        return jsonify(
            {
                "success": True,
                "delete": selection.id,
            }
        )

    except Exception:
        abort(422)


############# Error handlers #############


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "bad request"}), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"success": False, "error": 401, "message": "unauthorized"}), 401


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404,
    )


@app.errorhandler(405)
def not_found(error):
    return (
        jsonify({"success": False, "error": 405, "message": "method not allowed"}),
        405,
    )


@app.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422, "message": "unprocessable"}),
        422,
    )


@app.errorhandler(500)
def not_found(error):
    return (
        jsonify({"success": False, "error": 500, "message": "Internal server error"}),
        500,
    )


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
