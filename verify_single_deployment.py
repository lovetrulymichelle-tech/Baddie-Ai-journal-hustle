#!/usr/bin/env python3
"""
Single Deployment Verification Script for Baddie AI Journal Hustle.

This script helps verify that only one deployment configuration exists.
"""

import os
import sys
from datetime import datetime, UTC


def check_deployment_files():
    """Check for deployment configuration files."""
    print("🔍 Checking deployment configuration files...")
    
    # Expected files (should exist)
    expected_files = {
        "Procfile": "Railway deployment configuration",
        "requirements.txt": "Python dependencies",
        "app.py": "Main Flask application"
    }
    
    # Conflicting files (should NOT exist)
    conflicting_files = {
        "Dockerfile": "Docker deployment (conflicts with Railway)",
        "vercel.json": "Vercel deployment (conflicts with Railway)",
        "docker-compose.yml": "Docker Compose (conflicts with Railway)",
        ".gitlab-ci.yml": "GitLab CI deployment (conflicts with Railway)",
        "heroku.yml": "Heroku container deployment (conflicts with Railway)"
    }
    
    print("\n✅ Expected files (should exist):")
    missing_expected = []
    for file, description in expected_files.items():
        if os.path.exists(file):
            print(f"   ✅ {file} - {description}")
        else:
            print(f"   ❌ {file} - MISSING - {description}")
            missing_expected.append(file)
    
    print("\n⚠️  Conflicting files (should NOT exist):")
    found_conflicts = []
    for file, description in conflicting_files.items():
        if os.path.exists(file):
            print(f"   ❌ {file} - FOUND - {description}")
            found_conflicts.append(file)
        else:
            print(f"   ✅ {file} - Not found (good)")
    
    return missing_expected, found_conflicts


def check_deployment_policy():
    """Check if deployment policy exists."""
    print("\n📋 Checking deployment policy...")
    
    if os.path.exists("DEPLOYMENT_POLICY.md"):
        print("   ✅ DEPLOYMENT_POLICY.md exists")
        return True
    else:
        print("   ❌ DEPLOYMENT_POLICY.md missing")
        return False


def main():
    """Run deployment verification."""
    print("🚀 Single Deployment Verification")
    print(f"   Running at: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 50)
    
    missing_expected, found_conflicts = check_deployment_files()
    policy_exists = check_deployment_policy()
    
    print("\n" + "=" * 50)
    
    # Determine overall status
    if missing_expected:
        print("❌ MISSING REQUIRED FILES:")
        for file in missing_expected:
            print(f"   - {file}")
        print("\n   Solution: Ensure all required files are present")
        
    if found_conflicts:
        print("⚠️  CONFLICTING DEPLOYMENT FILES FOUND:")
        for file in found_conflicts:
            print(f"   - {file}")
        print("\n   Solution: Remove conflicting files to prevent multiple deployments")
        print("   Command: rm " + " ".join(found_conflicts))
        
    if not policy_exists:
        print("⚠️  DEPLOYMENT POLICY MISSING")
        print("   Solution: Create DEPLOYMENT_POLICY.md to document single deployment approach")
    
    # Final status
    if not missing_expected and not found_conflicts and policy_exists:
        print("🎉 VERIFICATION PASSED")
        print("✅ Single deployment configuration verified")
        print("✅ Only Railway deployment method configured")
        print("✅ No conflicting deployment files found")
        print("\n🚀 Ready for single Railway deployment!")
        return 0
    else:
        print("❌ VERIFICATION FAILED")
        print("🔧 Fix the issues above before deploying")
        return 1


if __name__ == "__main__":
    sys.exit(main())