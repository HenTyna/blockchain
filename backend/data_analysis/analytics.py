"""
Blockchain Analytics Module
Provides comprehensive analysis tools for blockchain data including:
- Transaction pattern analysis
- Network metrics
- Address activity analysis
- Performance metrics
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


class BlockchainAnalytics:
    """Analytics class for blockchain data analysis"""
    
    def __init__(self, blockchain):
        self.blockchain = blockchain
    
    def analyze_transaction_patterns(self) -> Dict[str, Any]:
        """Analyze transaction patterns in the blockchain"""
        try:
            # Extract all transactions
            all_transactions = []
            for block in self.blockchain.chain:
                for tx in block.transactions:
                    all_transactions.append({
                        'block_index': block.index,
                        'timestamp': tx.timestamp,
                        'sender': tx.sender,
                        'recipient': tx.recipient,
                        'amount': tx.amount,
                        'transaction_id': tx.transaction_id
                    })
            
            if not all_transactions:
                return {"message": "No transactions found"}
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(all_transactions)
            
            # Basic statistics
            total_transactions = len(df)
            total_volume = df['amount'].sum()
            avg_transaction_amount = df['amount'].mean()
            median_transaction_amount = df['amount'].median()
            
            # Transaction frequency over time
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
            df['date'] = df['datetime'].dt.date
            
            daily_transactions = df.groupby('date').size().to_dict()
            daily_volume = df.groupby('date')['amount'].sum().to_dict()
            
            # Top addresses by transaction count
            sender_counts = df['sender'].value_counts().head(10).to_dict()
            recipient_counts = df['recipient'].value_counts().head(10).to_dict()
            
            # Top addresses by volume
            sender_volume = df.groupby('sender')['amount'].sum().sort_values(ascending=False).head(10).to_dict()
            recipient_volume = df.groupby('recipient')['amount'].sum().sort_values(ascending=False).head(10).to_dict()
            
            # Transaction size distribution
            amount_ranges = [
                (0, 10, '0-10'),
                (10, 50, '10-50'),
                (50, 100, '50-100'),
                (100, 500, '100-500'),
                (500, float('inf'), '500+')
            ]
            
            size_distribution = {}
            for min_val, max_val, label in amount_ranges:
                if max_val == float('inf'):
                    count = len(df[df['amount'] >= min_val])
                else:
                    count = len(df[(df['amount'] >= min_val) & (df['amount'] < max_val)])
                size_distribution[label] = count
            
            return {
                "total_transactions": total_transactions,
                "total_volume": total_volume,
                "average_transaction_amount": avg_transaction_amount,
                "median_transaction_amount": median_transaction_amount,
                "daily_transactions": daily_transactions,
                "daily_volume": daily_volume,
                "top_senders_by_count": sender_counts,
                "top_recipients_by_count": recipient_counts,
                "top_senders_by_volume": sender_volume,
                "top_recipients_by_volume": recipient_volume,
                "transaction_size_distribution": size_distribution
            }
            
        except Exception as e:
            logger.error(f"Error analyzing transaction patterns: {e}")
            return {"error": str(e)}
    
    def get_network_metrics(self) -> Dict[str, Any]:
        """Get network performance metrics"""
        try:
            if len(self.blockchain.chain) < 2:
                return {"message": "Insufficient blocks for network analysis"}
            
            # Block time analysis
            block_times = []
            for i in range(1, len(self.blockchain.chain)):
                current_block = self.blockchain.chain[i]
                previous_block = self.blockchain.chain[i - 1]
                block_time = current_block.timestamp - previous_block.timestamp
                block_times.append(block_time)
            
            avg_block_time = np.mean(block_times)
            median_block_time = np.median(block_times)
            min_block_time = np.min(block_times)
            max_block_time = np.max(block_times)
            
            # Transactions per block
            transactions_per_block = [len(block.transactions) for block in self.blockchain.chain]
            avg_transactions_per_block = np.mean(transactions_per_block)
            max_transactions_per_block = np.max(transactions_per_block)
            
            # Mining difficulty analysis
            nonces = [block.nonce for block in self.blockchain.chain]
            avg_nonce = np.mean(nonces)
            total_nonce_attempts = sum(nonces)
            
            # Network throughput
            total_time = self.blockchain.chain[-1].timestamp - self.blockchain.chain[0].timestamp
            total_transactions = sum(len(block.transactions) for block in self.blockchain.chain)
            transactions_per_second = total_transactions / total_time if total_time > 0 else 0
            
            return {
                "block_time_analysis": {
                    "average_block_time": avg_block_time,
                    "median_block_time": median_block_time,
                    "minimum_block_time": min_block_time,
                    "maximum_block_time": max_block_time
                },
                "transactions_per_block": {
                    "average": avg_transactions_per_block,
                    "maximum": max_transactions_per_block,
                    "distribution": transactions_per_block
                },
                "mining_metrics": {
                    "average_nonce": avg_nonce,
                    "total_nonce_attempts": total_nonce_attempts,
                    "current_difficulty": self.blockchain.difficulty
                },
                "network_throughput": {
                    "transactions_per_second": transactions_per_second,
                    "total_transactions": total_transactions,
                    "total_time_seconds": total_time
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting network metrics: {e}")
            return {"error": str(e)}
    
    def analyze_address_activity(self) -> Dict[str, Any]:
        """Analyze address activity patterns"""
        try:
            # Extract all transactions
            all_transactions = []
            for block in self.blockchain.chain:
                for tx in block.transactions:
                    all_transactions.append({
                        'block_index': block.index,
                        'timestamp': tx.timestamp,
                        'sender': tx.sender,
                        'recipient': tx.recipient,
                        'amount': tx.amount
                    })
            
            if not all_transactions:
                return {"message": "No transactions found"}
            
            df = pd.DataFrame(all_transactions)
            
            # Get all unique addresses
            all_addresses = set(df['sender'].unique()) | set(df['recipient'].unique())
            
            # Address activity analysis
            address_stats = {}
            for address in all_addresses:
                sent_transactions = df[df['sender'] == address]
                received_transactions = df[df['recipient'] == address]
                
                total_sent = len(sent_transactions)
                total_received = len(received_transactions)
                total_sent_amount = sent_transactions['amount'].sum()
                total_received_amount = received_transactions['amount'].sum()
                
                # Calculate net flow
                net_amount = total_received_amount - total_sent_amount
                
                # Get first and last activity
                all_address_txs = df[(df['sender'] == address) | (df['recipient'] == address)]
                if not all_address_txs.empty:
                    first_activity = all_address_txs['timestamp'].min()
                    last_activity = all_address_txs['timestamp'].max()
                    activity_duration = last_activity - first_activity
                else:
                    first_activity = last_activity = activity_duration = 0
                
                address_stats[address] = {
                    "total_sent_transactions": total_sent,
                    "total_received_transactions": total_received,
                    "total_sent_amount": total_sent_amount,
                    "total_received_amount": total_received_amount,
                    "net_amount": net_amount,
                    "first_activity": first_activity,
                    "last_activity": last_activity,
                    "activity_duration": activity_duration,
                    "total_transactions": total_sent + total_received
                }
            
            # Most active addresses
            most_active = sorted(
                address_stats.items(),
                key=lambda x: x[1]['total_transactions'],
                reverse=True
            )[:10]
            
            # Addresses with highest volume
            highest_volume = sorted(
                address_stats.items(),
                key=lambda x: x[1]['total_sent_amount'] + x[1]['total_received_amount'],
                reverse=True
            )[:10]
            
            # Address types (senders vs receivers)
            sender_addresses = [addr for addr, stats in address_stats.items() if stats['total_sent_transactions'] > 0]
            receiver_addresses = [addr for addr, stats in address_stats.items() if stats['total_received_transactions'] > 0]
            both_addresses = [addr for addr, stats in address_stats.items() 
                            if stats['total_sent_transactions'] > 0 and stats['total_received_transactions'] > 0]
            
            return {
                "total_unique_addresses": len(all_addresses),
                "most_active_addresses": dict(most_active),
                "highest_volume_addresses": dict(highest_volume),
                "address_types": {
                    "sender_only": len([addr for addr in sender_addresses if addr not in receiver_addresses]),
                    "receiver_only": len([addr for addr in receiver_addresses if addr not in sender_addresses]),
                    "both_sender_and_receiver": len(both_addresses)
                },
                "all_address_stats": address_stats
            }
            
        except Exception as e:
            logger.error(f"Error analyzing address activity: {e}")
            return {"error": str(e)}
    
    def get_blockchain_health_metrics(self) -> Dict[str, Any]:
        """Get blockchain health and security metrics"""
        try:
            # Chain validation
            is_valid = self.blockchain.is_chain_valid()
            
            # Block integrity check
            integrity_issues = []
            for i, block in enumerate(self.blockchain.chain):
                calculated_hash = block.calculate_hash()
                if calculated_hash != block.hash:
                    integrity_issues.append(f"Block {i}: Hash mismatch")
            
            # Transaction integrity check
            transaction_issues = []
            for i, block in enumerate(self.blockchain.chain):
                for j, tx in enumerate(block.transactions):
                    calculated_tx_hash = tx.calculate_hash()
                    if calculated_tx_hash != tx.transaction_id:
                        transaction_issues.append(f"Block {i}, Transaction {j}: Hash mismatch")
            
            # Chain length and growth
            chain_length = len(self.blockchain.chain)
            if chain_length > 1:
                growth_rate = (chain_length - 1) / (self.blockchain.chain[-1].timestamp - self.blockchain.chain[0].timestamp)
            else:
                growth_rate = 0
            
            # Pending transactions
            pending_count = len(self.blockchain.pending_transactions)
            
            return {
                "chain_valid": is_valid,
                "integrity_issues": integrity_issues,
                "transaction_issues": transaction_issues,
                "chain_length": chain_length,
                "growth_rate_blocks_per_second": growth_rate,
                "pending_transactions": pending_count,
                "health_score": self._calculate_health_score(is_valid, integrity_issues, transaction_issues)
            }
            
        except Exception as e:
            logger.error(f"Error getting blockchain health metrics: {e}")
            return {"error": str(e)}
    
    def _calculate_health_score(self, is_valid: bool, integrity_issues: List[str], transaction_issues: List[str]) -> float:
        """Calculate a health score for the blockchain"""
        score = 100.0
        
        if not is_valid:
            score -= 50
        
        score -= len(integrity_issues) * 10
        score -= len(transaction_issues) * 5
        
        return max(0.0, score)
    
    def export_analytics_data(self, format: str = "json") -> str:
        """Export analytics data in specified format"""
        try:
            data = {
                "transaction_patterns": self.analyze_transaction_patterns(),
                "network_metrics": self.get_network_metrics(),
                "address_activity": self.analyze_address_activity(),
                "health_metrics": self.get_blockchain_health_metrics(),
                "export_timestamp": datetime.now().isoformat()
            }
            
            if format.lower() == "json":
                return json.dumps(data, indent=2, default=str)
            elif format.lower() == "csv":
                # Convert to CSV format (simplified)
                return "CSV export not implemented yet"
            else:
                return json.dumps(data, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Error exporting analytics data: {e}")
            return json.dumps({"error": str(e)})
