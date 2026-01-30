#!/usr/bin/env python3
"""
Test script to verify the fix for missing feature names error.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# Test data for Implementation Estimation
implementation_test_data = {
    "Feature_ID": "TEST_001",
    "No_of_UserStories": "5",
    "Story_Complexity": "2",
    "Design_Complexity": "2",
    "Meta_Complexity": "1",
    "Features_Impacted": "3",
    "Files_Impacted": "4",
    "Approx_LOC_Source": "1500",
    "Approx_LOC_Test": "500",
    "Approx_Code_Complexity": "2",
    "No_of_Interfaces_Impacted": "2",
    "Interface_Complexity": "1",
    "Interfaces_Added": "1",
    "Interfaces_Updated": "1",
    "Interfaces_Deleted": "0",
    "Integration_Complexity": "2",
    "CrossComponent_Dependencies": "1",
    "OAM_Simulator_Change": "0",
    "UT_Count": "10",
    "PYSCT_Count": "5",
    "New_Test_Cases": "15",
    "Test_Case_Complexity": "2",
    "Test_Coverage": "85",
    "Review_Needed": "1",
    "Legacy_Test_Coverage (%)": "50",
    "ICFS_Design_Complexity": "2",
    "PM_impact": "0",
    "CM_impact": "0",
    "FM_impact": "0",
    "Tech_Lead_Support": "1",
    "estimate": "Estimate Implementation Effort"
}

# Test data for Grooming Estimation
grooming_test_data = {
    "Feature_ID": "TEST_002",
    "No_of_UserStories": "4",
    "Story_Complexity": "2",
    "Design_Complexity": "2",
    "Meta_Complexity": "1",
    "Assumptions_Count": "2",
    "Features_Impacted": "2",
    "Codebase_Study_Required": "1",
    "No_of_Interfaces_Impacted": "1",
    "Interface_Complexity": "1",
    "Existing_Design_Study_Required": "0",
    "CrossComponent_Dependencies": "1",
    "ICFS_Design_Complexity": "1",
    "META_Impact_Level": "1",
    "Cloud_Deployment": "0",
    "Classical_Deployment": "1",
    "PM_impact": "0",
    "CM_impact": "0",
    "FM_impact": "0",
    "Fronthaul_impact": "1",
    "Backhaul_impact": "1",
    "Tech_Lead_Support": "0",
    "Open_Points_Percentage": "10",
    "estimate": "Estimate Grooming Effort"
}

def test_implementation_estimation():
    print("\n" + "="*60)
    print("Testing Implementation Effort Estimation")
    print("="*60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/implementation",
            data=implementation_test_data
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Check if prediction is in the response
            if "Estimated Implementation Hours" in response.text:
                print("✓ SUCCESS: Estimation completed without missing feature error")
                # Extract the prediction value
                import re
                match = re.search(r"Estimated Implementation Hours: <strong>([\d.]+)</strong>", response.text)
                if match:
                    print(f"✓ Predicted Hours: {match.group(1)}")
                return True
            elif "Missing feature" in response.text or "error-box" in response.text:
                print("✗ FAILED: Error message found in response")
                # Extract error
                import re
                match = re.search(r"<div class=\"error-box\">([^<]+)</div>", response.text)
                if match:
                    print(f"  Error: {match.group(1)}")
                return False
        else:
            print(f"✗ FAILED: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False

def test_grooming_estimation():
    print("\n" + "="*60)
    print("Testing Grooming Effort Estimation")
    print("="*60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/grooming",
            data=grooming_test_data
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Check if prediction is in the response
            if "Estimated Grooming Hours" in response.text:
                print("✓ SUCCESS: Estimation completed without missing feature error")
                # Extract the prediction value
                import re
                match = re.search(r"Estimated Grooming Hours: <strong>([\d.]+)</strong>", response.text)
                if match:
                    print(f"✓ Predicted Hours: {match.group(1)}")
                return True
            elif "Missing feature" in response.text or "error-box" in response.text:
                print("✗ FAILED: Error message found in response")
                # Extract error
                import re
                match = re.search(r"<div class=\"error-box\">([^<]+)</div>", response.text)
                if match:
                    print(f"  Error: {match.group(1)}")
                return False
        else:
            print(f"✗ FAILED: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    print("\nStarting Test Suite for Feature Name Fix")
    print("Test URL: " + BASE_URL)
    
    impl_result = test_implementation_estimation()
    groom_result = test_grooming_estimation()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Implementation Estimation: {'PASSED ✓' if impl_result else 'FAILED ✗'}")
    print(f"Grooming Estimation:       {'PASSED ✓' if groom_result else 'FAILED ✗'}")
    print("="*60)
    
    if impl_result and groom_result:
        print("\n✓ All tests passed! The fix is working correctly.")
        exit(0)
    else:
        print("\n✗ Some tests failed. Please review the errors above.")
        exit(1)
