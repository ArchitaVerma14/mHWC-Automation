"""
Script to install the AAM app and verify it's ready for testing
"""

import subprocess
import os
import sys
import time

def run_command(cmd, description=""):
    """Run a shell command and return output"""
    try:
        print(f"\n▶ {description}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.stdout:
            print(result.stdout)
        if result.returncode != 0 and result.stderr:
            print(f"⚠ Warning: {result.stderr}")
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        print(f"✗ Error: {e}")
        return 1, "", str(e)


def check_adb():
    """Check if ADB is available"""
    print("\n" + "="*70)
    print("STEP 1: Checking ADB Connection")
    print("="*70)
    
    code, out, err = run_command("adb devices", "Checking connected devices")
    if "emulator-5554" in out or "device" in out:
        print("✓ Device connected successfully")
        return True
    else:
        print("✗ No device connected. Check emulator is running")
        return False


def check_app_installed():
    """Check if app is installed"""
    print("\n" + "="*70)
    print("STEP 2: Checking if AAM App is Installed")
    print("="*70)
    
    code, out, err = run_command(
        "adb shell pm list packages | findstr piramalswasthya",
        "Searching for AAM app package"
    )
    
    if "org.piramalswasthya.cho.niramay.uat" in out:
        print("✓ AAM app is installed")
        return True
    else:
        print("✗ AAM app is NOT installed")
        print("\nTo install the app:")
        print("1. Place the APK file in the project directory")
        print("2. Run: adb install path/to/app.apk")
        print("3. Or run: adb install-multiple app1.apk app2.apk ...")
        return False


def get_app_activities():
    """Get all launchable activities for the app"""
    print("\n" + "="*70)
    print("STEP 3: Finding Launchable Activities")
    print("="*70)
    
    code, out, err = run_command(
        "adb shell cmd package resolve-activity --brief org.piramalswasthya.cho.niramay.uat",
        "Getting app activities"
    )
    
    if code == 0 and out:
        print("\nAvailable activities:")
        print(out)
        return out.strip().split('\n')[-1] if out.strip() else None
    else:
        print("✗ Could not retrieve activities")
        return None


def clear_app_data():
    """Clear app data for fresh login"""
    print("\n" + "="*70)
    print("STEP 4: Clearing App Data (for fresh login)")
    print("="*70)
    
    code, out, err = run_command(
        "adb shell pm clear org.piramalswasthya.cho.niramay.uat",
        "Clearing app data"
    )
    
    if code == 0:
        print("✓ App data cleared")
        return True
    else:
        print("⚠ Could not clear app data (this is OK if first run)")
        return False


def launch_app():
    """Launch the app directly"""
    print("\n" + "="*70)
    print("STEP 5: Launching AAM App")
    print("="*70)
    
    package = "org.piramalswasthya.cho.niramay.uat"
    
    # Try different methods to launch
    methods = [
        (f'adb shell am start -n {package}/{package}.MainActivity', ".MainActivity"),
        (f'adb shell monkey -p {package} 1', "monkey (any activity)"),
        (f'adb shell am start -a android.intent.action.MAIN -n {package}/.MainActivity', "MAIN intent"),
    ]
    
    for cmd, method in methods:
        print(f"\nTrying: {method}")
        code, out, err = run_command(cmd, f"Attempting to launch using {method}")
        
        if code == 0 or "Successfully" in out or "Starting" in out:
            print(f"✓ App launched using {method}")
            return True
        else:
            if "Permission" in err or "unable to resolve" in err:
                print(f"  (Activity not exported or available)")
                continue
    
    print("\n✗ Could not launch app with direct activity")
    print("\nNote: The app will be launched automatically by Appium during test")
    return False


def verify_emulator():
    """Verify emulator is in good state"""
    print("\n" + "="*70)
    print("STEP 6: Verifying Emulator State")
    print("="*70)
    
    code, out, err = run_command("adb shell getprop ro.build.version.release", "Checking Android version")
    if code == 0:
        print(f"✓ Emulator is responsive. Android version: {out.strip()}")
        return True
    else:
        print("✗ Emulator not responsive")
        return False


def main():
    """Main setup function"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "AAM APP TEST ENVIRONMENT SETUP" + " "*24 + "║")
    print("╚" + "="*68 + "╝")
    
    # Check steps
    adb_ok = check_adb()
    
    if not adb_ok:
        print("\n✗ Setup failed: ADB/Emulator issue")
        sys.exit(1)
    
    emulator_ok = verify_emulator()
    app_installed = check_app_installed()
    activity = get_app_activities() if app_installed else None
    data_cleared = clear_app_data() if app_installed else None
    app_launched = launch_app() if app_installed else None
    
    # Summary
    print("\n" + "="*70)
    print("SETUP SUMMARY")
    print("="*70)
    print(f"✓ ADB Connection: OK")
    print(f"{'✓' if app_installed else '✗'} App Installed: {'YES' if app_installed else 'NO'}")
    print(f"{'✓' if data_cleared else '⚠'} App Data Cleared: {'YES' if data_cleared else 'NOT NEEDED'}")
    print(f"{'✓' if app_launched else '⚠'} Manual App Launch: {'SUCCESS' if app_launched else 'WILL USE APPIUM'}")
    
    if app_installed:
        print("\n✓ Environment is ready for testing!")
        print("\nRun test with:")
        print("  cd mHWC-Automation")
        print("  .\\venv\\Scripts\\pytest.exe tests/test_login_782.py -v -s")
    else:
        print("\n✗ App is not installed. Please:")
        print("  1. Download the APK file")
        print("  2. Run: adb install path/to/aam-app.apk")
        print("  3. Then run this script again")
        sys.exit(1)


if __name__ == "__main__":
    main()
