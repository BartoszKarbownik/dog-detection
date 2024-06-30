from flask import Blueprint, request, jsonify, current_app
from ..models import User
import os

img_blueprint = Blueprint('img', __name__)


@img_blueprint.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = Image.query.get(image_id)
    if image and os.path.exists(image['filepath']):
        return send_from_directory(os.path.dirname(image.filepath), os.path.basename(image.filepath))
    return jsonify({'message': 'File not found'}), 404