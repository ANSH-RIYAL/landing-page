from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, Response
from flask_pymongo import PyMongo
from datetime import datetime
from functools import wraps
import config
import os
import csv
from io import StringIO

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config["MONGO_URI"] = config.MONGO_URI
app.config["MONGO_DBNAME"] = config.DB_NAME

mongo = PyMongo(app)

# Admin login required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/coming-soon')
def coming_soon():
    return render_template('coming_soon.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == config.ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid password', 'error')
    
    # Get stats from MongoDB if logged in
    if session.get('admin_logged_in'):
        subscribers = mongo.db.subscribers.find()
        interest_clicks = mongo.db.interest_tracking.find()
        contact_messages = mongo.db.contact_messages.find()
        return render_template('admin/admin.html', 
                             subscribers=subscribers,
                             interest_clicks=interest_clicks,
                             contact_messages=contact_messages)
    
    return render_template('admin/admin.html')

@app.route('/admin/download-stats')
@admin_required
def admin_download_stats():
    # Create CSV file
    output = StringIO()
    writer = csv.writer(output)
    
    # Write summary section
    writer.writerow(['Grocer Ease Statistics'])
    writer.writerow(['Generated on:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow([])
    
    # Write subscriber details
    writer.writerow(['Subscribers'])
    writer.writerow(['Email', 'Timestamp', 'Source'])
    for subscriber in mongo.db.subscribers.find():
        writer.writerow([
            subscriber.get('email', ''),
            subscriber.get('timestamp', ''),
            subscriber.get('source', '')
        ])
    writer.writerow([])
    
    # Write interest clicks
    writer.writerow(['Interest Clicks'])
    writer.writerow(['Source', 'Timestamp', 'IP Address'])
    for click in mongo.db.interest_tracking.find():
        writer.writerow([
            click.get('source', ''),
            click.get('timestamp', ''),
            click.get('ip_address', '')
        ])
    writer.writerow([])
    
    # Write contact messages
    writer.writerow(['Contact Messages'])
    writer.writerow(['Email', 'Message', 'Timestamp'])
    for message in mongo.db.contact_messages.find():
        writer.writerow([
            message.get('email', ''),
            message.get('message', ''),
            message.get('timestamp', '')
        ])
    
    output.seek(0)
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=grocer_ease_full_stats.csv'}
    )

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.get_json()
        email = data.get('email')
        source = data.get('source', 'website')
        
        if not email:
            return jsonify({'status': 'error', 'message': 'Email is required'}), 400
        
        # Save to MongoDB
        mongo.db.subscribers.insert_one({
            'email': email,
            'timestamp': datetime.now(),
            'source': source
        })
        
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error saving subscriber: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/interest/count')
def get_count():
    try:
        count = mongo.db.interest_tracking.count_documents({})
        return jsonify({'count': count})
    except Exception as e:
        print(f"Error getting interest count: {str(e)}")
        return jsonify({'count': 0})

@app.route('/api/interest', methods=['POST'])
def track_interest():
    try:
        data = request.get_json()
        source = data.get('source', 'unknown')
        
        # Get IP address
        ip_address = request.remote_addr
        if 'X-Forwarded-For' in request.headers:
            ip_address = request.headers['X-Forwarded-For'].split(',')[0]
        
        # Save to MongoDB
        mongo.db.interest_tracking.insert_one({
            'source': source,
            'timestamp': datetime.now(),
            'ip_address': ip_address
        })
        
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error tracking interest: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        if not email or not message or not name:
            return jsonify({'status': 'error', 'message': 'Name, email and message are required'}), 400
        
        # Save to MongoDB
        mongo.db.contact_messages.insert_one({
            'name': name,
            'email': email,
            'message': message,
            'timestamp': datetime.now()
        })
        
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error saving contact message: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 