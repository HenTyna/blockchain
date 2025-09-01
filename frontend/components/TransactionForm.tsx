import React, { useState } from 'react';
import { Send, Loader2, CheckCircle } from 'lucide-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import toast from 'react-hot-toast';

interface TransactionFormProps {}

const TransactionForm: React.FC<TransactionFormProps> = () => {
  const [formData, setFormData] = useState({
    sender: '',
    recipient: '',
    amount: ''
  });

  const queryClient = useQueryClient();

  const createTransactionMutation = useMutation({
    mutationFn: async (data: { sender: string; recipient: string; amount: number }) => {
      const response = await axios.post('/api/transactions', data);
      return response.data;
    },
    onSuccess: (data) => {
      toast.success('Transaction created successfully!');
      setFormData({ sender: '', recipient: '', amount: '' });
      // Invalidate and refetch blockchain data
      queryClient.invalidateQueries({ queryKey: ['blockchain'] });
      queryClient.invalidateQueries({ queryKey: ['blockchain-stats'] });
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create transaction');
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.sender || !formData.recipient || !formData.amount) {
      toast.error('Please fill in all fields');
      return;
    }

    const amount = parseFloat(formData.amount);
    if (isNaN(amount) || amount <= 0) {
      toast.error('Please enter a valid amount');
      return;
    }

    createTransactionMutation.mutate({
      sender: formData.sender,
      recipient: formData.recipient,
      amount: amount
    });
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center mb-6">
        <Send className="h-6 w-6 text-blue-600 mr-2" />
        <h3 className="text-lg font-semibold text-gray-900">Create Transaction</h3>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="sender" className="block text-sm font-medium text-gray-700 mb-1">
            Sender Address
          </label>
          <input
            type="text"
            id="sender"
            name="sender"
            value={formData.sender}
            onChange={handleInputChange}
            placeholder="Enter sender address"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            disabled={createTransactionMutation.isPending}
          />
        </div>

        <div>
          <label htmlFor="recipient" className="block text-sm font-medium text-gray-700 mb-1">
            Recipient Address
          </label>
          <input
            type="text"
            id="recipient"
            name="recipient"
            value={formData.recipient}
            onChange={handleInputChange}
            placeholder="Enter recipient address"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            disabled={createTransactionMutation.isPending}
          />
        </div>

        <div>
          <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-1">
            Amount
          </label>
          <input
            type="number"
            id="amount"
            name="amount"
            value={formData.amount}
            onChange={handleInputChange}
            placeholder="Enter amount"
            step="0.01"
            min="0"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            disabled={createTransactionMutation.isPending}
          />
        </div>

        <button
          type="submit"
          disabled={createTransactionMutation.isPending}
          className="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {createTransactionMutation.isPending ? (
            <>
              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              Creating Transaction...
            </>
          ) : (
            <>
              <Send className="h-4 w-4 mr-2" />
              Create Transaction
            </>
          )}
        </button>
      </form>

      {/* Quick Actions */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h4 className="text-sm font-medium text-gray-900 mb-3">Quick Actions</h4>
        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={() => setFormData({
              sender: 'Alice',
              recipient: 'Bob',
              amount: '50'
            })}
            className="px-3 py-2 text-sm border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Alice → Bob (50)
          </button>
          <button
            onClick={() => setFormData({
              sender: 'Bob',
              recipient: 'Charlie',
              amount: '30'
            })}
            className="px-3 py-2 text-sm border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Bob → Charlie (30)
          </button>
        </div>
      </div>

      {/* Transaction Status */}
      {createTransactionMutation.isSuccess && (
        <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-md">
          <div className="flex items-center">
            <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
            <span className="text-sm text-green-800">
              Transaction created successfully! Transaction ID: {createTransactionMutation.data?.transaction_id?.substring(0, 8)}...
            </span>
          </div>
        </div>
      )}

      {createTransactionMutation.isError && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <div className="flex items-center">
            <span className="text-sm text-red-800">
              Error: {createTransactionMutation.error?.message || 'Failed to create transaction'}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default TransactionForm;
