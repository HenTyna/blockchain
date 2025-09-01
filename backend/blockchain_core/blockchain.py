"""
Basic Blockchain Implementation in Python
This module provides a simple blockchain implementation with:
- Block creation and validation
- Proof of Work consensus
- Transaction management
- Chain validation
"""

import hashlib
import json
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class Transaction:
    """Represents a transaction in the blockchain"""
    sender: str
    recipient: str
    amount: float
    timestamp: float
    transaction_id: str = None

    def __post_init__(self):
        if self.transaction_id is None:
            self.transaction_id = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calculate hash of the transaction"""
        transaction_string = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        return hashlib.sha256(transaction_string.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary"""
        return asdict(self)


@dataclass
class Block:
    """Represents a block in the blockchain"""
    index: int
    timestamp: float
    transactions: List[Transaction]
    previous_hash: str
    nonce: int = 0
    hash: str = None

    def __post_init__(self):
        if self.hash is None:
            self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calculate hash of the block"""
        block_string = (
            f"{self.index}{self.timestamp}{self.previous_hash}{self.nonce}"
            f"{json.dumps([tx.to_dict() for tx in self.transactions], sort_keys=True)}"
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        """Mine the block with proof of work"""
        target = "0" * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        logger.info(f"Block mined! Hash: {self.hash}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }


class Blockchain:
    """Main blockchain class"""
    
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = difficulty
        self.mining_reward = 10.0
        
        # Create genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """Create the first block in the chain"""
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0"
        )
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
        logger.info("Genesis block created")
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def add_transaction(self, sender: str, recipient: str, amount: float) -> str:
        """Add a new transaction to pending transactions"""
        transaction = Transaction(
            sender=sender,
            recipient=recipient,
            amount=amount,
            timestamp=time.time()
        )
        
        self.pending_transactions.append(transaction)
        logger.info(f"Transaction added: {transaction.transaction_id}")
        return transaction.transaction_id
    
    def mine_pending_transactions(self, miner_address: str) -> Block:
        """Mine pending transactions and create a new block"""
        # Create mining reward transaction
        reward_transaction = Transaction(
            sender="Blockchain",
            recipient=miner_address,
            amount=self.mining_reward,
            timestamp=time.time()
        )
        
        # Add reward transaction to pending transactions
        transactions_to_mine = self.pending_transactions + [reward_transaction]
        
        # Create new block
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=transactions_to_mine,
            previous_hash=self.get_latest_block().hash
        )
        
        # Mine the block
        block.mine_block(self.difficulty)
        
        # Add block to chain
        self.chain.append(block)
        
        # Reset pending transactions
        self.pending_transactions = []
        
        logger.info(f"Block {block.index} mined by {miner_address}")
        return block
    
    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                logger.error(f"Invalid hash in block {i}")
                return False
            
            # Check if previous hash is correct
            if current_block.previous_hash != previous_block.hash:
                logger.error(f"Invalid previous hash in block {i}")
                return False
        
        logger.info("Blockchain is valid")
        return True
    
    def get_balance(self, address: str) -> float:
        """Get balance of an address"""
        balance = 0.0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.recipient == address:
                    balance += transaction.amount
        
        return balance
    
    def get_block_by_index(self, index: int) -> Optional[Block]:
        """Get block by index"""
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None
    
    def get_transaction_by_id(self, transaction_id: str) -> Optional[Transaction]:
        """Get transaction by ID"""
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.transaction_id == transaction_id:
                    return transaction
        return None
    
    def get_chain_stats(self) -> Dict[str, Any]:
        """Get blockchain statistics"""
        total_transactions = sum(len(block.transactions) for block in self.chain)
        total_blocks = len(self.chain)
        
        return {
            "total_blocks": total_blocks,
            "total_transactions": total_transactions,
            "difficulty": self.difficulty,
            "mining_reward": self.mining_reward,
            "pending_transactions": len(self.pending_transactions)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert blockchain to dictionary"""
        return {
            "chain": [block.to_dict() for block in self.chain],
            "pending_transactions": [tx.to_dict() for tx in self.pending_transactions],
            "difficulty": self.difficulty,
            "mining_reward": self.mining_reward
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load blockchain from dictionary"""
        self.chain = []
        for block_data in data["chain"]:
            transactions = [
                Transaction(**tx_data) for tx_data in block_data["transactions"]
            ]
            block = Block(
                index=block_data["index"],
                timestamp=block_data["timestamp"],
                transactions=transactions,
                previous_hash=block_data["previous_hash"],
                nonce=block_data["nonce"],
                hash=block_data["hash"]
            )
            self.chain.append(block)
        
        self.pending_transactions = [
            Transaction(**tx_data) for tx_data in data["pending_transactions"]
        ]
        self.difficulty = data["difficulty"]
        self.mining_reward = data["mining_reward"]


# Example usage and testing
if __name__ == "__main__":
    # Create blockchain
    blockchain = Blockchain(difficulty=2)
    
    # Add some transactions
    blockchain.add_transaction("Alice", "Bob", 50)
    blockchain.add_transaction("Bob", "Charlie", 30)
    
    # Mine block
    blockchain.mine_pending_transactions("miner1")
    
    # Add more transactions
    blockchain.add_transaction("Charlie", "Alice", 20)
    blockchain.add_transaction("Alice", "David", 10)
    
    # Mine another block
    blockchain.mine_pending_transactions("miner2")
    
    # Print blockchain info
    print("Blockchain Stats:", blockchain.get_chain_stats())
    print("Alice's balance:", blockchain.get_balance("Alice"))
    print("Bob's balance:", blockchain.get_balance("Bob"))
    print("Is chain valid:", blockchain.is_chain_valid())
