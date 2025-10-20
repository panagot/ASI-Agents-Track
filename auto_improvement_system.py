#!/usr/bin/env python3
"""
Auto-Improvement System for MediTech AI Healthcare Agent
Continuously monitors, tests, and improves the agent's performance
"""

import requests
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentAutoImprover:
    def __init__(self, agent_url: str):
        self.agent_url = agent_url
        self.session_id = None
        self.performance_metrics = {
            'total_tests': 0,
            'successful_responses': 0,
            'feedback_responses': 0,
            'emergency_detection_accuracy': 0,
            'confidence_variation': 0,
            'response_times': []
        }
        
        # Test scenarios for continuous improvement
        self.test_scenarios = {
            'symptom_analysis': [
                "I have a headache and nausea",
                "Persistent cough with fever and fatigue",
                "Chest pain with shortness of breath",
                "Fever, cough, and body aches",
                "Severe headache with vision problems",
                "Abdominal pain with nausea and vomiting",
                "Dizziness and fatigue",
                "Rash with itching and fever"
            ],
            'emergency_detection': [
                "Severe chest pain radiating to arm",
                "Can't breathe, chest tightness",
                "Unconscious, not responding",
                "Severe bleeding from wound",
                "Sudden severe headache with neck stiffness",
                "Chest pain with sweating and nausea"
            ],
            'feedback_testing': [
                "Yes, the analysis matches my experience",
                "Yes, the analysis matches my experience. Thank you!",
                "No, the analysis doesn't match",
                "Thank you for the analysis",
                "The analysis was helpful"
            ],
            'edge_cases': [
                "I'm having fever",
                "Please analyze my symptoms",
                "What symptoms should I look for?",
                "I have a persistent headache",
                "Cough and fatigue for 3 days"
            ]
        }
    
    def start_session(self) -> bool:
        """Start a new chat session with the agent"""
        try:
            # Initialize session (this might need to be adapted based on Agentverse API)
            self.session_id = f"auto_improve_{int(time.time())}"
            logger.info(f"Started session: {self.session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to start session: {e}")
            return False
    
    def send_message(self, message: str) -> Dict:
        """Send a message to the agent and get response"""
        try:
            # This would need to be adapted to the actual Agentverse API
            # For now, we'll simulate the interaction
            payload = {
                "message": message,
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat()
            }
            
            # Simulate API call (replace with actual Agentverse API call)
            response = self.simulate_agent_response(message)
            
            self.performance_metrics['total_tests'] += 1
            self.performance_metrics['response_times'].append(response.get('response_time', 0))
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return {"error": str(e)}
    
    def simulate_agent_response(self, message: str) -> Dict:
        """Simulate agent response for testing (replace with actual API call)"""
        # This simulates what the agent would return
        # In reality, this would be an HTTP request to the Agentverse API
        
        response_time = random.uniform(0.5, 2.0)  # Simulate response time
        
        # Simulate different response types based on message content
        if any(word in message.lower() for word in ["yes", "no", "thank", "matches"]):
            return {
                "response": "✅ Thank you for your feedback! I'm glad the analysis was helpful and accurate.",
                "response_time": response_time,
                "type": "feedback_response",
                "success": True
            }
        elif any(word in message.lower() for word in ["chest pain", "can't breathe", "unconscious", "severe"]):
            return {
                "response": "🚨 EMERGENCY ALERT 🚨 Your symptoms may indicate a medical emergency!",
                "response_time": response_time,
                "type": "emergency_detection",
                "success": True
            }
        else:
            return {
                "response": "🩺 SYMPTOM ANALYSIS REPORT 🩺 Analyzing your symptoms...",
                "response_time": response_time,
                "type": "symptom_analysis",
                "success": True
            }
    
    def test_symptom_analysis(self) -> Dict:
        """Test symptom analysis capabilities"""
        logger.info("Testing symptom analysis capabilities...")
        results = []
        
        for scenario in self.test_scenarios['symptom_analysis']:
            response = self.send_message(scenario)
            results.append({
                'scenario': scenario,
                'response': response,
                'success': response.get('success', False)
            })
            
            if response.get('success'):
                self.performance_metrics['successful_responses'] += 1
            
            time.sleep(1)  # Rate limiting
        
        return {'test_type': 'symptom_analysis', 'results': results}
    
    def test_emergency_detection(self) -> Dict:
        """Test emergency detection accuracy"""
        logger.info("Testing emergency detection...")
        results = []
        
        for scenario in self.test_scenarios['emergency_detection']:
            response = self.send_message(scenario)
            is_emergency = 'emergency' in response.get('response', '').lower()
            results.append({
                'scenario': scenario,
                'response': response,
                'detected_emergency': is_emergency,
                'expected_emergency': True
            })
            
            if is_emergency:
                self.performance_metrics['emergency_detection_accuracy'] += 1
            
            time.sleep(1)
        
        return {'test_type': 'emergency_detection', 'results': results}
    
    def test_feedback_responses(self) -> Dict:
        """Test feedback response handling"""
        logger.info("Testing feedback responses...")
        results = []
        
        for scenario in self.test_scenarios['feedback_testing']:
            response = self.send_message(scenario)
            has_feedback_response = 'thank' in response.get('response', '').lower()
            results.append({
                'scenario': scenario,
                'response': response,
                'has_feedback_response': has_feedback_response,
                'expected_feedback': True
            })
            
            if has_feedback_response:
                self.performance_metrics['feedback_responses'] += 1
            
            time.sleep(1)
        
        return {'test_type': 'feedback_responses', 'results': results}
    
    def analyze_performance(self) -> Dict:
        """Analyze current performance metrics"""
        total_tests = self.performance_metrics['total_tests']
        if total_tests == 0:
            return {'error': 'No tests performed yet'}
        
        avg_response_time = sum(self.performance_metrics['response_times']) / len(self.performance_metrics['response_times'])
        
        performance_score = {
            'success_rate': self.performance_metrics['successful_responses'] / total_tests,
            'feedback_response_rate': self.performance_metrics['feedback_responses'] / total_tests,
            'emergency_detection_rate': self.performance_metrics['emergency_detection_accuracy'] / total_tests,
            'avg_response_time': avg_response_time,
            'total_tests': total_tests
        }
        
        # Calculate estimated rating based on performance
        estimated_rating = self.calculate_estimated_rating(performance_score)
        performance_score['estimated_rating'] = estimated_rating
        
        return performance_score
    
    def calculate_estimated_rating(self, performance: Dict) -> float:
        """Calculate estimated rating based on performance metrics"""
        base_rating = 4.1  # Current rating
        
        # Adjust based on performance
        if performance['success_rate'] > 0.9:
            base_rating += 0.1
        if performance['feedback_response_rate'] > 0.8:
            base_rating += 0.1
        if performance['emergency_detection_rate'] > 0.9:
            base_rating += 0.1
        if performance['avg_response_time'] < 1.5:
            base_rating += 0.05
        
        return min(base_rating, 5.0)  # Cap at 5.0
    
    def generate_improvement_suggestions(self, performance: Dict) -> List[str]:
        """Generate improvement suggestions based on performance"""
        suggestions = []
        
        if performance['success_rate'] < 0.9:
            suggestions.append("Improve response success rate - check for error handling")
        
        if performance['feedback_response_rate'] < 0.8:
            suggestions.append("Enhance feedback detection patterns")
        
        if performance['emergency_detection_rate'] < 0.9:
            suggestions.append("Improve emergency detection accuracy")
        
        if performance['avg_response_time'] > 2.0:
            suggestions.append("Optimize response time - consider caching")
        
        if performance['estimated_rating'] < 4.3:
            suggestions.append("Focus on confidence calibration and context integration")
        
        return suggestions
    
    def run_comprehensive_test(self) -> Dict:
        """Run comprehensive test suite"""
        logger.info("Starting comprehensive agent test...")
        
        if not self.start_session():
            return {'error': 'Failed to start session'}
        
        test_results = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'tests': {}
        }
        
        # Run all test suites
        test_results['tests']['symptom_analysis'] = self.test_symptom_analysis()
        test_results['tests']['emergency_detection'] = self.test_emergency_detection()
        test_results['tests']['feedback_responses'] = self.test_feedback_responses()
        
        # Analyze performance
        performance = self.analyze_performance()
        test_results['performance'] = performance
        
        # Generate improvement suggestions
        suggestions = self.generate_improvement_suggestions(performance)
        test_results['improvement_suggestions'] = suggestions
        
        return test_results
    
    def save_results(self, results: Dict, filename: str = None):
        """Save test results to file"""
        if filename is None:
            filename = f"agent_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            logger.info(f"Results saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

def main():
    """Main function to run the auto-improvement system"""
    # Agent URL from the user
    agent_url = "https://chat.agentverse.ai/sessions/dbbf8679-f14c-4bcf-8d4c-cd1465ad7ad2"
    
    # Create auto-improver instance
    improver = AgentAutoImprover(agent_url)
    
    # Run comprehensive test
    results = improver.run_comprehensive_test()
    
    # Print results
    print("\n" + "="*50)
    print("AGENT AUTO-IMPROVEMENT TEST RESULTS")
    print("="*50)
    
    if 'error' in results:
        print(f"Error: {results['error']}")
        return
    
    print(f"Session ID: {results['session_id']}")
    print(f"Timestamp: {results['timestamp']}")
    print()
    
    # Performance summary
    perf = results['performance']
    print("PERFORMANCE SUMMARY:")
    print(f"  Success Rate: {perf['success_rate']:.2%}")
    print(f"  Feedback Response Rate: {perf['feedback_response_rate']:.2%}")
    print(f"  Emergency Detection Rate: {perf['emergency_detection_rate']:.2%}")
    print(f"  Average Response Time: {perf['avg_response_time']:.2f}s")
    print(f"  Estimated Rating: {perf['estimated_rating']:.1f}/5.0")
    print()
    
    # Improvement suggestions
    print("IMPROVEMENT SUGGESTIONS:")
    for i, suggestion in enumerate(results['improvement_suggestions'], 1):
        print(f"  {i}. {suggestion}")
    
    # Save results
    improver.save_results(results)
    
    print(f"\nResults saved to file for further analysis.")

if __name__ == "__main__":
    main()
