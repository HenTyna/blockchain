import React from 'react';
import { TrendingUp, BarChart3, Activity } from 'lucide-react';

interface AnalyticsChartProps {
  type?: 'transactions' | 'network' | 'addresses';
}

const AnalyticsChart: React.FC<AnalyticsChartProps> = ({ type = 'transactions' }) => {
  const getChartData = () => {
    switch (type) {
      case 'transactions':
        return {
          title: 'Transaction Volume',
          icon: TrendingUp,
          data: [
            { label: 'Mon', value: 12 },
            { label: 'Tue', value: 19 },
            { label: 'Wed', value: 15 },
            { label: 'Thu', value: 25 },
            { label: 'Fri', value: 22 },
            { label: 'Sat', value: 18 },
            { label: 'Sun', value: 14 }
          ]
        };
      case 'network':
        return {
          title: 'Network Performance',
          icon: Activity,
          data: [
            { label: 'Block Time', value: 2.5 },
            { label: 'TPS', value: 15 },
            { label: 'Difficulty', value: 4 },
            { label: 'Pending', value: 8 }
          ]
        };
      case 'addresses':
        return {
          title: 'Address Activity',
          icon: BarChart3,
          data: [
            { label: 'Active', value: 45 },
            { label: 'Inactive', value: 12 },
            { label: 'New', value: 8 }
          ]
        };
      default:
        return {
          title: 'Analytics',
          icon: BarChart3,
          data: []
        };
    }
  };

  const chartData = getChartData();
  const Icon = chartData.icon;
  const maxValue = Math.max(...chartData.data.map(d => d.value));

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center mb-4">
        <Icon className="h-6 w-6 text-blue-600 mr-2" />
        <h3 className="text-lg font-semibold text-gray-900">{chartData.title}</h3>
      </div>
      
      <div className="space-y-3">
        {chartData.data.map((item, index) => (
          <div key={index} className="flex items-center">
            <div className="w-20 text-sm text-gray-600">{item.label}</div>
            <div className="flex-1 mx-4">
              <div className="bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${(item.value / maxValue) * 100}%` }}
                ></div>
              </div>
            </div>
            <div className="w-12 text-sm font-medium text-gray-900 text-right">
              {item.value}
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-sm text-gray-600">
          {type === 'transactions' && 'Daily transaction volume over the past week'}
          {type === 'network' && 'Current network performance metrics'}
          {type === 'addresses' && 'Address activity distribution'}
        </p>
      </div>
    </div>
  );
};

export default AnalyticsChart;
