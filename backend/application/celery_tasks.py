from main import app, celery, mail
from application.models import SponsorBio, Users, InfluencerBio, Ads, Campaigns
from flask_mail import Message
from flask import render_template_string
from datetime import datetime
from pytz import timezone


@celery.task
def daily_visit_reminder():
    with app.app_context():
        influencers = InfluencerBio.query.all()
        for i in influencers:
            with open('influencers.txt', 'a') as f:
                f.write(f"{i.name} {i.niche}\n")
            user = Users.query.get(i.user_id)
            to = user.email
            ads = Ads.query.filter_by(
                influencer_id=i.id, status='pending').all()
            if len(ads) == 0:
                continue

            subject = "Daily Visit Reminder"
            body = f"Hello {i.name},\n\nYou have {len(ads)} ads requests pending. You can review them from you dashboard.\n\nThank you."
            msg = Message(subject, recipients=[to], body=body)
            try:
                mail.send(msg)
            except Exception as e:
                print(e)
                continue


@celery.task
def export_campigns(sponsor_id):
    with app.app_context():
        campaigns = Campaigns.query.filter_by(
            sponsor_id=sponsor_id).all()
        sponsor = SponsorBio.query.get(sponsor_id)
        user = Users.query.get(sponsor.user_id)
        to = user.email
        with open('campaigns.csv', 'w') as f:
            f.write(
                "ID,Name,Description,Budget,Start,End,Flagged,Campaign Visibility,Goal\n")
        with open('campaigns.csv', 'a') as f:
            for campaign in campaigns:
                f.write(
                    f"{campaign.id},{campaign.campaign_name},{campaign.campaign_desc},{sponsor.budget},{campaign.campaign_start},{campaign.campaign_end},{campaign.flagged},{campaign.campaign_visibility},{campaign.campaign_goal}\n")
        with open('campaigns.csv', 'r') as f:
            msg = Message("Campaigns Export", recipients=[to,
                          'abulaman6@gmail.com'], body="Campaigns exported successfully")
            msg.attach('campaigns.csv', 'text/csv', f.read())
            mail.send(msg)


@celery.task
def monthly_report():
    with app.app_context():
        template_string = """
<html>
    <head>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: center;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h1>Monthly Report</h1>
        <table>
            <tr>
                <th>Name</th>
                <th>Budget</th>
                <th>start</th>
                <th>end</th>
                <th>visilibity</th>

            </tr>
            {% for camp in campaigns %}
            <tr>
                <td>{{ camp.campaign_name }}</td>
                <td>{{ camp.budget }}</td>
                <td>{{ camp.campaign_start }}</td>
                <td>{{ camp.campaign_end }}</td>
                <td>{{ camp.campaign_visibility }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
</html>
        """

        sponsors = SponsorBio.query.all()
        for sponsor in sponsors:
            user = Users.query.get(sponsor.user_id)
            campaigns = Campaigns.query.filter_by(
                sponsor_id=sponsor.id).all()

            rendered = render_template_string(
                template_string, campaigns=campaigns)
            to = user.email
            subject = "Monthly Report"
            msg = Message(subject, recipients=[to], html=rendered)
            try:
                mail.send(msg)
            except Exception as e:
                print(e)
                continue
