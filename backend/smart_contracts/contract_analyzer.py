"""
Smart Contract Analyzer
Provides tools for analyzing Solidity smart contracts including:
- Security vulnerability detection
- Gas optimization analysis
- Code quality assessment
- Best practices validation
"""

import re
import ast
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class VulnerabilityType(Enum):
    """Types of smart contract vulnerabilities"""
    REENTRANCY = "reentrancy"
    INTEGER_OVERFLOW = "integer_overflow"
    UNCHECKED_EXTERNAL_CALLS = "unchecked_external_calls"
    ACCESS_CONTROL = "access_control"
    GAS_LIMIT = "gas_limit"
    TIMESTAMP_DEPENDENCE = "timestamp_dependence"
    UNINITIALIZED_STORAGE = "uninitialized_storage"
    DELEGATE_CALL = "delegate_call"
    FRONTRUNNING = "frontrunning"
    DOS = "denial_of_service"


@dataclass
class Vulnerability:
    """Represents a detected vulnerability"""
    type: VulnerabilityType
    severity: str  # "low", "medium", "high", "critical"
    description: str
    line_number: Optional[int]
    code_snippet: Optional[str]
    recommendation: str


class ContractAnalyzer:
    """Smart contract security analyzer"""
    
    def __init__(self):
        self.vulnerability_patterns = self._initialize_patterns()
        self.gas_optimization_patterns = self._initialize_gas_patterns()
        self.best_practices = self._initialize_best_practices()
    
    def _initialize_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize vulnerability detection patterns"""
        return {
            "reentrancy": [
                {
                    "pattern": r"\.call\s*\(\s*[^)]*\)",
                    "description": "External call without reentrancy protection",
                    "severity": "high"
                },
                {
                    "pattern": r"\.send\s*\(\s*[^)]*\)",
                    "description": "Using .send() instead of .call()",
                    "severity": "medium"
                }
            ],
            "integer_overflow": [
                {
                    "pattern": r"(\w+)\s*\+\s*(\w+)",
                    "description": "Potential integer overflow in addition",
                    "severity": "medium"
                },
                {
                    "pattern": r"(\w+)\s*\*\s*(\w+)",
                    "description": "Potential integer overflow in multiplication",
                    "severity": "medium"
                }
            ],
            "unchecked_external_calls": [
                {
                    "pattern": r"(\w+)\.call\s*\(\s*[^)]*\)",
                    "description": "External call without checking return value",
                    "severity": "medium"
                }
            ],
            "access_control": [
                {
                    "pattern": r"function\s+(\w+)\s*\([^)]*\)\s*(?:public|external)",
                    "description": "Public function without access control",
                    "severity": "low"
                }
            ],
            "timestamp_dependence": [
                {
                    "pattern": r"block\.timestamp",
                    "description": "Using block.timestamp for critical operations",
                    "severity": "medium"
                },
                {
                    "pattern": r"now\s*[+\-*/]\s*\d+",
                    "description": "Timestamp-based calculations",
                    "severity": "medium"
                }
            ],
            "uninitialized_storage": [
                {
                    "pattern": r"storage\s+(\w+)\s*;",
                    "description": "Uninitialized storage variable",
                    "severity": "low"
                }
            ],
            "delegate_call": [
                {
                    "pattern": r"\.delegatecall\s*\(\s*[^)]*\)",
                    "description": "Using delegatecall - potential security risk",
                    "severity": "high"
                }
            ]
        }
    
    def _initialize_gas_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize gas optimization patterns"""
        return {
            "storage_optimization": [
                {
                    "pattern": r"storage\s+(\w+)\s*;",
                    "description": "Consider using memory for temporary variables",
                    "severity": "low"
                }
            ],
            "loop_optimization": [
                {
                    "pattern": r"for\s*\(\s*[^)]*\)\s*\{[^}]*storage[^}]*\}",
                    "description": "Storage access in loops - consider caching",
                    "severity": "medium"
                }
            ],
            "function_visibility": [
                {
                    "pattern": r"function\s+(\w+)\s*\([^)]*\)\s*public",
                    "description": "Consider using external for functions not called internally",
                    "severity": "low"
                }
            ]
        }
    
    def _initialize_best_practices(self) -> Dict[str, List[str]]:
        """Initialize best practices checklist"""
        return {
            "security": [
                "Use OpenZeppelin contracts for standard functionality",
                "Implement proper access control mechanisms",
                "Use SafeMath for arithmetic operations",
                "Validate all external inputs",
                "Implement emergency stop functionality",
                "Use events for important state changes",
                "Avoid using tx.origin for authorization",
                "Implement proper upgrade patterns"
            ],
            "gas_optimization": [
                "Use appropriate data locations (storage, memory, calldata)",
                "Pack structs efficiently",
                "Use events instead of storage for historical data",
                "Batch operations when possible",
                "Use external functions for functions not called internally",
                "Avoid unnecessary storage reads",
                "Use assembly for low-level operations when beneficial"
            ],
            "code_quality": [
                "Use descriptive variable and function names",
                "Add comprehensive documentation",
                "Implement proper error handling",
                "Use consistent coding style",
                "Add unit tests for all functions",
                "Use require statements with descriptive error messages",
                "Implement proper inheritance patterns"
            ]
        }
    
    def analyze_contract(self, contract_code: str) -> Dict[str, Any]:
        """Analyze a smart contract for vulnerabilities and issues"""
        try:
            vulnerabilities = self._detect_vulnerabilities(contract_code)
            gas_issues = self._analyze_gas_optimization(contract_code)
            best_practices_check = self._check_best_practices(contract_code)
            code_metrics = self._calculate_code_metrics(contract_code)
            
            return {
                "vulnerabilities": [v.__dict__ for v in vulnerabilities],
                "gas_optimization": gas_issues,
                "best_practices": best_practices_check,
                "code_metrics": code_metrics,
                "security_score": self._calculate_security_score(vulnerabilities),
                "gas_score": self._calculate_gas_score(gas_issues),
                "overall_score": self._calculate_overall_score(vulnerabilities, gas_issues)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing contract: {e}")
            return {"error": str(e)}
    
    def _detect_vulnerabilities(self, contract_code: str) -> List[Vulnerability]:
        """Detect vulnerabilities in the contract code"""
        vulnerabilities = []
        lines = contract_code.split('\n')
        
        for vuln_type, patterns in self.vulnerability_patterns.items():
            for pattern_info in patterns:
                pattern = pattern_info["pattern"]
                matches = re.finditer(pattern, contract_code, re.IGNORECASE)
                
                for match in matches:
                    # Find line number
                    line_number = None
                    for i, line in enumerate(lines):
                        if match.group() in line:
                            line_number = i + 1
                            break
                    
                    vulnerability = Vulnerability(
                        type=VulnerabilityType(vuln_type),
                        severity=pattern_info["severity"],
                        description=pattern_info["description"],
                        line_number=line_number,
                        code_snippet=match.group(),
                        recommendation=self._get_recommendation(vuln_type)
                    )
                    vulnerabilities.append(vulnerability)
        
        return vulnerabilities
    
    def _analyze_gas_optimization(self, contract_code: str) -> List[Dict[str, Any]]:
        """Analyze gas optimization opportunities"""
        gas_issues = []
        lines = contract_code.split('\n')
        
        for issue_type, patterns in self.gas_optimization_patterns.items():
            for pattern_info in patterns:
                pattern = pattern_info["pattern"]
                matches = re.finditer(pattern, contract_code, re.IGNORECASE)
                
                for match in matches:
                    # Find line number
                    line_number = None
                    for i, line in enumerate(lines):
                        if match.group() in line:
                            line_number = i + 1
                            break
                    
                    gas_issues.append({
                        "type": issue_type,
                        "severity": pattern_info["severity"],
                        "description": pattern_info["description"],
                        "line_number": line_number,
                        "code_snippet": match.group(),
                        "recommendation": self._get_gas_recommendation(issue_type)
                    })
        
        return gas_issues
    
    def _check_best_practices(self, contract_code: str) -> Dict[str, List[Dict[str, Any]]]:
        """Check adherence to best practices"""
        results = {}
        
        for category, practices in self.best_practices.items():
            category_results = []
            for practice in practices:
                # Simple keyword-based checking (can be enhanced)
                is_followed = self._check_practice_followed(contract_code, practice)
                category_results.append({
                    "practice": practice,
                    "followed": is_followed,
                    "recommendation": practice if not is_followed else "Good practice followed"
                })
            results[category] = category_results
        
        return results
    
    def _check_practice_followed(self, contract_code: str, practice: str) -> bool:
        """Check if a specific best practice is followed"""
        practice_lower = practice.lower()
        code_lower = contract_code.lower()
        
        # Simple keyword-based checking
        if "safemath" in practice_lower and "safemath" in code_lower:
            return True
        elif "openzeppelin" in practice_lower and "openzeppelin" in code_lower:
            return True
        elif "require" in practice_lower and "require" in code_lower:
            return True
        elif "event" in practice_lower and "event" in code_lower:
            return True
        elif "external" in practice_lower and "external" in code_lower:
            return True
        
        return False
    
    def _calculate_code_metrics(self, contract_code: str) -> Dict[str, Any]:
        """Calculate code quality metrics"""
        lines = contract_code.split('\n')
        total_lines = len(lines)
        non_empty_lines = len([line for line in lines if line.strip()])
        
        # Count functions
        function_count = len(re.findall(r'function\s+\w+', contract_code))
        
        # Count variables
        variable_count = len(re.findall(r'(?:uint|int|bool|address|string|bytes)\s+\w+', contract_code))
        
        # Count comments
        comment_lines = len([line for line in lines if line.strip().startswith('//') or line.strip().startswith('/*')])
        
        return {
            "total_lines": total_lines,
            "non_empty_lines": non_empty_lines,
            "function_count": function_count,
            "variable_count": variable_count,
            "comment_lines": comment_lines,
            "comment_ratio": comment_lines / non_empty_lines if non_empty_lines > 0 else 0
        }
    
    def _get_recommendation(self, vuln_type: str) -> str:
        """Get recommendation for vulnerability type"""
        recommendations = {
            "reentrancy": "Use ReentrancyGuard or implement checks-effects-interactions pattern",
            "integer_overflow": "Use SafeMath library or Solidity 0.8+ which has built-in overflow protection",
            "unchecked_external_calls": "Always check return values of external calls",
            "access_control": "Implement proper access control using modifiers or OpenZeppelin's AccessControl",
            "timestamp_dependence": "Avoid using block.timestamp for critical operations, consider using block numbers",
            "uninitialized_storage": "Always initialize storage variables",
            "delegate_call": "Be extremely careful with delegatecall, understand the security implications"
        }
        return recommendations.get(vuln_type, "Review the code for potential security issues")
    
    def _get_gas_recommendation(self, issue_type: str) -> str:
        """Get recommendation for gas optimization"""
        recommendations = {
            "storage_optimization": "Use memory for temporary variables, pack structs efficiently",
            "loop_optimization": "Cache storage variables in memory when used in loops",
            "function_visibility": "Use external for functions not called internally"
        }
        return recommendations.get(issue_type, "Consider gas optimization techniques")
    
    def _calculate_security_score(self, vulnerabilities: List[Vulnerability]) -> float:
        """Calculate security score based on vulnerabilities"""
        if not vulnerabilities:
            return 100.0
        
        score = 100.0
        severity_weights = {
            "low": 5,
            "medium": 15,
            "high": 30,
            "critical": 50
        }
        
        for vuln in vulnerabilities:
            score -= severity_weights.get(vuln.severity, 10)
        
        return max(0.0, score)
    
    def _calculate_gas_score(self, gas_issues: List[Dict[str, Any]]) -> float:
        """Calculate gas optimization score"""
        if not gas_issues:
            return 100.0
        
        score = 100.0
        severity_weights = {
            "low": 3,
            "medium": 8,
            "high": 15
        }
        
        for issue in gas_issues:
            score -= severity_weights.get(issue["severity"], 5)
        
        return max(0.0, score)
    
    def _calculate_overall_score(self, vulnerabilities: List[Vulnerability], gas_issues: List[Dict[str, Any]]) -> float:
        """Calculate overall contract score"""
        security_score = self._calculate_security_score(vulnerabilities)
        gas_score = self._calculate_gas_score(gas_issues)
        
        # Weight security more heavily than gas optimization
        return (security_score * 0.7) + (gas_score * 0.3)
    
    def get_common_vulnerabilities(self) -> List[Dict[str, Any]]:
        """Get list of common smart contract vulnerabilities"""
        return [
            {
                "name": "Reentrancy",
                "description": "Attack where a contract calls an external contract before updating its own state",
                "severity": "High",
                "example": "function withdraw() { msg.sender.call{value: balances[msg.sender]}(); balances[msg.sender] = 0; }",
                "prevention": "Use ReentrancyGuard or implement checks-effects-interactions pattern"
            },
            {
                "name": "Integer Overflow/Underflow",
                "description": "Arithmetic operations that exceed the maximum or minimum value of a data type",
                "severity": "Medium",
                "example": "uint256 a = 2**256 - 1; uint256 b = a + 1; // This will overflow",
                "prevention": "Use SafeMath library or Solidity 0.8+"
            },
            {
                "name": "Unchecked External Calls",
                "description": "External calls without proper error handling",
                "severity": "Medium",
                "example": "someContract.someFunction(); // No return value check",
                "prevention": "Always check return values and handle failures"
            },
            {
                "name": "Access Control Issues",
                "description": "Functions that can be called by unauthorized users",
                "severity": "Medium",
                "example": "function transferFunds() public { // No access control }",
                "prevention": "Use modifiers or OpenZeppelin's AccessControl"
            },
            {
                "name": "Timestamp Dependence",
                "description": "Using block.timestamp for critical operations",
                "severity": "Medium",
                "example": "require(block.timestamp > deadline);",
                "prevention": "Use block numbers or be aware of timestamp manipulation"
            }
        ]
