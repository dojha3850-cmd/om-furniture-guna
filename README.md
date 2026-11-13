# Om Furniture website — Guna, MP

## Included
- Responsive customer-facing website
- WhatsApp enquiry links and enquiry form
- Flask backend with SQLite enquiry storage
- Camera/gallery photo upload endpoint and project gallery
- Health check at `/health`

## Run locally
1. Install Python 3.10+.
2. Run `pip install -r requirements.txt`
3. Run `python app.py`
4. Open `http://localhost:5000`

## Deploy
Deploy this folder to a Python web host that supports Flask/Gunicorn and persistent storage.
- Build/install command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Set a persistent disk/storage path before using for production, and back up `om_furniture.db` and `static/uploads/`.
- Add a custom domain and enable HTTPS in your hosting provider's dashboard.

## Before public launch
- Replace the sample stock interior photos with your own project photos.
- Confirm the email address spelling and phone numbers.
- Add a privacy notice and business policies if you collect customer details.
- Configure backups and spam protection for public forms.
- The photo upload currently accepts image files up to 12 MB. Restrict upload access or add admin moderation before advertising the upload feature publicly.
