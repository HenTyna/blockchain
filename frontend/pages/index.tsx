import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { 
  Activity, 
  BarChart3, 
  Shield, 
  Code, 
  Database, 
  TrendingUp,
  Users,
  Zap,
  Globe,
  Lock
} from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

// Components
import BlockchainStats from '../components/BlockchainStats';
import TransactionForm from '../components/TransactionForm';
import BlockExplorer from '../components/BlockExplorer';
import AnalyticsChart from '../components/AnalyticsChart';
import SmartContractAnalyzer from '../components/SmartContractAnalyzer';

// Types
interface BlockchainData {
  chain: any[];
  pending_transactions: any[];
  difficulty: number;
  mining_reward: number;
}

interface StatsData {
  total_blocks: number;
  total_transactions: number;
  difficulty: number;
  mining_reward: number;
  pending_transactions: number;
}

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview');

  // Fetch blockchain data
  const { data: blockchainData, isLoading: blockchainLoading } = useQuery({
    queryKey: ['blockchain'],
    queryFn: async () => {
      const response = await axios.get('/api/blockchain');
      return response.data;
    },
    refetchInterval: 5000, // Refresh every 5 seconds
  });

  // Fetch blockchain stats
  const { data: statsData, isLoading: statsLoading } = useQuery({
    queryKey: ['blockchain-stats'],
    queryFn: async () => {
      const response = await axios.get('/api/blockchain/stats');
      return response.data;
    },
    refetchInterval: 5000,
  });

  const tabs = [
    { id: 'overview', name: 'Overview', icon: Activity },
    { id: 'transactions', name: 'Transactions', icon: BarChart3 },
    { id: 'blocks', name: 'Block Explorer', icon: Database },
    { id: 'analytics', name: 'Analytics', icon: TrendingUp },
    { id: 'smart-contracts', name: 'Smart Contracts', icon: Code },
    { id: 'security', name: 'Security', icon: Shield },
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <div className="space-y-6">
            <BlockchainStats stats={statsData} loading={statsLoading} />
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <AnalyticsChart />
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
                <div className="space-y-3">
                  {blockchainData?.chain?.slice(-5).reverse().map((block: any, index: number) => (
                    <div key={block.index} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                      <div>
                        <p className="font-medium">Block #{block.index}</p>
                        <p className="text-sm text-gray-600">
                          {block.transactions.length} transactions
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-600">
                          {new Date(block.timestamp * 1000).toLocaleTimeString()}
                        </p>
                        <p className="text-xs text-gray-500">
                          Hash: {block.hash.substring(0, 8)}...
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        );
      
      case 'transactions':
        return (
          <div className="space-y-6">
            <TransactionForm />
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4">Pending Transactions</h3>
              {blockchainData?.pending_transactions?.length > 0 ? (
                <div className="space-y-3">
                  {blockchainData.pending_transactions.map((tx: any, index: number) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                      <div>
                        <p className="font-medium">{tx.sender} → {tx.recipient}</p>
                        <p className="text-sm text-gray-600">Amount: {tx.amount}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-xs text-gray-500">
                          {new Date(tx.timestamp * 1000).toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No pending transactions</p>
              )}
            </div>
          </div>
        );
      
      case 'blocks':
        return <BlockExplorer blockchain={blockchainData} />;
      
      case 'analytics':
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold mb-4">Transaction Patterns</h3>
                <AnalyticsChart type="transactions" />
              </div>
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold mb-4">Network Metrics</h3>
                <AnalyticsChart type="network" />
              </div>
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold mb-4">Address Activity</h3>
                <AnalyticsChart type="addresses" />
              </div>
            </div>
          </div>
        );
      
      case 'smart-contracts':
        return <SmartContractAnalyzer />;
      
      case 'security':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4">Security Overview</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="p-4 bg-green-50 rounded-lg">
                  <div className="flex items-center">
                    <Shield className="h-8 w-8 text-green-600" />
                    <div className="ml-3">
                      <p className="text-sm font-medium text-green-800">Chain Valid</p>
                      <p className="text-2xl font-bold text-green-900">
                        {blockchainData ? 'Yes' : 'No'}
                      </p>
                    </div>
                  </div>
                </div>
                <div className="p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-center">
                    <Lock className="h-8 w-8 text-blue-600" />
                    <div className="ml-3">
                      <p className="text-sm font-medium text-blue-800">Blocks</p>
                      <p className="text-2xl font-bold text-blue-900">
                        {statsData?.total_blocks || 0}
                      </p>
                    </div>
                  </div>
                </div>
                <div className="p-4 bg-purple-50 rounded-lg">
                  <div className="flex items-center">
                    <Zap className="h-8 w-8 text-purple-600" />
                    <div className="ml-3">
                      <p className="text-sm font-medium text-purple-800">Difficulty</p>
                      <p className="text-2xl font-bold text-purple-900">
                        {statsData?.difficulty || 0}
                      </p>
                    </div>
                  </div>
                </div>
                <div className="p-4 bg-orange-50 rounded-lg">
                  <div className="flex items-center">
                    <Users className="h-8 w-8 text-orange-600" />
                    <div className="ml-3">
                      <p className="text-sm font-medium text-orange-800">Transactions</p>
                      <p className="text-2xl font-bold text-orange-900">
                        {statsData?.total_transactions || 0}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <>
      <Head>
        <title>Blockchain Research Dashboard</title>
        <meta name="description" content="Comprehensive blockchain research and analysis platform" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div className="flex items-center">
                <Globe className="h-8 w-8 text-blue-600" />
                <h1 className="ml-3 text-2xl font-bold text-gray-900">
                  Blockchain Research
                </h1>
              </div>
              <div className="flex items-center space-x-4">
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                  <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
                  Connected
                </span>
              </div>
            </div>
          </div>
        </header>

        {/* Navigation Tabs */}
        <nav className="bg-white border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex space-x-8">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center py-4 px-1 border-b-2 font-medium text-sm ${
                      activeTab === tab.id
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <Icon className="h-5 w-5 mr-2" />
                    {tab.name}
                  </button>
                );
              })}
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            {renderTabContent()}
          </div>
        </main>
      </div>
    </>
  );
}
