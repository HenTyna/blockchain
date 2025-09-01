import React, { useState } from 'react';
import { Search, ChevronDown, ChevronUp, Hash, Clock, Users } from 'lucide-react';

interface BlockExplorerProps {
  blockchain: any;
}

const BlockExplorer: React.FC<BlockExplorerProps> = ({ blockchain }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedBlocks, setExpandedBlocks] = useState<Set<number>>(new Set());

  const toggleBlockExpansion = (blockIndex: number) => {
    const newExpanded = new Set(expandedBlocks);
    if (newExpanded.has(blockIndex)) {
      newExpanded.delete(blockIndex);
    } else {
      newExpanded.add(blockIndex);
    }
    setExpandedBlocks(newExpanded);
  };

  const filteredBlocks = blockchain?.chain?.filter((block: any) => {
    if (!searchTerm) return true;
    
    const searchLower = searchTerm.toLowerCase();
    return (
      block.index.toString().includes(searchLower) ||
      block.hash.toLowerCase().includes(searchLower) ||
      block.transactions.some((tx: any) => 
        tx.sender.toLowerCase().includes(searchLower) ||
        tx.recipient.toLowerCase().includes(searchLower)
      )
    );
  }) || [];

  const formatHash = (hash: string) => {
    return `${hash.substring(0, 8)}...${hash.substring(hash.length - 8)}`;
  };

  const formatTimestamp = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString();
  };

  return (
    <div className="space-y-6">
      {/* Search Bar */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center">
          <Search className="h-5 w-5 text-gray-400 mr-3" />
          <input
            type="text"
            placeholder="Search by block index, hash, or address..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 border-0 focus:ring-0 text-lg"
          />
        </div>
      </div>

      {/* Blocks List */}
      <div className="space-y-4">
        {filteredBlocks.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <p className="text-gray-500">No blocks found</p>
          </div>
        ) : (
          filteredBlocks.map((block: any) => (
            <div key={block.index} className="bg-white rounded-lg shadow overflow-hidden">
              {/* Block Header */}
              <div 
                className="p-6 cursor-pointer hover:bg-gray-50 transition-colors"
                onClick={() => toggleBlockExpansion(block.index)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center">
                      <Hash className="h-5 w-5 text-blue-600 mr-2" />
                      <span className="font-semibold text-lg">Block #{block.index}</span>
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                      <Clock className="h-4 w-4 mr-1" />
                      {formatTimestamp(block.timestamp)}
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                      <Users className="h-4 w-4 mr-1" />
                      {block.transactions.length} transactions
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-500">
                      Nonce: {block.nonce}
                    </span>
                    {expandedBlocks.has(block.index) ? (
                      <ChevronUp className="h-5 w-5 text-gray-400" />
                    ) : (
                      <ChevronDown className="h-5 w-5 text-gray-400" />
                    )}
                  </div>
                </div>
                
                {/* Block Hash */}
                <div className="mt-3">
                  <p className="text-sm text-gray-600">
                    Hash: <span className="font-mono text-gray-900">{formatHash(block.hash)}</span>
                  </p>
                  <p className="text-sm text-gray-600">
                    Previous Hash: <span className="font-mono text-gray-900">{formatHash(block.previous_hash)}</span>
                  </p>
                </div>
              </div>

              {/* Block Details (Expandable) */}
              {expandedBlocks.has(block.index) && (
                <div className="border-t border-gray-200 bg-gray-50">
                  <div className="p-6">
                    <h4 className="font-semibold text-gray-900 mb-4">Transactions</h4>
                    {block.transactions.length === 0 ? (
                      <p className="text-gray-500">No transactions in this block</p>
                    ) : (
                      <div className="space-y-3">
                        {block.transactions.map((tx: any, txIndex: number) => (
                          <div key={txIndex} className="bg-white rounded-lg p-4 border">
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center space-x-2">
                                <span className="text-sm font-medium text-gray-900">
                                  {tx.sender}
                                </span>
                                <span className="text-gray-400">→</span>
                                <span className="text-sm font-medium text-gray-900">
                                  {tx.recipient}
                                </span>
                              </div>
                              <span className="text-sm font-semibold text-green-600">
                                {tx.amount} COIN
                              </span>
                            </div>
                            <div className="text-xs text-gray-500">
                              <p>Transaction ID: {formatHash(tx.transaction_id)}</p>
                              <p>Timestamp: {formatTimestamp(tx.timestamp)}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Summary Stats */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Blockchain Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <p className="text-2xl font-bold text-blue-600">
              {blockchain?.chain?.length || 0}
            </p>
            <p className="text-sm text-gray-600">Total Blocks</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-green-600">
              {blockchain?.chain?.reduce((total: number, block: any) => 
                total + block.transactions.length, 0) || 0}
            </p>
            <p className="text-sm text-gray-600">Total Transactions</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-purple-600">
              {blockchain?.pending_transactions?.length || 0}
            </p>
            <p className="text-sm text-gray-600">Pending Transactions</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlockExplorer;
