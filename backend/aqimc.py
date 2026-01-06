"""
Adaptive Quantum-Inspired Multi-Layer Cipher (AQIMC)
Implementation of the four-layer encryption algorithm
"""

import numpy as np
from typing import List, Tuple, Union
import math


class AQIMC:
    """
    Adaptive Quantum-Inspired Multi-Layer Cipher (AQIMC)

    Implements a four-layer encryption algorithm:
    1. Dynamic Key-Shift Substitution (DKSS)
    2. Non-Linear Relational Pair Encoding (NRPE)
    3. Variable Block Matrix Diffusion (VBMD)
    4. Key-Driven Positional Permutation (KDPP)
    """

    def __init__(self):
        pass

    def _text_to_numbers(self, text: str) -> List[int]:
        """Convert text to numbers (A=0, B=1, ..., Z=25)"""
        return [ord(char.upper()) - ord('A') for char in text if char.isalpha()]

    def _numbers_to_text(self, numbers: List[int]) -> str:
        """Convert numbers back to text (0=A, 1=B, ..., 25=Z)"""
        result = ""
        for num in numbers:
            result += chr((num % 26) + ord('A'))
        return result

    def _pad_to_even(self, numbers: List[int]) -> List[int]:
        """Pad list with 'A' (0) to make it even length for pair processing"""
        if len(numbers) % 2 != 0:
            numbers.append(0)  # Pad with 'A'
        return numbers

    def _get_matrix_inverse(self, matrix: np.ndarray) -> np.ndarray:
        """Get modular inverse of a matrix under mod 26"""
        try:
            det = int(np.round(np.linalg.det(matrix)))
            det_inv = pow(det, -1, 26)  # Modular multiplicative inverse of determinant
            adj = np.round(det * np.linalg.inv(matrix)).astype(int) % 26
            inv_matrix = (det_inv * adj) % 26
            return inv_matrix.astype(int)
        except:
            # If determinant is not invertible, create a new valid matrix
            raise ValueError("Matrix is not invertible under mod 26")

    # Layer 1: Dynamic Key-Shift Substitution (DKSS)
    def layer1_dkss_encrypt(self, plaintext: str, key1: str) -> str:
        """
        Layer-1: Dynamic Key-Shift Substitution (DKSS)
        Formula: Cᵢ = (Pᵢ + K₁[i mod |K₁|] + i) mod 26
        Purpose: break frequency analysis
        """
        numbers = self._text_to_numbers(plaintext)
        key_numbers = self._text_to_numbers(key1)

        result = []
        for i, p in enumerate(numbers):
            k = key_numbers[i % len(key_numbers)]
            c = (p + k + i) % 26
            result.append(c)

        return self._numbers_to_text(result)

    def layer1_dkss_decrypt(self, ciphertext: str, key1: str) -> str:
        """
        Inverse of Layer-1: Dynamic Key-Shift Substitution (DKSS)
        Formula: Pᵢ = (Cᵢ - K₁[i mod |K₁|] - i) mod 26
        """
        numbers = self._text_to_numbers(ciphertext)
        key_numbers = self._text_to_numbers(key1)

        result = []
        for i, c in enumerate(numbers):
            k = key_numbers[i % len(key_numbers)]
            p = (c - k - i) % 26
            result.append(p)

        return self._numbers_to_text(result)

    # Layer 2: Non-Linear Relational Pair Encoding (NRPE)
    def layer2_nrpe_encrypt(self, text: str, key2: str) -> str:
        """
        Layer-2: Non-Linear Relational Pair Encoding (NRPE)
        Process characters in pairs
        Formula: C₁ = (a + 2b) mod 26, C₂ = |a - b|
        Purpose: destroy linguistic structure
        """
        numbers = self._text_to_numbers(text)
        numbers = self._pad_to_even(numbers)  # Ensure even length

        # Use key2 to potentially modify the transformation
        key_numbers = self._text_to_numbers(key2) if key2 else []

        result = []
        for i in range(0, len(numbers), 2):
            a = numbers[i]
            b = numbers[i + 1]

            c1 = (a + 2 * b) % 26
            c2 = abs(a - b) % 26

            # Optionally apply key2 transformation
            if key_numbers:
                c1 = (c1 + key_numbers[i % len(key_numbers)]) % 26
                c2 = (c2 + key_numbers[(i + 1) % len(key_numbers)]) % 26

            result.extend([c1, c2])

        return self._numbers_to_text(result)

    def layer2_nrpe_decrypt(self, text: str, key2: str) -> str:
        """
        Inverse of Layer-2: Non-Linear Relational Pair Encoding (NRPE)
        From C₁ = (a + 2b) mod 26 and C₂ = |a - b|, we need to solve for a and b
        """
        numbers = self._text_to_numbers(text)

        # Reverse any key2 transformation first
        key_numbers = self._text_to_numbers(key2) if key2 else []
        if key_numbers:
            for i in range(len(numbers)):
                numbers[i] = (numbers[i] - key_numbers[i % len(key_numbers)]) % 26

        result = []
        for i in range(0, len(numbers), 2):
            c1 = numbers[i]
            c2 = numbers[i + 1]

            # We have:
            # c1 = (a + 2b) mod 26
            # c2 = |a - b|
            #
            # Case 1: a >= b, so c2 = (a - b) mod 26
            # From c2 = a - b => a = c2 + b
            # Substitute into c1 = a + 2b => c1 = (c2 + b) + 2b = c2 + 3b
            # So 3b = c1 - c2 => b = (c1 - c2) * 3^(-1) mod 26
            # And a = c2 + b
            #
            # Case 2: a < b, so c2 = (b - a) mod 26
            # From c2 = b - a => b = c2 + a
            # Substitute into c1 = a + 2b => c1 = a + 2(c2 + a) = a + 2c2 + 2a = 3a + 2c2
            # So 3a = c1 - 2c2 => a = (c1 - 2c2) * 3^(-1) mod 26
            # And b = c2 + a

            # Calculate modular inverse of 3 mod 26
            try:
                inv_3 = pow(3, -1, 26)

                # Try case 1: a >= b
                b1 = ((c1 - c2) * inv_3) % 26
                a1 = (c2 + b1) % 26
                if a1 >= b1 and (a1 + 2 * b1) % 26 == c1 and abs(a1 - b1) % 26 == c2:
                    result.extend([a1, b1])
                    continue

                # Try case 2: a < b
                a2 = ((c1 - 2 * c2) * inv_3) % 26
                b2 = (c2 + a2) % 26
                if a2 < b2 and (a2 + 2 * b2) % 26 == c1 and abs(a2 - b2) % 26 == c2:
                    result.extend([a2, b2])
                    continue

                # If neither case works, try other possibilities
                # Brute force approach for this non-linear system
                found = False
                for a in range(26):
                    for b in range(26):
                        if (a + 2 * b) % 26 == c1 and abs(a - b) % 26 == c2:
                            result.extend([a, b])
                            found = True
                            break
                    if found:
                        break
                if not found:
                    # If no solution found, add original values (degradation)
                    result.extend([c1, c2])

            except ValueError:
                # 3 has no inverse mod 26 in this case, use brute force
                found = False
                for a in range(26):
                    for b in range(26):
                        if (a + 2 * b) % 26 == c1 and abs(a - b) % 26 == c2:
                            result.extend([a, b])
                            found = True
                            break
                    if found:
                        break
                if not found:
                    # If no solution found, add original values (degradation)
                    result.extend([c1, c2])

        return self._numbers_to_text(result)

    # Layer 3: Variable Block Matrix Diffusion (VBMD)
    def layer3_vbmd_encrypt(self, text: str, key3: str) -> str:
        """
        Layer-3: Variable Block Matrix Diffusion (VBMD)
        Block sizes: 2x2, 3x3, or 4x4
        Formula: C = K₃ × P (mod 26)
        Matrix must be invertible (for decryption)
        Purpose: diffusion & avalanche effect
        """
        numbers = self._text_to_numbers(text)

        # Determine block size based on key length
        key_numbers = self._text_to_numbers(key3)
        block_size = 2 if len(key_numbers) < 10 else (3 if len(key_numbers) < 20 else 4)

        # Pad the text to make it divisible by block_size
        while len(numbers) % block_size != 0:
            numbers.append(0)  # Pad with 'A'

        result = []

        # Create matrix from key
        if block_size == 2:
            matrix = self._create_matrix_2x2(key_numbers)
        elif block_size == 3:
            matrix = self._create_matrix_3x3(key_numbers)
        else:  # block_size == 4
            matrix = self._create_matrix_4x4(key_numbers)

        # Process in blocks
        for i in range(0, len(numbers), block_size):
            block = np.array(numbers[i:i+block_size])
            block = block.reshape(-1, 1)  # Column vector

            # Multiply matrix by block
            encrypted_block = (matrix @ block) % 26
            encrypted_block = encrypted_block.flatten().tolist()

            result.extend(encrypted_block)

        return self._numbers_to_text(result)

    def layer3_vbmd_decrypt(self, text: str, key3: str) -> str:
        """
        Inverse of Layer-3: Variable Block Matrix Diffusion (VBMD)
        Formula: P = K₃^(-1) × C (mod 26)
        """
        numbers = self._text_to_numbers(text)

        # Determine block size based on key length
        key_numbers = self._text_to_numbers(key3)
        block_size = 2 if len(key_numbers) < 10 else (3 if len(key_numbers) < 20 else 4)

        # Create matrix from key and its inverse
        if block_size == 2:
            matrix = self._create_matrix_2x2(key_numbers)
        elif block_size == 3:
            matrix = self._create_matrix_3x3(key_numbers)
        else:  # block_size == 4
            matrix = self._create_matrix_4x4(key_numbers)

        # Get inverse matrix
        try:
            inv_matrix = self._get_matrix_inverse(matrix)
        except ValueError:
            # If matrix is not invertible, use original values
            return self._numbers_to_text(numbers)

        result = []

        # Process in blocks
        for i in range(0, len(numbers), block_size):
            block = np.array(numbers[i:i+block_size])
            block = block.reshape(-1, 1)  # Column vector

            # Multiply inverse matrix by block
            decrypted_block = (inv_matrix @ block) % 26
            decrypted_block = decrypted_block.flatten().tolist()

            result.extend(decrypted_block)

        return self._numbers_to_text(result)

    def _create_matrix_2x2(self, key_numbers: List[int]) -> np.ndarray:
        """Create a 2x2 invertible matrix from key numbers"""
        # Use first 4 key numbers to create 2x2 matrix
        if len(key_numbers) < 4:
            # Pad with repeated values if needed
            padded = key_numbers[:]
            while len(padded) < 4:
                padded.extend(key_numbers)
            padded = padded[:4]
        else:
            padded = key_numbers[:4]

        matrix = np.array([
            [padded[0], padded[1]],
            [padded[2], padded[3]]
        ])

        # Ensure the matrix is invertible (determinant is coprime with 26)
        det = int(np.round(np.linalg.det(matrix))) % 26
        if math.gcd(det, 26) != 1:
            # Adjust matrix to make it invertible
            matrix[0, 0] = (matrix[0, 0] + 1) % 26
            det = int(np.round(np.linalg.det(matrix))) % 26
            if math.gcd(det, 26) != 1:
                matrix[0, 1] = (matrix[0, 1] + 1) % 26
                det = int(np.round(np.linalg.det(matrix))) % 26
                if math.gcd(det, 26) != 1:
                    # If still not invertible, use a default invertible matrix
                    matrix = np.array([[1, 2], [3, 7]])  # det = 1, invertible

        return matrix

    def _create_matrix_3x3(self, key_numbers: List[int]) -> np.ndarray:
        """Create a 3x3 invertible matrix from key numbers"""
        # Use first 9 key numbers to create 3x3 matrix
        if len(key_numbers) < 9:
            # Pad with repeated values if needed
            padded = key_numbers[:]
            while len(padded) < 9:
                padded.extend(key_numbers)
            padded = padded[:9]
        else:
            padded = key_numbers[:9]

        matrix = np.array([
            [padded[0], padded[1], padded[2]],
            [padded[3], padded[4], padded[5]],
            [padded[6], padded[7], padded[8]]
        ])

        # Ensure the matrix is invertible (determinant is coprime with 26)
        det = int(np.round(np.linalg.det(matrix))) % 26
        if math.gcd(det, 26) != 1:
            # Adjust matrix to make it invertible
            matrix[0, 0] = (matrix[0, 0] + 1) % 26
            det = int(np.round(np.linalg.det(matrix))) % 26
            if math.gcd(det, 26) != 1:
                matrix[0, 1] = (matrix[0, 1] + 1) % 26
                det = int(np.round(np.linalg.det(matrix))) % 26
                if math.gcd(det, 26) != 1:
                    # If still not invertible, use a default invertible matrix
                    matrix = np.array([[1, 2, 3], [0, 1, 4], [5, 6, 0]])  # Custom invertible matrix

        return matrix

    def _create_matrix_4x4(self, key_numbers: List[int]) -> np.ndarray:
        """Create a 4x4 invertible matrix from key numbers"""
        # Use first 16 key numbers to create 4x4 matrix
        if len(key_numbers) < 16:
            # Pad with repeated values if needed
            padded = key_numbers[:]
            while len(padded) < 16:
                padded.extend(key_numbers)
            padded = padded[:16]
        else:
            padded = key_numbers[:16]

        matrix = np.array([
            [padded[0], padded[1], padded[2], padded[3]],
            [padded[4], padded[5], padded[6], padded[7]],
            [padded[8], padded[9], padded[10], padded[11]],
            [padded[12], padded[13], padded[14], padded[15]]
        ])

        # Ensure the matrix is invertible (determinant is coprime with 26)
        det = int(np.round(np.linalg.det(matrix))) % 26
        if math.gcd(det, 26) != 1:
            # Adjust matrix to make it invertible
            matrix[0, 0] = (matrix[0, 0] + 1) % 26
            det = int(np.round(np.linalg.det(matrix))) % 26
            if math.gcd(det, 26) != 1:
                matrix[0, 1] = (matrix[0, 1] + 1) % 26
                det = int(np.round(np.linalg.det(matrix))) % 26
                if math.gcd(det, 26) != 1:
                    # If still not invertible, use a default invertible matrix
                    matrix = np.array([
                        [1, 2, 3, 4],
                        [0, 1, 2, 3],
                        [0, 0, 1, 2],
                        [0, 0, 0, 1]
                    ])  # Identity-like matrix which is invertible

        return matrix

    # Layer 4: Key-Driven Positional Permutation (KDPP)
    def layer4_kdpp_encrypt(self, text: str, key4: str) -> str:
        """
        Layer-4: Key-Driven Positional Permutation (KDPP)
        Permute final ciphertext positions using key K₄
        Purpose: hide sequence & order
        """
        if not text:
            return text

        # Create permutation based on key
        key_numbers = self._text_to_numbers(key4)
        n = len(text)

        # Generate a permutation sequence based on the key
        permutation = list(range(n))

        # Use key to shuffle the permutation
        for i in range(n):
            j = (i + key_numbers[i % len(key_numbers)]) % n
            permutation[i], permutation[j] = permutation[j], permutation[i]

        # Apply permutation to text
        result = [''] * n
        for i in range(n):
            result[permutation[i]] = text[i]

        return ''.join(result)

    def layer4_kdpp_decrypt(self, text: str, key4: str) -> str:
        """
        Inverse of Layer-4: Key-Driven Positional Permutation (KDPP)
        """
        if not text:
            return text

        # Create permutation based on key (same as encryption)
        key_numbers = self._text_to_numbers(key4)
        n = len(text)

        # Generate the same permutation sequence based on the key
        permutation = list(range(n))

        # Use key to shuffle the permutation (same as encryption)
        for i in range(n):
            j = (i + key_numbers[i % len(key_numbers)]) % n
            permutation[i], permutation[j] = permutation[j], permutation[i]

        # Apply inverse permutation to text
        result = [''] * n
        for i in range(n):
            result[i] = text[permutation[i]]

        return ''.join(result)

    # Main encryption function
    def encrypt(self, plaintext: str, key1: str, key2: str, key3: str, key4: str) -> str:
        """
        Encrypt plaintext using all four layers of AQIMC
        """
        # Layer 1: DKSS
        layer1_result = self.layer1_dkss_encrypt(plaintext, key1)

        # Layer 2: NRPE
        layer2_result = self.layer2_nrpe_encrypt(layer1_result, key2)

        # Layer 3: VBMD
        layer3_result = self.layer3_vbmd_encrypt(layer2_result, key3)

        # Layer 4: KDPP
        final_result = self.layer4_kdpp_encrypt(layer3_result, key4)

        return final_result

    # Main decryption function
    def decrypt(self, ciphertext: str, key1: str, key2: str, key3: str, key4: str) -> str:
        """
        Decrypt ciphertext using inverse of all four layers of AQIMC
        """
        # Inverse Layer 4: KDPP
        layer3_result = self.layer4_kdpp_decrypt(ciphertext, key4)

        # Inverse Layer 3: VBMD
        layer2_result = self.layer3_vbmd_decrypt(layer3_result, key3)

        # Inverse Layer 2: NRPE
        layer1_result = self.layer2_nrpe_decrypt(layer2_result, key2)

        # Inverse Layer 1: DKSS
        original_text = self.layer1_dkss_decrypt(layer1_result, key1)

        return original_text


# Example usage and testing
if __name__ == "__main__":
    aqimc = AQIMC()

    # Test the algorithm
    plaintext = "HELLO"
    key1 = "KEY1"
    key2 = "KEY2"
    key3 = "MATRIXKEY"
    key4 = "PERMUTE"

    print(f"Original text: {plaintext}")

    # Encrypt
    encrypted = aqimc.encrypt(plaintext, key1, key2, key3, key4)
    print(f"Encrypted text: {encrypted}")

    # Decrypt
    decrypted = aqimc.decrypt(encrypted, key1, key2, key3, key4)
    print(f"Decrypted text: {decrypted}")

    # Verify
    print(f"Encryption/Decryption successful: {plaintext.upper() == decrypted}")