from application.models import *
from flask import jsonify, request, send_file
from application.database import db
from main import app
from application.auth import sponsor_required, admin_or_sponsor_required, admin_required, influencer_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from application.celery_tasks import export_campigns
import pandas as pd
from io import BytesIO
import logging


@app.route('/create-campaign', methods=['POST'])
@sponsor_required
def create_campaign():
    try:
        data = request.get_json()
        sponsor = SponsorBio.query.filter_by(user_id=get_jwt_identity()['user_id']).first()
        if sponsor:
            new_campaign = Campaigns(
                sponsor_id=sponsor.id, 
                campaign_name=data['name'], 
                campaign_desc=data['description'], 
                campaign_start=datetime.strptime(data['start_date'], "%Y-%m-%d"), 
                campaign_end=datetime.strptime(data['end_date'], "%Y-%m-%d"), 
                campaign_budget=data['budget'], 
                campaign_visibility=data['visibility'], 
                influencer_id=data['influencer_id'], 
                campaign_goal=data['goal']
            )
            db.session.add(new_campaign)
            db.session.commit()
            return jsonify({'message': 'Campaign created successfully'}), 201
        else:
            return jsonify({'message': 'Sponsor User does not exist'}), 404
    except Exception as e:
        logging.error("Error occurred while creating campaign", exc_info=True)
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/campaigns', methods=['GET'])
@admin_or_sponsor_required
def get_campaigns():
    try:
        campaigns = Campaigns.query.all()
        return jsonify([campaign.serialize() for campaign in campaigns]), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500


@app.route('/public-campaigns', methods=['GET'])
@jwt_required()
def get_public_campaigns():
    try:
        campaigns = Campaigns.query.filter_by(
            campaign_visibility='public').all()
        return jsonify([campaign.serialize() for campaign in campaigns]), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/private-influencer-campaigns', methods=['GET'])
@jwt_required()
def get_public_influencer_campaigns():
    try:
        user_email = get_jwt_identity()['email']
        user = Users.query.filter_by(email=user_email).first()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        if user.user_type != 'influencer':
            return jsonify({'message': 'Only influencers can access this resource'}), 403
        influencer_bio = user.influencer_bio()
        if not influencer_bio:
            return jsonify({'message': 'Influencer bio not found'}), 404

        influencer_bio_id = influencer_bio.id
        campaigns = Campaigns.query.filter_by(
            campaign_visibility='private',
            influencer_id=influencer_bio_id  # Match influencer_bio.id with influencer_id in the campaigns
        ).all()
        if campaigns:
            return jsonify([campaign.serialize() for campaign in campaigns]), 200
        else:
            return jsonify({'message': 'No campaigns found for this influencer'}), 404

    except Exception as e:
        return jsonify({'message': 'Something went wrong', 'error': str(e)}), 500


@app.route('/campaigns/<int:id>', methods=['GET'])
def get_campaign(id):
    try:
        campaign = Campaigns.query.filter_by(id=id).first()
        if campaign:
            influencer = InfluencerBio.query.filter_by(id=campaign.influencer_id).first()

            campaign_data = campaign.serialize()

            if influencer:
                campaign_data['influencer'] = influencer.serialize()
            else:
                campaign_data['influencer'] = None

            return jsonify(campaign_data), 200
        else:
            return jsonify({'message': 'Campaign does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/campaigns/<int:id>', methods=['PUT'])
@jwt_required()  # Assuming you use JWT for authentication
def update_campaign(id):
    try:
        data = request.get_json()

        # Check if data contains all the required fields
        required_fields = ['name', 'description', 'start_date', 'end_date', 'budget', 'visibility', 'goal']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400

        # Fetch the campaign by id
        campaign = Campaigns.query.filter_by(id=id).first()
        if not campaign:
            return jsonify({'message': 'Campaign does not exist'}), 404

        # Get the current user and sponsor
        user = get_jwt_identity()
        sponsor = SponsorBio.query.filter_by(user_id=user['user_id']).first()
        if not sponsor:
            return jsonify({'message': 'Sponsor User does not exist'}), 404

        # Ensure the user exists
        user = Users.query.filter_by(id=user['user_id']).first()
        if not user:
            return jsonify({'message': 'User does not exist'}), 404

        # Update campaign details
        campaign.campaign_name = data['name']
        campaign.campaign_desc = data['description']
        campaign.campaign_start = datetime.strptime(data['start_date'], "%Y-%m-%d")
        campaign.campaign_end = datetime.strptime(data['end_date'], "%Y-%m-%d")
        campaign.campaign_budget = data['budget']
        campaign.campaign_visibility = data['visibility']
        campaign.influencer_id = data.get('influencer_id')  # Using .get() to avoid KeyError
        campaign.campaign_goal = data['goal']

        db.session.commit()

        return jsonify({
            'message': 'Campaign updated successfully',
            'username': user.username  # Include username in response if needed
        }), 200

    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/campaigns/<int:id>/status', methods=['PUT'])
@jwt_required()
def update_campaign_status(id):
    try:
        user_email = get_jwt_identity()['email']
        user = Users.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        campaign = Campaigns.query.filter_by(id=id).first()
        if not campaign:
            return jsonify({'message': 'Campaign does not exist'}), 404

        data = request.get_json()
        if 'status' not in data:
            return jsonify({'message': 'Missing required field: status'}), 400

        campaign.campaign_status = data['status']
        db.session.commit()

        return jsonify({'message': 'Campaign status updated successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'Something went wrong', 'error': str(e)}), 500

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error(f'Internal Server Error: {error}')
    return jsonify({'message': 'An internal server error occurred.'}), 500


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/campaigns/<int:id>', methods=['DELETE'])
@sponsor_required
def delete_campaign(id):
    try:
        campaign = Campaigns.query.filter_by(id=id).first()
        if campaign:
            sponsor = SponsorBio.query.filter_by(
                user_id=get_jwt_identity()['user_id']).first()
            if sponsor:
                db.session.delete(campaign)
                db.session.commit()
                return jsonify({'message': 'Campaign deleted successfully'}), 200
            else:
                return jsonify({'message': 'Sponsor User does not exist'}), 404
        else:
            return jsonify({'message': 'Campaign does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500


@app.route('/active-campaigns', methods=['GET'])
@admin_or_sponsor_required
def get_my_active_campaigns():
    try:
        sponsor = SponsorBio.query.filter_by(
            user_id=get_jwt_identity()['user_id']).first()
        if sponsor:
            campaigns = Campaigns.query.filter_by(sponsor_id=sponsor.id).all()
            return jsonify([campaign.serialize() for campaign in campaigns if campaign.campaign_end > datetime.now()]), 200
        else:
            return jsonify({'message': 'Sponsor User does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500


@app.route('/my-campaigns', methods=['GET'])
@sponsor_required
def get_my_campaigns():
    try:
        sponsor = SponsorBio.query.filter_by(
            user_id=get_jwt_identity()['user_id']).first()
        if sponsor:
            campaigns = Campaigns.query.filter_by(sponsor_id=sponsor.id).all()
            return jsonify([campaign.serialize() for campaign in campaigns]), 200
        else:
            return jsonify({'message': 'Sponsor User does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500


@app.route('/influencer-active-campaigns', methods=['GET'])
@influencer_required
def get_influencer_active_campaigns():
    try:
        influencer = InfluencerBio.query.filter_by(
            user_id=get_jwt_identity()['user_id']).first()
        if influencer:
            campaign_ids = Ads.query.filter_by(
                influencer_id=influencer.id).filter(Ads.status == 'accepted').all()
            # fetch all campaigns with the ids in campaign_ids
            campaigns = Campaigns.query.filter(Campaigns.id.in_(
                [ad.campaign_id for ad in campaign_ids])).all()
            return jsonify([campaign.serialize() for campaign in campaigns if campaign.campaign_end > datetime.now()]), 200
        else:
            return jsonify({'message': 'Influencer User does not exist'}), 404

    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500


@app.route('/flag-campaign/<int:id>', methods=['PUT'])
@admin_required
def flag_campaign(id):
    try:
        campaign = Campaigns.query.filter_by(id=id).first()
        if campaign:
            campaign.flagged = True
            db.session.commit()
            return jsonify({'message': 'Campaign flagged'}), 200
        else:
            return jsonify({'message': 'Campaign does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500


@app.route('/flagged-campaigns', methods=['GET'])
@admin_required
def get_flagged_campaigns():
    try:
        campaigns = Campaigns.query.filter_by(flagged=True).all()
        return jsonify([campaign.serialize() for campaign in campaigns]), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500


@app.route('/unflag-campaigns', methods=['GET'])
@admin_required
def get_unflagged_campaigns():
    try:
        campaigns = Campaigns.query.filter_by(flagged=False).all()
        return jsonify([campaign.serialize() for campaign in campaigns]), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500


@app.route('/export-campaigns', methods=['GET'])
@sponsor_required
def export_campaign_data():
    print('inside')
    try:
        sponsor = SponsorBio.query.filter_by(
            user_id=get_jwt_identity()['user_id']).first()
        if sponsor:
            export_campigns(sponsor.id)  # type: ignore
            return jsonify({'message': 'Campaigns exported'}), 200
        else:
            return jsonify({'message': 'Sponsor User does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
