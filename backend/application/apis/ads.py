from application.models import *
from flask import jsonify, request
from application.database import db
from main import app
from application.auth import sponsor_required, admin_or_sponsor_required, admin_required, influencer_required
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/create-ad/<int:campaign_id>/<int:influencer_id>', methods=['POST'])
@jwt_required()
def create_ad(campaign_id, influencer_id):
    try:
        data = request.get_json()
        user = Users.query.filter_by(email=get_jwt_identity()['email']).first()
        if user:
            campaign = Campaigns.query.filter_by(id=campaign_id).first()
            if campaign:
                influencer = InfluencerBio.query.filter_by(id=influencer_id).first()
                if influencer:
                    ad = Ads(
                        campaign_id=campaign_id,
                        influencer_id=influencer_id,
                        messages=data['messages'],
                        requirements=data['requirements'],
                        payment_amount=data['payment_amount']
                    )
                    db.session.add(ad)
                    db.session.commit()
                    return jsonify({'message': 'Ad created successfully'}), 201
                else:
                    return jsonify({'message': 'Influencer does not exist'}), 404
            else:
                return jsonify({'message': 'Campaign does not exist'}), 404
        else:
            return jsonify({'message': 'User does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/ads', methods=['GET'])
@admin_required
def get_ads():
    try:
        ads = Ads.query.all()
        return jsonify([ad.serialize() for ad in ads]), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/ads/<int:id>', methods=['GET'])
@admin_required
def get_ad(id):
    try:
        ad = Ads.query.filter_by(id=id).first()
        if ad:
            return jsonify(ad.serialize()), 200
        else:
            return jsonify({'message': 'Ad does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/ads/<int:id>', methods=['PUT'])
@sponsor_required
def update_ad(id):
    try:
        data = request.get_json()
        sponsor = SponsorBio.query.filter_by(user_id=get_jwt_identity()).first()
        if sponsor:
            ad = Ads.query.filter_by(id=id).first()
            if ad:
                ad.messages = data['messages']
                ad.requirements = data['requirements']
                ad.payment_amount = data['payment_amount']
                db.session.commit()
                return jsonify({'message': 'Ad updated successfully'}), 200
            else:
                return jsonify({'message': 'Ad does not exist'}), 404
        else:
            return jsonify({'message': 'Sponsor User does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/ads/<int:id>', methods=['DELETE'])
@sponsor_required
def delete_ad(id):
    try:
        sponsor = SponsorBio.query.filter_by(user_id=get_jwt_identity()).first()
        if sponsor:
            ad = Ads.query.filter_by(id=id).first()
            if ad:
                db.session.delete(ad)
                db.session.commit()
                return jsonify({'message': 'Ad deleted successfully'}), 200
            else:
                return jsonify({'message': 'Ad does not exist'}), 404
        else:
            return jsonify({'message': 'Sponsor User does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/ads/get_influencer_ads/<int:influener_id>', methods=['GET'])
@jwt_required()
def get_influencer_ads(influencer_id):
    try:
        influencer = InfluencerBio.query.filter_by(id=influencer_id).first()
        if influencer:
            return jsonify([ad.serialize() for ad in influencer.ads]), 200
        else:
            return jsonify({'message': 'Influencer does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/ads/get_campaign_ads/<int:campaign_id>', methods=['GET'])
@admin_or_sponsor_required
def get_campaign_ads(campaign_id):
    try:
        campaign = Campaigns.query.filter_by(id=campaign_id).first()
        if campaign:
            return jsonify([ad.serialize() for ad in campaign.ads]), 200
        else:
            return jsonify({'message': 'Campaign does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/ads/<int:id>/accept', methods=['PUT'])
@influencer_required
def accept_ad(id):
    print(get_jwt_identity())
    try:
        influencer = InfluencerBio.query.filter_by(user_id=get_jwt_identity()['user_id']).first()
        if influencer:
            ad = Ads.query.filter_by(id=id).first()
            if ad:
                ad.status = 'accepted'
                db.session.commit()
                return jsonify({'message': 'Ad accepted'}), 200
            else:
                return jsonify({'message': 'Ad does not exist'}), 404
        else:
            return jsonify({'message': 'Influencer User does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/ads/<int:id>/reject', methods=['PUT'])
@influencer_required
def reject_ad(id):
    try:
        influencer = InfluencerBio.query.filter_by(user_id=get_jwt_identity()['user_id']).first()
        if influencer:
            ad = Ads.query.filter_by(id=id).first()
            if ad:
                ad.status = 'rejected'
                db.session.commit()
                return jsonify({'message': 'Ad rejected'}), 200
            else:
                return jsonify({'message': 'Ad does not exist'}), 404
        else:
            return jsonify({'message': 'Influencer User does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/ads/<int:id>/negotiate', methods=['PUT'])
@jwt_required()
def negotiate_ad(id):
    try:
        data = request.get_json()
        user = Users.query.filter_by(email=get_jwt_identity()).first()
        if user:
            ad = Ads.query.filter_by(id=id).first()
            if ad:
                ad.payment_amount = data['payment_amount']
                if user.user_type == 'sponsor':
                    ad.negotiation_turn = 'influencer'
                else:
                    ad.negotiation_turn = 'sponsor'
                db.session.commit()
                return jsonify({'message': 'Ad negotiated'}), 200
            else:
                return jsonify({'message': 'Ad does not exist'}), 404
        else:
            return jsonify({'message': 'User does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/get-pending-ads', methods=['GET'])
@influencer_required
def get_pending_ads():
    try:
        influencer = InfluencerBio.query.filter_by(user_id=get_jwt_identity()['user_id']).first()
        if influencer:
            ads = Ads.query.filter_by(influencer_id=influencer.id, status='pending').all()
           
            return jsonify([ad.serialize() for ad in ads]), 200
        else:
            return jsonify({'message': 'Influencer User does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

