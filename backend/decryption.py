"""
Decryption module for AQIMC system
Contains the decryption functions and logic
"""

from aqimc import AQIMC


class AQIMCDecryption:
    """
    Decryption module for the Adaptive Quantum-Inspired Multi-Layer Cipher (AQIMC)
    """

    def __init__(self):
        self.aqimc = AQIMC()

    def decrypt_text(self, ciphertext: str, key1: str, key2: str, key3: str, key4: str) -> dict:
        """
        Decrypt the ciphertext using inverse AQIMC algorithm

        Args:
            ciphertext: Text to decrypt
            key1: Key for Layer 1 (DKSS)
            key2: Key for Layer 2 (NRPE)
            key3: Key for Layer 3 (VBMD)
            key4: Key for Layer 4 (KDPP)

        Returns:
            Dictionary containing decrypted text and step-by-step information
        """
        try:
            # Validate inputs
            if not all(isinstance(key, str) and len(key) > 0 for key in [key1, key2, key3, key4]):
                raise ValueError("All keys must be non-empty strings")

            if not isinstance(ciphertext, str) or len(ciphertext) == 0:
                raise ValueError("Ciphertext must be a non-empty string")

            # Perform step-by-step decryption
            steps = {}

            # Step 1 (inverse of Layer 4): KDPP
            step1_result = self.aqimc.layer4_kdpp_decrypt(ciphertext, key4)
            steps['KDPP_inverse'] = {
                'input': ciphertext,
                'output': step1_result,
                'description': 'Inverse Key-Driven Positional Permutation applied'
            }

            # Step 2 (inverse of Layer 3): VBMD
            step2_result = self.aqimc.layer3_vbmd_decrypt(step1_result, key3)
            steps['VBMD_inverse'] = {
                'input': step1_result,
                'output': step2_result,
                'description': 'Inverse Variable Block Matrix Diffusion applied'
            }

            # Step 3 (inverse of Layer 2): NRPE
            step3_result = self.aqimc.layer2_nrpe_decrypt(step2_result, key2)
            steps['NRPE_inverse'] = {
                'input': step2_result,
                'output': step3_result,
                'description': 'Inverse Non-Linear Relational Pair Encoding applied'
            }

            # Step 4 (inverse of Layer 1): DKSS
            final_result = self.aqimc.layer1_dkss_decrypt(step3_result, key1)
            steps['DKSS_inverse'] = {
                'input': step3_result,
                'output': final_result,
                'description': 'Inverse Dynamic Key-Shift Substitution applied'
            }

            return {
                'success': True,
                'decrypted_text': final_result,
                'steps': steps,
                'original_ciphertext': ciphertext
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'decrypted_text': None,
                'steps': {}
            }


if __name__ == "__main__":
    # Test the decryption module
    from encryption import AQIMCEncryption

    # First encrypt something
    encryptor = AQIMCEncryption()
    plaintext = "HELLO"
    key1 = "KEY1"
    key2 = "KEY2"
    key3 = "MATRIXKEY"
    key4 = "PERMUTE"

    encrypt_result = encryptor.encrypt_text(plaintext, key1, key2, key3, key4)
    print(f"Original plaintext: {plaintext}")
    print(f"Encrypted text: {encrypt_result['encrypted_text']}")

    # Now decrypt it
    decryptor = AQIMCDecryption()
    result = decryptor.decrypt_text(encrypt_result['encrypted_text'], key1, key2, key3, key4)

    print("\nDecryption Result:")
    print(f"Success: {result['success']}")
    print(f"Decrypted Text: {result['decrypted_text']}")

    if result['success']:
        print("\nStep-by-step process:")
        for layer, info in result['steps'].items():
            print(f"{layer}: {info['input']} -> {info['output']} ({info['description']})")

        print(f"\nDecryption successful: {plaintext.upper() == result['decrypted_text']}")