import json
import requests
import os
from ecies import encrypt, decrypt
import binascii

class ClavigerBox:
    """
    ClavigerBox: The core primitive for agent-to-agent secret sharing.
    Allows packing arbitrary JSON secrets into an ECIES-encrypted payload
    and uploading it as a 'Lockbox' to IPFS.
    """
    
    def __init__(self, pinata_api_key=None, pinata_secret_key=None):
        # We use Pinata as the default IPFS gateway for pinning
        self.pinata_api_key = pinata_api_key or os.getenv("PINATA_API_KEY")
        self.pinata_secret_key = pinata_secret_key or os.getenv("PINATA_SECRET_KEY")
        self.pinata_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    def pack(self, secrets: dict, recipient_public_key_hex: str) -> bytes:
        """
        Takes a dictionary of secrets, converts to JSON, and encrypts it 
        using the recipient's Ethereum Public Key (ECIES).
        """
        # Ensure public key is in bytes
        if recipient_public_key_hex.startswith('0x'):
            recipient_public_key_hex = recipient_public_key_hex[2:]
            
        pub_key_bytes = binascii.unhexlify(recipient_public_key_hex)
        
        # Serialize secrets
        payload_str = json.dumps(secrets)
        payload_bytes = payload_str.encode('utf-8')
        
        # Encrypt
        print("🔒 Locking secrets with recipient's public key...")
        encrypted_bytes = encrypt(recipient_public_key_hex, payload_bytes)
        return encrypted_bytes

    def unpack(self, encrypted_bytes: bytes, my_private_key_hex: str) -> dict:
        """
        Decrypts a Lockbox payload using the agent's private key.
        """
        if my_private_key_hex.startswith('0x'):
            my_private_key_hex = my_private_key_hex[2:]
            
        print("🗝️ Unlocking box with private key...")
        decrypted_bytes = decrypt(my_private_key_hex, encrypted_bytes)
        
        payload_str = decrypted_bytes.decode('utf-8')
        return json.loads(payload_str)

    def upload_to_ipfs(self, encrypted_bytes: bytes, filename="claviger_box.enc") -> str:
        """
        Uploads an encrypted Lockbox to IPFS via Pinata.
        Returns the IPFS CID (Content Identifier).
        """
        if not self.pinata_api_key:
            raise ValueError("Pinata API credentials missing. Set PINATA_API_KEY in env.")
            
        headers = {
            "pinata_api_key": self.pinata_api_key,
            "pinata_secret_api_key": self.pinata_secret_key
        }
        
        files = {
            'file': (filename, encrypted_bytes)
        }
        
        print("📤 Uploading Lockbox to IPFS...")
        response = requests.post(self.pinata_url, files=files, headers=headers)
        
        if response.status_code == 200:
            cid = response.json()['IpfsHash']
            print(f"✅ Box secured on IPFS: ipfs://{cid}")
            return cid
        else:
            raise Exception(f"Failed to upload to IPFS: {response.text}")

    def download_from_ipfs(self, cid: str, gateway="https://ipfs.io/ipfs/") -> bytes:
        """
        Retrieves a Lockbox from an IPFS gateway.
        """
        url = f"{gateway}{cid}"
        print(f"📥 Downloading Lockbox from {url}...")
        response = requests.get(url)
        
        if response.status_code == 200:
            print("✅ Box retrieved successfully.")
            return response.content
        else:
            raise Exception(f"Failed to download from IPFS: {response.text}")

# --- Example Usage ---
if __name__ == "__main__":
    print("📦 Claviger Box Protocol Initialized.")
    # In a real scenario, you would instantiate ClavigerBox, pack your secrets,
    # and upload them to IPFS. The resulting CID is then sent on-chain via Base.
