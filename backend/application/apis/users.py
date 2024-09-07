from application.models import *
from flask import jsonify, request
from application.database import db
from main import app
from application.auth import admin_required
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        user = Users.query.filter_by(email=data['email']).first()
        if user:
            return jsonify({'message': 'User already exists'}), 409
        else:
            b=Bcrypt()
            hashed_password = b.generate_password_hash(data['password'])
            new_user = Users(email=data['email'], username=data['username'] ,password=hashed_password, user_type=data['user_type'])
            db.session.add(new_user)
            db.session.commit()
            if data['user_type'] == 'influencer':
                new_influencer = InfluencerBio(user_id=new_user.id, name=data['name'], category=data['category'], niche=data['niche'])
                db.session.add(new_influencer)
                db.session.commit()
            elif data['user_type'] == 'sponsor':
                new_sponsor = SponsorBio(user_id=new_user.id, name=data['name'], industry=data['industry'], budget=data['budget'])
                db.session.add(new_sponsor)
                db.session.commit()
            access_token = create_access_token(
                identity={"email": data['email'], "user_id": new_user.id}, additional_claims={"user_type": data['user_type']}
            )
            return jsonify({"token": access_token, "user": new_user.username, "user_type": new_user.user_type}), 201
            
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = Users.query.filter_by(email=data['email']).first()
        if user:
            b=Bcrypt()
            if b.check_password_hash(user.password, data['password']):
                if user.user_type == 'sponsor':
                    sponsor = SponsorBio.query.filter_by(user_id=user.id).first()
                    if not sponsor.approved:
                        return jsonify({'message': 'Sponsor not approved yet'}), 403
                #check if admin and pass admin to frontend
                access_token = create_access_token(
                identity={"email":user.email, "user_id": user.id}, additional_claims={"user_type": user.user_type}
                    )
                print(user.user_type)
                return jsonify({"token": access_token, "user": user.username, "user_type": user.user_type }), 200
            else:
                return jsonify({'message': 'Invalid password'}), 401
        else:
            return jsonify({'message': 'User does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = Users.query.all()
        return jsonify([user.serialize() for user in users]), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    try:
        user = Users.query.get(id)
        if user:
            return jsonify({'user': user.serialize()}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/current_user', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user = Users.query.filter_by(email=get_jwt_identity()['email']).first()
        return jsonify({'user': user.serialize()}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route("/users/approve_sponsor/<int:id>", methods=['PUT'])
@admin_required
def approve_sponsor(id):
    try:
        sponsor = SponsorBio.query.filter_by(user_id=id).first()
        if sponsor:
            sponsor.approved = True
            db.session.commit()
            return jsonify({'message': 'Sponsor approved'}), 200
        else:
            return jsonify({'message': 'Sponsor not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route("/influencers", methods=['GET'])
@jwt_required()
def get_all_influencers():
    try:
        influencers = InfluencerBio.query.all()
        return jsonify([influencer.serialize() for influencer in influencers]), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route("/user", methods=["PUT"])
@jwt_required()
def update_user():
    try:
        data = request.get_json()
        # Check if data contains all the required fields
        required_fields = ['username', "current_password", "new_password", "confirm_password"]
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400

        user = Users.query.filter_by(email=get_jwt_identity()['email']).first()
        user.username = data['username']
        b=Bcrypt()
        stored_hashed_password = user.password
        if b.check_password_hash(stored_hashed_password, data['current_password']):
            if (data['new_password'] != data['confirm_password']):
                return jsonify({'message': 'New password and confirm password doesn''t match '}), 404
            hashed_password = b.generate_password_hash(data['new_password'])
            user.password = hashed_password

            db.session.commit()
            return jsonify({'user': user.serialize()}), 200
        else:
            return jsonify({'message': 'Password is incorrect'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500