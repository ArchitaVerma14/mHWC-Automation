"""
Helper script to find the correct launcher activity for the app
Run this to identify which activity can be launched
"""

import subprocess
import sys

def get_launcher_activity(package_name):
    """
    Get the launcher activity for the given package
    """
    try:
        # Get all activities
        cmd = f'adb shell cmd package resolve-activity --brief {package_name}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        print(f"\n{'='*70}")
        print(f"Activities available for {package_name}:")
        print(f"{'='*70}\n")
        print(result.stdout)
        print(f"{'='*70}\n")
        
        # Try to get dumpsys output
        cmd2 = f'adb shell dumpsys package {package_name}'
        result2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
        
        if "android.intent.action.MAIN" in result2.stdout:
            print("Found MAIN activities:")
            for line in result2.stdout.split('\n'):
                if "android.intent.action.MAIN" in line or "android.intent.category.LAUNCHER" in line:
                    print(line)
        
        return result.stdout
        
    except Exception as e:
        print(f"Error: {e}")
        return None


def test_activity_launch(package_name, activity_name):
    """
    Test if an activity can be launched
    """
    try:
        full_activity = f"{package_name}/{activity_name}" if "/" not in activity_name else activity_name
        
        print(f"\nTesting activity: {full_activity}")
        cmd = f'adb shell am start-activity -W -n {full_activity} -a android.intent.action.MAIN -c android.intent.category.LAUNCHER'
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ SUCCESS: Activity launched successfully!")
            return True
        else:
            print("✗ FAILED: Activity could not be launched")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    package = "org.piramalswasthya.cho.niramay.uat"
    
    print("\n" + " "*70)
    print(" Finding Correct Launcher Activity for AAM App")
    print(" "*70)
    
    # Get all activities
    activities = get_launcher_activity(package)
    
    # Test common activity names
    print("\n" + "="*70)
    print("Testing common launcher activities:")
    print("="*70)
    
    test_activities = [
        ".MainActivity",
        ".ui.home_activity.HomeActivity",
        ".HomeActivity",
        ".SplashActivity",
        ".LoginActivity",
    ]
    
    for activity in test_activities:
        print(f"\nTesting: {activity}")
        test_activity_launch(package, activity)
