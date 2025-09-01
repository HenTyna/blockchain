import React from 'react';
import { 
  Database, 
  BarChart3, 
  Zap, 
  Users, 
  Clock,
  TrendingUp
} from 'lucide-react';

interface StatsData {
  total_blocks: number;
  total_transactions: number;
  difficulty: number;
  mining_reward: number;
  pending_transactions: number;
}

interface BlockchainStatsProps {
  stats: StatsData | undefined;
  loading: boolean;
}

const BlockchainStats: React.FC<BlockchainStatsProps> = ({ stats, loading }) => {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-8 bg-gray-200 rounded w-1/2"></div>
          </div>
        ))}
      </div>
    );
  }

  const statCards = [
    {
      title: 'Total Blocks',
      value: stats?.total_blocks || 0,
      icon: Database,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      description: 'Blocks in the chain'
    },
    {
      title: 'Total Transactions',
      value: stats?.total_transactions || 0,
      icon: BarChart3,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      description: 'Transactions processed'
    },
    {
      title: 'Mining Difficulty',
      value: stats?.difficulty || 0,
      icon: Zap,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      description: 'Current difficulty level'
    },
    {
      title: 'Pending Transactions',
      value: stats?.pending_transactions || 0,
      icon: Clock,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
      description: 'Awaiting confirmation'
    }
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center">
                <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
              <p className="mt-2 text-xs text-gray-500">{stat.description}</p>
            </div>
          );
        })}
      </div>

      {/* Additional Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Mining Reward</h3>
            <TrendingUp className="h-5 w-5 text-green-600" />
          </div>
          <div className="text-3xl font-bold text-green-600">
            {stats?.mining_reward || 0} COIN
          </div>
          <p className="text-sm text-gray-600 mt-2">
            Reward for successfully mining a block
          </p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Network Status</h3>
            <div className="flex items-center">
              <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
              <span className="text-sm text-green-600">Active</span>
            </div>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Chain Length:</span>
              <span className="text-sm font-medium">{stats?.total_blocks || 0}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Transaction Volume:</span>
              <span className="text-sm font-medium">{stats?.total_transactions || 0}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Pending Queue:</span>
              <span className="text-sm font-medium">{stats?.pending_transactions || 0}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlockchainStats;
