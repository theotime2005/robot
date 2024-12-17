# Create virtual environment
echo "Creating virtual environment"
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment"
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies"
pip install -r requirements.txt

# Check if Ollama is installed
echo "Checking if Ollama is installed"
if command -v ollama &> /dev/null; then
    echo "Ollama is installed."
    # Check if llama3.2-vision model is available
    echo "Checking if model 'llama3.2-vision' is installed"
    if ollama list | grep -q "llama3.2-vision"; then
        echo "Model 'llama3.2-vision' is already installed."
    else
        echo "Model 'llama3.2-vision' not found. Downloading now..."
        ollama pull llama3.2-vision
    fi
else
    echo "Ollama is not installed. Please install it before proceeding."
    exit 1
fi

echo "Setup complete"
echo "Run this command to activate virtual environment:"
echo "source .venv/bin/activate"
