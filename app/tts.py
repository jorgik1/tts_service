from flask import Blueprint, request, jsonify, send_file
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import io
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tts_bp = Blueprint('tts', __name__)

# Preload models at startup
try:
    logger.info("Preloading Bark models...")
    preload_models()
    logger.info("Models preloaded successfully.")
except Exception as e:
    logger.error(f"Error preloading models: {e}")
    raise

def text_to_speech(text):
    try:
        # Generate audio from text
        audio_array = generate_audio(text)
        return audio_array
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        raise

@tts_bp.route('/api/tts', methods=['POST'])
def tts():
    try:
        data = request.get_json()
        text = data.get('text', '')
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        audio = text_to_speech(text)
        wav_io = io.BytesIO()
        write_wav(wav_io, SAMPLE_RATE, audio)
        wav_io.seek(0)
        return send_file(wav_io, mimetype='audio/wav')
    except Exception as e:
        logger.error(f"Error in TTS endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500