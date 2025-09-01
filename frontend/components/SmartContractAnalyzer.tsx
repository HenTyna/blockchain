import React, { useState } from 'react';
import { Code, Shield, AlertTriangle, CheckCircle } from 'lucide-react';

const SmartContractAnalyzer: React.FC = () => {
  const [contractCode, setContractCode] = useState('');
  const [analysis, setAnalysis] = useState<any>(null);

  const sampleContract = `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleToken {
    mapping(address => uint256) public balances;
    
    function transfer(address to, uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
}`;

  const handleAnalyze = async () => {
    if (!contractCode.trim()) {
      alert('Please enter contract code to analyze');
      return;
    }

    try {
      const response = await fetch('/api/smart-contracts/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ contract_code: contractCode }),
      });
      
      const result = await response.json();
      setAnalysis(result);
    } catch (error) {
      console.error('Error analyzing contract:', error);
      // Mock analysis for demo
      setAnalysis({
        security_score: 85,
        gas_score: 90,
        overall_score: 87,
        vulnerabilities: [
          {
            type: 'access_control',
            severity: 'low',
            description: 'Public function without access control',
            line_number: 8,
            recommendation: 'Consider adding access control modifiers'
          }
        ],
        gas_optimization: [],
        best_practices: {
          security: [
            { practice: 'Use OpenZeppelin contracts', followed: false },
            { practice: 'Implement proper access control', followed: false }
          ]
        }
      });
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center mb-6">
          <Code className="h-6 w-6 text-blue-600 mr-2" />
          <h3 className="text-lg font-semibold text-gray-900">Smart Contract Analyzer</h3>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Code Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Contract Code (Solidity)
            </label>
            <textarea
              value={contractCode}
              onChange={(e) => setContractCode(e.target.value)}
              placeholder="Paste your Solidity contract code here..."
              className="w-full h-64 p-3 border border-gray-300 rounded-md font-mono text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <div className="mt-3 flex space-x-3">
              <button
                onClick={() => setContractCode(sampleContract)}
                className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50"
              >
                Load Sample
              </button>
              <button
                onClick={handleAnalyze}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Analyze Contract
              </button>
            </div>
          </div>

          {/* Analysis Results */}
          <div>
            <h4 className="text-md font-semibold text-gray-900 mb-4">Analysis Results</h4>
            
            {analysis ? (
              <div className="space-y-4">
                {/* Scores */}
                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center p-3 bg-green-50 rounded-lg">
                    <div className="text-2xl font-bold text-green-600">{analysis.security_score}</div>
                    <div className="text-sm text-green-800">Security</div>
                  </div>
                  <div className="text-center p-3 bg-blue-50 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">{analysis.gas_score}</div>
                    <div className="text-sm text-blue-800">Gas</div>
                  </div>
                  <div className="text-center p-3 bg-purple-50 rounded-lg">
                    <div className="text-2xl font-bold text-purple-600">{analysis.overall_score}</div>
                    <div className="text-sm text-purple-800">Overall</div>
                  </div>
                </div>

                {/* Vulnerabilities */}
                {analysis.vulnerabilities && analysis.vulnerabilities.length > 0 && (
                  <div>
                    <h5 className="font-medium text-gray-900 mb-2 flex items-center">
                      <AlertTriangle className="h-4 w-4 text-red-600 mr-1" />
                      Vulnerabilities Found
                    </h5>
                    <div className="space-y-2">
                      {analysis.vulnerabilities.map((vuln: any, index: number) => (
                        <div key={index} className="p-3 bg-red-50 border border-red-200 rounded">
                          <div className="flex items-center justify-between">
                            <span className="text-sm font-medium text-red-800">{vuln.type}</span>
                            <span className={`text-xs px-2 py-1 rounded ${
                              vuln.severity === 'high' ? 'bg-red-200 text-red-800' :
                              vuln.severity === 'medium' ? 'bg-yellow-200 text-yellow-800' :
                              'bg-blue-200 text-blue-800'
                            }`}>
                              {vuln.severity}
                            </span>
                          </div>
                          <p className="text-sm text-red-700 mt-1">{vuln.description}</p>
                          {vuln.line_number && (
                            <p className="text-xs text-red-600 mt-1">Line: {vuln.line_number}</p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Best Practices */}
                {analysis.best_practices && (
                  <div>
                    <h5 className="font-medium text-gray-900 mb-2 flex items-center">
                      <Shield className="h-4 w-4 text-green-600 mr-1" />
                      Best Practices
                    </h5>
                    <div className="space-y-2">
                      {analysis.best_practices.security?.map((practice: any, index: number) => (
                        <div key={index} className="flex items-center">
                          {practice.followed ? (
                            <CheckCircle className="h-4 w-4 text-green-600 mr-2" />
                          ) : (
                            <AlertTriangle className="h-4 w-4 text-yellow-600 mr-2" />
                          )}
                          <span className={`text-sm ${practice.followed ? 'text-green-700' : 'text-yellow-700'}`}>
                            {practice.practice}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Code className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>Enter contract code and click "Analyze Contract" to see results</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SmartContractAnalyzer;
