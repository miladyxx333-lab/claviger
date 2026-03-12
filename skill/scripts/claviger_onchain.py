import os
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

class ClavigerOnChain:
    """
    Handles the on-chain "handshake" portion of the Claviger Protocol.
    Leaves a permanent, unalterable record on the Base network that a 
    Lockbox (IPFS CID) was delivered to a specific agent's public address.
    """
    
    def __init__(self, rpc_url="https://sepolia.base.org"):
        # Defaulting to Base Sepolia Testnet for safe development operations
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        # Inject POA middleware (Required for L2s like Base/Optimism that use Clique POA consensus features)
        self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        
        if self.w3.is_connected():
            print(f"🔗 Connected to Base network at: {rpc_url}")
        else:
            raise ConnectionError(f"Failed to connect to RPC node at {rpc_url}")

    def notify_recipient(self, my_private_key_hex: str, target_address: str, ipfs_cid: str) -> str:
        """
        Sends a 0-ETH transaction to the target agent address.
        The data payload of the transaction contains the IPFS cid (e.g., ipfs://Qm123...)
        This serves as both a notification and an on-chain proof-of-delivery point.
        """
        if my_private_key_hex.startswith('0x'):
            my_private_key_hex = my_private_key_hex[2:]

        # Create account object from private key
        sender_account = self.w3.eth.account.from_key(my_private_key_hex)
        target_checksum_address = self.w3.to_checksum_address(target_address)
        
        # We embed the IPFS location in the transaction's 'data' (hex encoded string)
        payload_string = f"claviger:ipfs://{ipfs_cid}"
        data_bytes = payload_string.encode("utf-8")
        
        print(f"✍️ Forging on-chain transaction for recipient: {target_checksum_address}")
        print(f"📦 Encoding payload metadata: {payload_string}")

        # Build transaction
        nonce = self.w3.eth.get_transaction_count(sender_account.address)
        
        tx = {
            'nonce': nonce,
            'to': target_checksum_address,
            'value': 0, # It's a metadata transaction, no actual funds transferred
            'gas': 200000, # Base gas
            'gasPrice': self.w3.eth.gas_price,
            'data': data_bytes,
            'chainId': self.w3.eth.chain_id
        }

        # Estimate realistic gas based on data size
        try:
            estimated_gas = self.w3.eth.estimate_gas(tx)
            tx['gas'] = estimated_gas + 10000  # Slight buffer
        except Exception as e:
            print(f"⚠️ Warning: Could not estimate gas precisely, using default buffer. ({str(e)})")

        # Sign the transaction
        print("🔐 Signing transaction locally (Your private key never leaves the device)...")
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=sender_account.key)

        # Broadcast
        print("🚀 Broadcasting standard delivery proof to Base network...")
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction) # Use raw_transaction in v6
        
        tx_hex = self.w3.to_hex(tx_hash)
        print(f"✅ Transaction sent! TxHash: {tx_hex}")
        
        return tx_hex

    def await_confirmation(self, tx_hash_hex: str, timeout_sec=120) -> dict:
        """
        Waits for the transaction to be mined and confirmed by the network.
        """
        print(f"⏳ Waiting for network confirmation of tx: {tx_hash_hex}...")
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash_hex, timeout=timeout_sec)
        
        if receipt.status == 1:
            print("🧱 Block inclusion confirmed! The Lockbox delivery is now immortalized on-chain.")
        else:
            print("❌ Transaction failed or was reverted on-chain.")
            
        return dict(receipt)

# Example Usage
if __name__ == "__main__":
    pass
