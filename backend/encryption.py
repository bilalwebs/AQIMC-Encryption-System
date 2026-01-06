"""
Encryption module for AQIMC system
Contains the encryption functions and logic
"""

from aqimc import AQIMC


class AQIMCEncryption:
    """
    Encryption module for the Adaptive Quantum-Inspired Multi-Layer Cipher (AQIMC)
    """

    def __init__(self):
        self.aqimc = AQIMC()

    def encrypt_text(self, plaintext: str, key1: str, key2: str, key3: str, key4: str) -> dict:
        """
        Encrypt the plaintext using AQIMC algorithm

        Args:
            plaintext: Text to encrypt
            key1: Key for Layer 1 (DKSS)
            key2: Key for Layer 2 (NRPE)
            key3: Key for Layer 3 (VBMD)
            key4: Key for Layer 4 (KDPP)

        Returns:
            Dictionary containing encrypted text and step-by-step information
        """
        try:
            # Validate inputs
            if not all(isinstance(key, str) and len(key) > 0 for key in [key1, key2, key3, key4]):
                raise ValueError("All keys must be non-empty strings")

            if not isinstance(plaintext, str) or len(plaintext) == 0:
                raise ValueError("Plaintext must be a non-empty string")

            # Perform step-by-step encryption
            steps = {}

            # Step 1: DKSS
            step1_result = self.aqimc.layer1_dkss_encrypt(plaintext, key1)
            steps['DKSS'] = {
                'input': plaintext,
                'output': step1_result,
                'description': 'Dynamic Key-Shift Substitution applied'
            }

            # Step 2: NRPE
            step2_result = self.aqimc.layer2_nrpe_encrypt(step1_result, key2)
            steps['NRPE'] = {
                'input': step1_result,
                'output': step2_result,
                'description': 'Non-Linear Relational Pair Encoding applied'
            }

            # Step 3: VBMD
            step3_result = self.aqimc.layer3_vbmd_encrypt(step2_result, key3)
            steps['VBMD'] = {
                'input': step2_result,
                'output': step3_result,
                'description': 'Variable Block Matrix Diffusion applied'
            }

            # Step 4: KDPP
            final_result = self.aqimc.layer4_kdpp_encrypt(step3_result, key4)
            steps['KDPP'] = {
                'input': step3_result,
                'output': final_result,
                'description': 'Key-Driven Positional Permutation applied'
            }

            return {
                'success': True,
                'encrypted_text': final_result,
                'steps': steps,
                'original_plaintext': plaintext
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'encrypted_text': None,
                'steps': {}
            }


if __name__ == "__main__":
    # Test the encryption module
    encryptor = AQIMCEncryption()

    plaintext = "HELLO"
    key1 = "KEY1"
    key2 = "KEY2"
    key3 = "MATRIXKEY"
    key4 = "PERMUTE"

    result = encryptor.encrypt_text(plaintext, key1, key2, key3, key4)

    print("Encryption Result:")
    print(f"Success: {result['success']}")
    print(f"Encrypted Text: {result['encrypted_text']}")

    if result['success']:
        print("\nStep-by-step process:")
        for layer, info in result['steps'].items():
            print(f"{layer}: {info['input']} -> {info['output']} ({info['description']})")