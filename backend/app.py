"""
Flask API for AQIMC Encryption System
Provides REST endpoints for encryption and decryption
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from encryption import AQIMCEncryption
from decryption import AQIMCDecryption
import re


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize encryption/decryption modules
encryptor = AQIMCEncryption()
decryptor = AQIMCDecryption()


def validate_text(text):
    """Validate that text contains only alphabetic characters and spaces"""
    if not isinstance(text, str) or len(text) == 0:
        return False, "Text must be a non-empty string"

    # Allow uppercase/lowercase letters and spaces
    if not re.match(r'^[A-Za-z\s]*$', text):
        return False, "Text can only contain letters and spaces"

    return True, ""


def validate_key(key):
    """Validate that key contains only alphabetic characters"""
    if not isinstance(key, str) or len(key) == 0:
        return False, "Key must be a non-empty string"

    # Allow uppercase/lowercase letters
    if not re.match(r'^[A-Za-z]+$', key):
        return False, "Key can only contain alphabetic characters"

    return True, ""


@app.route('/')
def home():
    return jsonify({
        'message': 'AQIMC Encryption System API',
        'endpoints': {
            'encrypt': '/encrypt (POST)',
            'decrypt': '/decrypt (POST)'
        }
    })


@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        plaintext = data.get('plaintext', '').strip()
        key1 = data.get('key1', '').strip()
        key2 = data.get('key2', '').strip()  # Added Key 2
        key3 = data.get('key3', '').strip()
        key4 = data.get('key4', '').strip()

        # Validate inputs
        is_valid, error_msg = validate_text(plaintext)
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400

        for key, key_name in [(key1, 'key1'), (key2, 'key2'), (key3, 'key3'), (key4, 'key4')]:  # Include key2
            is_valid, error_msg = validate_key(key)
            if not is_valid:
                return jsonify({'success': False, 'error': f'{key_name}: {error_msg}'}), 400

        # Perform encryption
        result = encryptor.encrypt_text(plaintext, key1, key2, key3, key4)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred during encryption: {str(e)}'
        }), 500


@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        ciphertext = data.get('ciphertext', '').strip()
        key1 = data.get('key1', '').strip()
        key2 = data.get('key2', '').strip()  # Added Key 2
        key3 = data.get('key3', '').strip()
        key4 = data.get('key4', '').strip()

        # Validate inputs
        is_valid, error_msg = validate_text(ciphertext)
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400

        for key, key_name in [(key1, 'key1'), (key2, 'key2'), (key3, 'key3'), (key4, 'key4')]:  # Include key2
            is_valid, error_msg = validate_key(key)
            if not is_valid:
                return jsonify({'success': False, 'error': f'{key_name}: {error_msg}'}), 400

        # Perform decryption
        result = decryptor.decrypt_text(ciphertext, key1, key2, key3, key4)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred during decryption: {str(e)}'
        }), 500


@app.route('/test', methods=['GET'])
def test():
    """Test endpoint to verify the system works"""
    try:
        # Test with a simple example
        plaintext = "HELLO"
        key1 = "TEST"
        key2 = "TEST2"  # Added Key 2
        key3 = "TESTKEY"
        key4 = "PERM"

        encrypt_result = encryptor.encrypt_text(plaintext, key1, key2, key3, key4)

        if encrypt_result['success']:
            ciphertext = encrypt_result['encrypted_text']
            decrypt_result = decryptor.decrypt_text(ciphertext, key1, key2, key3, key4)

            if decrypt_result['success']:
                return jsonify({
                    'success': True,
                    'message': 'System is working correctly',
                    'test_plaintext': plaintext,
                    'encrypted': ciphertext,
                    'decrypted': decrypt_result['decrypted_text'],
                    'match': plaintext.upper() == decrypt_result['decrypted_text']
                })

        return jsonify({
            'success': False,
            'message': 'System test failed'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Test failed: {str(e)}'
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)