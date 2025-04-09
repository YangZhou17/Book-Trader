from flask import Blueprint, request, jsonify
from extensions import db
from models import User, Follower, Following

follows_bp = Blueprint('follows', __name__)

@follows_bp.route('/follow', methods=['POST'])
def follow_user():
    data = request.get_json()
    follower_name = data.get('follower_name')
    followed_name = data.get('followed_name')

    if not follower_name or not followed_name:
        return jsonify({'success': False, 'message': 'Missing follower_name or followed_name'}), 400
    if follower_name == followed_name:
        return jsonify({'success': False, 'message': 'A user cannot follow themselves.'}), 400

    follower_user = User.query.filter_by(username=follower_name).first()
    followed_user = User.query.filter_by(username=followed_name).first()
    if not follower_user or not followed_user:
        return jsonify({'success': False, 'message': 'User(s) not found'}), 404

    existing_following = Following.query.filter_by(
        user_id=follower_user.id,
        following_id=followed_user.id
    ).first()
    if existing_following:
        return jsonify({
            'success': False,
            'message': f'{follower_name} is already following {followed_name}'
        }), 400

    new_following = Following(
        user_id=follower_user.id,
        following_id=followed_user.id
    )
    
    new_follower = Follower(
        user_id=followed_user.id,
        follower_id=follower_user.id
    )

    db.session.add(new_following)
    db.session.add(new_follower)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'{follower_name} is now following {followed_name}'
    }), 200

@follows_bp.route('/unfollow', methods=['POST'])
def unfollow_user():
    data = request.get_json()
    follower_name = data.get('follower_name')
    followed_name = data.get('followed_name')

    if not follower_name or not followed_name:
        return jsonify({'success': False, 'message': 'Missing follower_name or followed_name'}), 400
    if follower_name == followed_name:
        return jsonify({'success': False, 'message': 'A user cannot unfollow themselves.'}), 400

    follower_user = User.query.filter_by(username=follower_name).first()
    followed_user = User.query.filter_by(username=followed_name).first()
    if not follower_user or not followed_user:
        return jsonify({'success': False, 'message': 'User(s) not found'}), 404

    existing_following = Following.query.filter_by(
        user_id=follower_user.id,
        following_id=followed_user.id
    ).first()
    if existing_following:
        db.session.delete(existing_following)

    existing_follower = Follower.query.filter_by(
        user_id=followed_user.id,
        follower_id=follower_user.id
    ).first()
    if existing_follower:
        db.session.delete(existing_follower)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'{follower_name} has unfollowed {followed_name}'
    }), 200

@follows_bp.route('/<username>/followers', methods=['GET'])
def get_followers(username):
    """
    Fetch all users who follow <username>.
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    follower_records = Follower.query.filter_by(user_id=user.id).all()

    followers_list = []
    for record in follower_records:
        follower_user = db.session.get(User,record.follower_id)
        if follower_user:
            followers_list.append({'name': follower_user.username})

    return jsonify(followers_list), 200

@follows_bp.route('/<username>/following', methods=['GET'])
def get_following(username):
    """
    Fetch all users <username> is following.
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    following_records = Following.query.filter_by(user_id=user.id).all()

    following_list = []
    for record in following_records:
        followed_user = db.session.get(User,record.following_id)
        if followed_user:
            following_list.append({'name': followed_user.username})

    return jsonify(following_list), 200
