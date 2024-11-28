import os
import warnings

# Umgebungsvariablen setzen
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["USE_TRITON"] = "0"  # Deaktiviert Triton bei Problemen

from flask import Flask, render_template, request, jsonify
from huggingface_hub import snapshot_download
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Warnungen unterdrücken
warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)

# Ordner für heruntergeladene Modelle
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Cache für geladene Modelle
loaded_models = {}

@app.route('/')
def index():
    # Verfügbare Modelle aus dem Ordner auflisten
    models = os.listdir(MODEL_DIR)
    return render_template('index.html', models=models)

@app.route('/download', methods=['POST'])
def download_model():
    model_name = request.form.get('model_name')
    print(f"Request to download model: {model_name}")  # Debug-Log
    try:
        # Modell von Hugging Face herunterladen
        model_path = snapshot_download(repo_id=model_name, cache_dir=MODEL_DIR)
        print(f"Model downloaded successfully to: {model_path}")  # Debug-Log
        return jsonify({'success': True, 'model': model_name})
    except Exception as e:
        print(f"Error downloading model: {e}")  # Debug-Log
        return jsonify({'success': False, 'error': str(e)})

@app.route('/chat', methods=['POST'])
def chat():
    model_name = request.json.get('model_name')
    user_input = request.json.get('user_input')
    params = request.json

    if not model_name:
        return jsonify({'success': False, 'error': 'Model name is required.'})
    if not user_input:
        return jsonify({'success': False, 'error': 'User input is required.'})

    print(f"Received chat request: model={model_name}, input={user_input}")

    # Überprüfen, ob das Modell bereits geladen ist
    if model_name not in loaded_models:
        print(f"Loading model: {model_name}")
        try:
            # Navigiere zu snapshots/<HASH>
            model_dir = os.path.join(MODEL_DIR, model_name, "snapshots")
            snapshot_subdirs = os.listdir(model_dir)
            if not snapshot_subdirs:
                raise EnvironmentError(f"No snapshots found for model {model_name} in {model_dir}")
            
            model_path = os.path.join(model_dir, snapshot_subdirs[0])

            # Modelltyp überprüfen und entsprechende Pipeline wählen
            if "t5" in model_name.lower():
                loaded_models[model_name] = pipeline(
                    "text2text-generation",
                    model=model_path,
                    device=-1
                )
            elif "gpt" in model_name.lower():
                loaded_models[model_name] = pipeline(
                    "text-generation",
                    model=model_path,
                    device=-1
                )
            elif "llama" in model_name.lower():
                loaded_models[model_name] = pipeline(
                    "text-generation",
                    model=model_path,
                    device=-1
                )
            elif "bart" in model_name.lower():
                loaded_models[model_name] = pipeline(
                    "text2text-generation",
                    model=model_path,
                    device=-1
                )
            else:
                raise ValueError(f"Unsupported model type for {model_name}")
        except Exception as e:
            print(f"Error loading model: {e}")
            return jsonify({'success': False, 'error': f"Failed to load model: {e}"})

    # Eingabe an das Modell senden
    try:
        do_sample = params.get('do_sample', True)  # Standard: True
        temperature = float(params.get('temperature', 0.7))

        response = loaded_models[model_name](
            user_input, 
            max_length=int(params.get('max_length', 100)), 
            temperature=temperature,
            do_sample=do_sample
        )

        # Benutzer-Nachricht und Modell-Antwort
        chat_history = {
            'user_message': user_input,
            'model_response': response[0]['generated_text']
        }
        return jsonify({'success': True, 'response': chat_history})
    except Exception as e:
        print(f"Error during text generation: {e}")
        return jsonify({'success': False, 'error': f"Failed to generate text: {e}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
