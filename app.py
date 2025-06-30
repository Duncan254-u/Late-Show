from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Episode, Guest, Appearance
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.route('/episodes', methods=['GET'])
def index():
    return jsonify({
          "message": "Welcome to the Late Show API",
        "endpoints": [
            "GET /episodes",
            "GET /episodes/<id>",
            "GET /guests",
            "POST /appearances"
        ]
    })

@app.route('/episodes/<int:episode_id>', methods=['GET'])
def get_episode_by_id(episode_id):
    try:
        episode = Episode.query.get(episode_id)
        if not episode:
            return jsonify({"error": "Episode not found"}), 404
        episode_data = episode.to_dict(only=('id', 'date', 'number', 'appearances'))
        
        formatted_appearances = []
        for appearance in episode.appearances:
            appearance_data = {
                "id": appearance.id,
                "rating": appearance.rating,
                "episode_id": appearance.episode_id,
                "guest_id": appearance.guest_id,
                "guest": appearance.guest.to_dict(only=('id', 'name', 'occupation'))
            }
            formatted_appearances.append(appearance_data)
        episode_data['appearances'] = formatted_appearances
        return jsonify(episode_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/guests', methods=['GET'])
def get_guests():
    try:
        guests = Guest.query.all()
        # Serialize guests, excluding appearances for this endpoint
        guests_data = [guest.to_dict(only=('id', 'name', 'occupation')) for guest in guests]
        return jsonify(guests_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/appearances', methods=['POST'])
def create_appearance():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"errors": ["No data provided"]}), 400
        
        required_fields = ['rating', 'episode_id', 'guest_id']
        errors = []
        for field in required_fields:
            if field not in data:
                errors.append(f"{field} is required")
        if errors:
            return jsonify({"errors": errors}), 400
        
        episode = Episode.query.get(data['episode_id'])
        guest = Guest.query.get(data['guest_id'])
        if not episode:
            errors.append("Episode not found")
        if not guest:
            errors.append("Guest not found")
        if errors:
            return jsonify({"errors": errors}), 404
        
        appearance = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        db.session.add(appearance)
        db.session.commit()

        appearance_data = {
            "id": appearance.id,
            "rating": appearance.rating,
            "episode_id": appearance.episode_id,
            "guest_id": appearance.guest_id,
            "guest": appearance.guest.to_dict(only=('id', 'name', 'occupation'))
        }
        return jsonify(appearance_data), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Resource not found"}), 404
@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)












        


