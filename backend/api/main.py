"""
FastAPI Backend for Blockchain Research
Provides REST API endpoints for blockchain operations, data analysis, and research tools.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from blockchain_core.blockchain import Blockchain, Transaction, Block
from data_analysis.analytics import BlockchainAnalytics
from smart_contracts.contract_analyzer import ContractAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Blockchain Research API",
    description="A comprehensive API for blockchain research and analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize blockchain and analysis tools
blockchain = Blockchain(difficulty=2)
analytics = BlockchainAnalytics(blockchain)
contract_analyzer = ContractAnalyzer()

# Pydantic models for request/response
class TransactionRequest(BaseModel):
    sender: str
    recipient: str
    amount: float

class MiningRequest(BaseModel):
    miner_address: str

class BlockResponse(BaseModel):
    index: int
    timestamp: float
    transactions: List[Dict[str, Any]]
    previous_hash: str
    nonce: int
    hash: str

class BlockchainStats(BaseModel):
    total_blocks: int
    total_transactions: int
    difficulty: int
    mining_reward: float
    pending_transactions: int

class AddressBalance(BaseModel):
    address: str
    balance: float

# API Routes

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Blockchain Research API",
        "version": "1.0.0",
        "endpoints": {
            "blockchain": "/api/blockchain",
            "transactions": "/api/transactions",
            "mining": "/api/mining",
            "analytics": "/api/analytics",
            "smart_contracts": "/api/smart-contracts"
        }
    }

# Blockchain endpoints
@app.get("/api/blockchain", response_model=Dict[str, Any])
async def get_blockchain():
    """Get the entire blockchain"""
    try:
        return blockchain.to_dict()
    except Exception as e:
        logger.error(f"Error getting blockchain: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/blockchain/stats", response_model=BlockchainStats)
async def get_blockchain_stats():
    """Get blockchain statistics"""
    try:
        stats = blockchain.get_chain_stats()
        return BlockchainStats(**stats)
    except Exception as e:
        logger.error(f"Error getting blockchain stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/blockchain/validate")
async def validate_blockchain():
    """Validate the blockchain"""
    try:
        is_valid = blockchain.is_chain_valid()
        return {"valid": is_valid}
    except Exception as e:
        logger.error(f"Error validating blockchain: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/blockchain/blocks/{block_index}", response_model=BlockResponse)
async def get_block(block_index: int):
    """Get a specific block by index"""
    try:
        block = blockchain.get_block_by_index(block_index)
        if block is None:
            raise HTTPException(status_code=404, detail="Block not found")
        return BlockResponse(**block.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting block {block_index}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Transaction endpoints
@app.post("/api/transactions", response_model=Dict[str, str])
async def create_transaction(transaction: TransactionRequest):
    """Create a new transaction"""
    try:
        transaction_id = blockchain.add_transaction(
            sender=transaction.sender,
            recipient=transaction.recipient,
            amount=transaction.amount
        )
        return {"transaction_id": transaction_id, "message": "Transaction added to pending transactions"}
    except Exception as e:
        logger.error(f"Error creating transaction: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/transactions/pending")
async def get_pending_transactions():
    """Get all pending transactions"""
    try:
        return {
            "pending_transactions": [
                tx.to_dict() for tx in blockchain.pending_transactions
            ]
        }
    except Exception as e:
        logger.error(f"Error getting pending transactions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/transactions/{transaction_id}")
async def get_transaction(transaction_id: str):
    """Get a specific transaction by ID"""
    try:
        transaction = blockchain.get_transaction_by_id(transaction_id)
        if transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting transaction {transaction_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Mining endpoints
@app.post("/api/mining/mine", response_model=BlockResponse)
async def mine_block(request: MiningRequest, background_tasks: BackgroundTasks):
    """Mine a new block with pending transactions"""
    try:
        if not blockchain.pending_transactions:
            raise HTTPException(status_code=400, detail="No pending transactions to mine")
        
        # Mine block in background to avoid blocking
        def mine_block_task():
            return blockchain.mine_pending_transactions(request.miner_address)
        
        background_tasks.add_task(mine_block_task)
        
        # For now, return the latest block (will be updated after mining)
        latest_block = blockchain.get_latest_block()
        return BlockResponse(**latest_block.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error mining block: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/mining/status")
async def get_mining_status():
    """Get current mining status"""
    try:
        return {
            "pending_transactions": len(blockchain.pending_transactions),
            "difficulty": blockchain.difficulty,
            "mining_reward": blockchain.mining_reward
        }
    except Exception as e:
        logger.error(f"Error getting mining status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Address and balance endpoints
@app.get("/api/addresses/{address}/balance", response_model=AddressBalance)
async def get_address_balance(address: str):
    """Get balance for a specific address"""
    try:
        balance = blockchain.get_balance(address)
        return AddressBalance(address=address, balance=balance)
    except Exception as e:
        logger.error(f"Error getting balance for {address}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Analytics endpoints
@app.get("/api/analytics/transaction-patterns")
async def get_transaction_patterns():
    """Get transaction pattern analysis"""
    try:
        patterns = analytics.analyze_transaction_patterns()
        return patterns
    except Exception as e:
        logger.error(f"Error analyzing transaction patterns: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/analytics/network-metrics")
async def get_network_metrics():
    """Get network performance metrics"""
    try:
        metrics = analytics.get_network_metrics()
        return metrics
    except Exception as e:
        logger.error(f"Error getting network metrics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/analytics/address-activity")
async def get_address_activity():
    """Get address activity analysis"""
    try:
        activity = analytics.analyze_address_activity()
        return activity
    except Exception as e:
        logger.error(f"Error analyzing address activity: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Smart contract endpoints
@app.post("/api/smart-contracts/analyze")
async def analyze_smart_contract(contract_code: str):
    """Analyze a smart contract for security vulnerabilities"""
    try:
        analysis = contract_analyzer.analyze_contract(contract_code)
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing smart contract: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/smart-contracts/vulnerabilities")
async def get_common_vulnerabilities():
    """Get list of common smart contract vulnerabilities"""
    try:
        vulnerabilities = contract_analyzer.get_common_vulnerabilities()
        return vulnerabilities
    except Exception as e:
        logger.error(f"Error getting vulnerabilities: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "blockchain_valid": blockchain.is_chain_valid()}

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
