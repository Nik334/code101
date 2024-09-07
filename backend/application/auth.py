from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims["user_type"] == "admin":
            return fn(*args, **kwargs)
        else:
            return jsonify(msg="Admins only!"), 403

    return decorator

def influencer_required(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims["user_type"] == "influencer":
            return fn(*args, **kwargs)
        else:
            return jsonify(msg="Influencers only!"), 403

    return decorator

def sponsor_required(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims["user_type"] == "sponsor":
            return fn(*args, **kwargs)
        else:
            return jsonify(msg="Sponsors only!"), 403

    return decorator

def admin_or_sponsor_required(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims["user_type"] == "admin" or claims["user_type"] == "sponsor":
            return fn(*args, **kwargs)
        else:
            return jsonify(msg="Admins or Sponsors only!"), 403

    return decorator