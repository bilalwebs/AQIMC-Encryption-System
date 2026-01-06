# Adaptive Quantum-Inspired Multi-Layer Cipher (AQIMC) Encryption System

## Overview

The Adaptive Quantum-Inspired Multi-Layer Cipher (AQIMC) is an educational encryption system that implements a four-layer encryption algorithm designed to demonstrate advanced cryptographic principles. This system is suitable for academic projects, final year submissions, and research presentations.

## Algorithm Design

The AQIMC algorithm consists of four sequential layers, each designed to enhance security through different cryptographic techniques:

### Layer 1: Dynamic Key-Shift Substitution (DKSS)
- **Formula**: Cᵢ = (Pᵢ + K₁[i mod |K₁|] + i) mod 26
- **Purpose**: Break frequency analysis by shifting characters based on position and key

### Layer 2: Non-Linear Relational Pair Encoding (NRPE)
- **Formula**: C₁ = (a + 2b) mod 26, C₂ = |a - b|
- **Purpose**: Destroy linguistic structure by processing characters in pairs

### Layer 3: Variable Block Matrix Diffusion (VBMD)
- **Formula**: C = K₃ × P (mod 26)
- **Block Sizes**: 2×2, 3×3, or 4×4 matrices based on key length
- **Purpose**: Create diffusion and avalanche effect through matrix multiplication

### Layer 4: Key-Driven Positional Permutation (KDPP)
- **Method**: Permute final ciphertext positions using key K₄
- **Purpose**: Hide sequence and order information

## Project Structure

```
AQIMC-Encryption-System/
├── backend/
│   ├── aqimc.py          # Core AQIMC algorithm implementation
│   ├── encryption.py     # Encryption module
│   ├── decryption.py     # Decryption module
│   └── app.py           # Flask API endpoints
├── frontend/
│   ├── index.html       # Main HTML interface
│   ├── style.css        # Styling and layout
│   └── script.js        # Frontend JavaScript logic
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies
```

## Installation

1. Clone or download the project
2. Navigate to the project directory
3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Backend (API)

1. Start the Flask server:
```bash
cd backend
python app.py
```

The API will start on `http://localhost:5000`

### API Endpoints

- **Encrypt**: `POST /encrypt`
```json
{
  "plaintext": "HELLO",
  "key1": "KEY1",
  "key2": "KEY2",
  "key3": "MATRIXKEY",
  "key4": "PERMUTE"
}
```

- **Decrypt**: `POST /decrypt`
```json
{
  "ciphertext": "ENCRYPTED_TEXT",
  "key1": "KEY1",
  "key2": "KEY2",
  "key3": "MATRIXKEY",
  "key4": "PERMUTE"
}
```

### Frontend

1. Start the Flask server (as described above)
2. Open `frontend/index.html` in a web browser
3. Enter your plaintext and keys
4. Click "Encrypt" to encrypt or "Decrypt" to decrypt

## How to Use the System

### 1. Plaintext Input
- This is the text you want to encrypt
- Example: "HELLO" or "my name is ahmad" (both uppercase and lowercase supported)
- Only letters (A-Z, a-z) and spaces are allowed
- The system will automatically convert lowercase to uppercase for processing

### 2. The Four Keys (Very Important!)
You need to provide 4 different keys for the 4-layer encryption:

- **Key 1 (DKSS)**: For Dynamic Key-Shift Substitution
  - Example: "KEYA", "secret", "MyPass" (both uppercase and lowercase supported)
  - Must contain only letters (A-Z, a-z), no numbers or symbols

- **Key 2 (NRPE)**: For Non-Linear Relational Pair Encoding
  - Example: "KEYB", "magic", "Code2" (both uppercase and lowercase supported)
  - Must contain only letters (A-Z, a-z), no numbers or symbols

- **Key 3 (VBMD)**: For Variable Block Matrix Diffusion
  - Example: "MATRIX", "longkey", "vbmdkey" (both uppercase and lowercase supported)
  - Can be longer, must contain only letters

- **Key 4 (KDPP)**: For Key-Driven Positional Permutation
  - Example: "PERMUTE", "finalkey", "endkey" (both uppercase and lowercase supported)
  - Must contain only letters (A-Z, a-z)

### 3. Example Usage
- **Plaintext**: `Hello` or `hello` (both work)
- **Key 1**: `keya` or `KEYA` (both work)
- **Key 2**: `keyb` or `KEYB` (both work)
- **Key 3**: `matrix` or `MATRIX` (both work)
- **Key 4**: `permute` or `PERMUTE` (both work)

### 4. Step-by-Step Process
1. Write your message in the "Plaintext" box (uppercase or lowercase)
2. Enter 4 different keys in the 4 key boxes (uppercase or lowercase)
3. Click "Encrypt" button
4. The encrypted text will appear in "Ciphertext" box
5. To decrypt: Make sure you have the same 4 keys and click "Decrypt"

### 5. Important Rules
- **All keys must contain only letters (A-Z, a-z)** - no numbers or symbols
- **You must remember the same 4 keys** to decrypt your message later
- **Each key should be different** for better security
- **For decryption**: You must use exactly the same 4 keys that were used for encryption
- **Case insensitive**: The system handles both uppercase and lowercase input

## Example Usage

**Plaintext**: `HELLO`
**Key 1 (DKSS)**: `KEYA`
**Key 2 (NRPE)**: `KEYB`
**Key 3 (VBMD)**: `MATRIX`
**Key 4 (KDPP)**: `PERMUTE`

The system will process the text through all four layers, providing both the final encrypted result and step-by-step visualization of each layer's transformation.

## Visualization Features

The system includes real-time visualization of each encryption layer:
- **DKSS Layer**: Shows how characters are shifted based on position and key
- **NRPE Layer**: Shows how character pairs are transformed using non-linear equations
- **VBMD Layer**: Shows how matrix multiplication diffuses the data
- **KDPP Layer**: Shows how positions are permuted based on the key

## Security Analysis

### Strengths
- **Multi-layered approach**: Four distinct layers provide layered security
- **Positional dependence**: DKSS layer incorporates character position
- **Non-linear transformation**: NRPE layer uses non-linear mathematical operations
- **Matrix diffusion**: VBMD layer provides diffusion properties
- **Positional scrambling**: KDPP layer conceals order information

### Limitations
- **Key management**: Requires careful key distribution and storage
- **Computational overhead**: Multiple layers increase processing time
- **Block padding**: VBMD layer may require padding for proper matrix operations

## Academic Applications

This system is ideal for:
- Final year computer science projects
- Cryptography course assignments
- Academic research on multi-layered encryption
- Educational demonstrations of cryptographic principles
- Presentation at academic conferences

## Viva Preparation Points

### Algorithm Understanding
1. Explain each of the four layers and their purposes
2. Discuss the mathematical formulas used in each layer
3. Describe the inverse operations for decryption
4. Analyze the security properties of each layer

### Implementation Details
1. Explain the Python implementation of the algorithm
2. Describe the Flask API architecture
3. Discuss the frontend implementation and user interface
4. Address any challenges faced during implementation

### Security Analysis
1. Compare with classical encryption methods
2. Discuss the advantages of multi-layered encryption
3. Address potential vulnerabilities
4. Propose future improvements

## Deployment

### Deploying to Vercel (Frontend Only)

To deploy the frontend to Vercel:

1. Update the API endpoint in `frontend/script.js` to point to your deployed backend:
   ```javascript
   const API_BASE_URL = 'https://your-backend.onrender.com'; // Replace with your actual backend URL
   ```

2. Add the `vercel.json` file to configure static hosting

3. Deploy to Vercel using the Vercel CLI or GitHub integration

### Backend Deployment Options

The backend needs to be deployed separately. Options include:

1. **Render.com**:
   - Create a new web service
   - Connect to your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python backend/app.py`

2. **Heroku**:
   - Create a new app
   - Connect to GitHub
   - Deploy manually or enable automatic deploys

3. **Railway**:
   - Import your GitHub repository
   - Add requirements.txt for dependencies
   - Deploy the backend service

### Important Notes for Deployment:
- The frontend and backend must be deployed separately
- Update the API URL in frontend to match your deployed backend
- Ensure CORS is properly configured for cross-origin requests

## Future Improvements

1. **Enhanced Key Management**: Implement secure key generation and distribution
2. **Performance Optimization**: Optimize the algorithm for larger text processing
3. **Additional Layers**: Consider adding more cryptographic layers
4. **Quantum Resistance**: Research quantum-resistant modifications
5. **Hybrid Approach**: Combine with existing encryption standards (AES, RSA)

## Conclusion

The AQIMC system demonstrates the principles of multi-layered encryption with a unique approach that combines substitution, non-linear encoding, matrix diffusion, and positional permutation. While designed for educational purposes, it showcases how combining multiple cryptographic techniques can enhance security through layered protection.

The system provides a practical demonstration of advanced cryptographic concepts suitable for academic study and research.