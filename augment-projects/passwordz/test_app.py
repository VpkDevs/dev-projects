"""
Test script for the password extraction tool.
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_browser_detection():
    """Test browser detection functionality."""
    print("Testing browser detection...")
    
    from browser_detector import BrowserDetector
    
    detector = BrowserDetector()
    profiles = detector.detect_all_profiles()
    
    print(f"Found {len(profiles)} browser profiles:")
    for profile in profiles:
        print(f"  - {profile}")
    
    return len(profiles) > 0

def test_password_analyzer():
    """Test password analysis functionality."""
    print("\nTesting password analyzer...")
    
    from password_analyzer import PasswordAnalyzer
    
    analyzer = PasswordAnalyzer()
    
    # Test with sample passwords
    test_passwords = [
        "password123",
        "MyStr0ngP@ssw0rd!",
        "123456",
        "qwerty",
        "admin",
        "P@ssw0rd2023!",
        "weakpass",
        "VeryStrongPassword123!@#"
    ]
    
    print(f"Analyzing {len(test_passwords)} test passwords...")
    
    # Analyze individual passwords
    for password in test_passwords[:3]:  # Just test first 3
        analysis = analyzer.analyze_password(password)
        print(f"  Password: {password}")
        print(f"    Strength: {analysis.strength_level} ({analysis.strength_score:.1f}/100)")
        print(f"    Length: {analysis.length}, Entropy: {analysis.entropy:.1f}")
    
    # Analyze the entire list
    list_analysis = analyzer.analyze_password_list(test_passwords)
    print(f"\nList Analysis:")
    print(f"  Total: {list_analysis['total_passwords']}")
    print(f"  Unique: {list_analysis['unique_passwords']}")
    print(f"  Average Length: {list_analysis['average_length']}")
    print(f"  Average Strength: {list_analysis['average_strength_score']:.1f}")
    
    return True

def test_statistics():
    """Test statistics functionality."""
    print("\nTesting statistics...")
    
    from extraction_stats import StatisticsManager
    
    stats = StatisticsManager('test_stats.json')
    
    # Simulate a session
    stats.start_session()
    stats.add_profile_result("Google Chrome", 15, False)
    stats.add_profile_result("Microsoft Edge", 8, False)
    stats.add_profile_result("Firefox", 0, True)  # Error case
    session = stats.end_session(20)  # 20 unique passwords
    
    print(f"Session completed:")
    print(f"  Profiles scanned: {session.profiles_scanned}")
    print(f"  Passwords found: {session.passwords_found}")
    print(f"  Unique passwords: {session.unique_passwords}")
    print(f"  Success rate: {session.success_rate:.1f}%")
    
    # Get summary
    summary = stats.get_summary_stats()
    print(f"Summary stats:")
    print(f"  Total extractions: {summary['total_extractions']}")
    print(f"  Total passwords: {summary['total_passwords_found']}")
    
    # Clean up test file
    try:
        os.remove('test_stats.json')
    except:
        pass
    
    return True

def test_config():
    """Test configuration functionality."""
    print("\nTesting configuration...")
    
    from config import Config
    
    config = Config('test_config.json')
    
    # Test getting values
    window_width = config.get('ui.window_width', 800)
    print(f"Window width: {window_width}")
    
    # Test setting values
    config.set('ui.window_width', 1200)
    config.save_config()
    
    # Test loading
    new_config = Config('test_config.json')
    new_width = new_config.get('ui.window_width')
    print(f"New window width: {new_width}")
    
    # Clean up test file
    try:
        os.remove('test_config.json')
    except:
        pass
    
    return new_width == 1200

def test_encryption():
    """Test encryption functionality."""
    print("\nTesting encryption...")
    
    from encryption import PasswordEncryption
    
    encryption = PasswordEncryption('test_encryption.key')
    
    # Test password list encryption
    test_passwords = ["password1", "password2", "password3"]
    
    encrypted_data = encryption.encrypt_password_list(test_passwords)
    print(f"Encrypted {len(test_passwords)} passwords")
    
    decrypted_passwords = encryption.decrypt_password_list(encrypted_data)
    print(f"Decrypted {len(decrypted_passwords)} passwords")
    
    success = test_passwords == decrypted_passwords
    print(f"Encryption/Decryption successful: {success}")
    
    # Clean up test file
    try:
        os.remove('test_encryption.key')
    except:
        pass
    
    return success

def main():
    """Run all tests."""
    print("Running Password Extraction Tool Tests")
    print("=" * 40)
    
    tests = [
        ("Browser Detection", test_browser_detection),
        ("Password Analyzer", test_password_analyzer),
        ("Statistics", test_statistics),
        ("Configuration", test_config),
        ("Encryption", test_encryption)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result, None))
        except Exception as e:
            results.append((test_name, False, str(e)))
    
    print("\n" + "=" * 40)
    print("Test Results:")
    print("=" * 40)
    
    passed = 0
    for test_name, result, error in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if error:
            print(f"  Error: {error}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(tests)} tests")
    
    if passed == len(tests):
        print("All tests passed! The application should work correctly.")
    else:
        print("Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
