"""
Test script to verify WorkspaceClient() initialization with different configurations.
"""
from databricks.sdk import WorkspaceClient
import os
import sys


def test_without_config():
    """Test 1: WorkspaceClient() without any configuration"""
    print("=" * 60)
    print("TEST 1: WorkspaceClient() without any configuration")
    print("=" * 60)
    
    try:
        w = WorkspaceClient()
        user = w.current_user.me()
        print(f"✅ SUCCESS: Connected as {user.user_name}")
        print(f"   User ID: {user.id}")
        print(f"   Active: {user.active}")
        return True
    except Exception as e:
        print(f"❌ FAILED: {type(e).__name__}")
        print(f"   Message: {str(e)[:150]}")
        return False


def test_with_profile_param_dev():
    """Test 2: WorkspaceClient(profile='dev')"""
    print("\n" + "=" * 60)
    print("TEST 2: WorkspaceClient(profile='dev')")
    print("=" * 60)
    
    try:
        w = WorkspaceClient(profile='dev')
        user = w.current_user.me()
        print(f"✅ SUCCESS: Connected as {user.user_name}")
        print(f"   User ID: {user.id}")
        print(f"   Active: {user.active}")
        return True
    except Exception as e:
        print(f"❌ FAILED: {type(e).__name__}")
        print(f"   Message: {str(e)[:150]}")
        return False


def test_with_dotenv():
    """Test 3: WorkspaceClient() with .env file (if exists)"""
    print("\n" + "=" * 60)
    print("TEST 3: WorkspaceClient() with .env file")
    print("=" * 60)
    
    from pathlib import Path
    env_file = Path(".env")
    
    if not env_file.exists():
        print("⚠️  SKIPPED: .env file does not exist")
        return None
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        profile = os.getenv('DATABRICKS_CONFIG_PROFILE')
        print(f"   .env sets DATABRICKS_CONFIG_PROFILE={profile}")
        
        w = WorkspaceClient()
        user = w.current_user.me()
        print(f"✅ SUCCESS: Connected as {user.user_name}")
        print(f"   User ID: {user.id}")
        print(f"   Active: {user.active}")
        return True
    except Exception as e:
        print(f"❌ FAILED: {type(e).__name__}")
        print(f"   Message: {str(e)[:150]}")
        return False


def main():
    """Run all tests and provide summary"""
    print("\n🧪 Testing WorkspaceClient Initialization\n")
    
    results = {
        "Test 1 (No config)": test_without_config(),
        "Test 2 (profile='dev')": test_with_profile_param_dev(),
        "Test 3 (.env file)": test_with_dotenv(),
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    
    for test_name, result in results.items():
        if result is True:
            status = "✅ PASSED"
        elif result is False:
            status = "❌ FAILED"
        else:
            status = "⚠️  SKIPPED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")
    
    # Recommendations
    print("\n" + "=" * 60)
    print("💡 RECOMMENDATIONS")
    print("=" * 60)
    
    if results["Test 1 (No config)"] is False:
        print("❌ WorkspaceClient() does NOT work without configuration")
        print("\n✅ Working solutions:")
        
        if results["Test 2 (profile='dev')"] is True:
            print("   1. Use explicit parameter: WorkspaceClient(profile='dev')")
        
        print("\n📝 Recommended approach for your app:")
        print("   Add to .env file: DATABRICKS_CONFIG_PROFILE=dev")
        print("   Then use: WorkspaceClient() in your code")
    else:
        print("✅ WorkspaceClient() works without explicit configuration!")
    
    print("\n")
    
    # Exit code
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
