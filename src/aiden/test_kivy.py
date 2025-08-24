#!/usr/bin/env python3
"""
Kivy Test and Setup Script
This script tests if Kivy is installed and working properly.
If not installed, it provides installation instructions.
"""

import sys
import os
import subprocess
import platform


def check_python_version():
    """Check if Python version is compatible with Kivy"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python {version.major}.{version.minor} is not supported by Kivy.")
        print("📋 Kivy requires Python 3.7 or higher.")
        return False

    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible with Kivy.")
    return True


def test_kivy_import():
    """Test if Kivy can be imported"""
    try:
        import kivy
        print(f"✅ Kivy is installed! Version: {kivy.__version__}")
        return True
    except ImportError:
        print("❌ Kivy is not installed.")
        return False


def test_kivy_basic_functionality():
    """Test basic Kivy functionality"""
    try:
        from kivy.app import App
        from kivy.uix.label import Label
        from kivy.config import Config

        # Configure Kivy to prevent window from opening during test
        Config.set('graphics', 'width', '100')
        Config.set('graphics', 'height', '100')
        Config.set('graphics', 'borderless', '1')
        Config.set('graphics', 'window_state', 'hidden')

        print("✅ Basic Kivy imports successful.")

        # Test widget creation
        label = Label(text='Test')
        print("✅ Widget creation successful.")

        return True

    except Exception as e:
        print(f"❌ Kivy functionality test failed: {e}")
        return False


def install_kivy():
    """Attempt to install Kivy"""
    system = platform.system().lower()

    print("🔧 Attempting to install Kivy...")

    commands = []

    if system == "windows":
        commands = [
            [sys.executable, "-m", "pip", "install", "kivy[base]"],
            [sys.executable, "-m", "pip", "install", "kivy"]
        ]
    elif system == "darwin":  # macOS
        commands = [
            [sys.executable, "-m", "pip", "install", "kivy"],
            [sys.executable, "-m", "pip", "install", "kivy[base]"]
        ]
    else:  # Linux and others
        commands = [
            [sys.executable, "-m", "pip", "install", "kivy"],
            ["sudo", "apt-get", "install", "python3-kivy"]
        ]

    for i, cmd in enumerate(commands):
        try:
            print(f"🔄 Trying installation method {i+1}...")
            print(f"   Command: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                print("✅ Installation successful!")
                return True
            else:
                print(f"❌ Installation failed with code {result.returncode}")
                if result.stderr:
                    print(f"   Error: {result.stderr[:200]}")

        except subprocess.TimeoutExpired:
            print("⏱️ Installation timed out")
        except FileNotFoundError:
            print(f"❌ Command not found: {cmd[0]}")
        except Exception as e:
            print(f"❌ Installation error: {e}")

    return False


def show_manual_installation_instructions():
    """Show manual installation instructions"""
    system = platform.system().lower()

    print("\n" + "="*60)
    print("📚 MANUAL INSTALLATION INSTRUCTIONS")
    print("="*60)

    print("\n🔧 Basic Installation:")
    print("   pip install kivy")

    if system == "windows":
        print("\n🪟 Windows Specific:")
        print("   pip install kivy[base]")
        print("   # Or with media support:")
        print("   pip install kivy[base,media]")
        print("\n   If you have issues, try:")
        print("   python -m pip install --upgrade pip wheel setuptools")
        print("   python -m pip install kivy[base] --no-deps")

    elif system == "darwin":
        print("\n🍎 macOS Specific:")
        print("   # Install dependencies first (if using Homebrew):")
        print("   brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer")
        print("   pip install kivy")
        print("\n   # For Apple Silicon Macs:")
        print("   pip install kivy[base] --no-binary kivy")

    else:
        print("\n🐧 Linux Specific:")
        print("   # Install system dependencies first:")
        print("   sudo apt update")
        print("   sudo apt install python3-kivy")
        print("\n   # Or install via pip:")
        print("   sudo apt install python3-dev python3-setuptools")
        print("   sudo apt install ffmpeg libsdl2-dev libsdl2-image-dev")
        print("   pip install kivy")

    print("\n🌐 Virtual Environment (Recommended):")
    print("   python -m venv kivy_env")
    if system == "windows":
        print("   kivy_env\\Scripts\\activate")
    else:
        print("   source kivy_env/bin/activate")
    print("   pip install kivy")

    print("\n📖 For more help, visit: https://kivy.org/doc/stable/gettingstarted/installation.html")


def run_simple_kivy_test():
    """Run a simple Kivy application test"""
    try:
        print("\n🧪 Running simple Kivy application test...")

        # Import required modules
        from kivy.app import App
        from kivy.uix.label import Label
        from kivy.config import Config

        # Configure for testing
        Config.set('graphics', 'width', '400')
        Config.set('graphics', 'height', '300')
        Config.set('graphics', 'resizable', '0')

        class TestApp(App):
            def build(self):
                return Label(
                    text='Kivy Test Successful!\nClose this window to continue.',
                    font_size='18sp',
                    halign='center'
                )

        print("✅ Test app created successfully.")
        print("📱 A test window should open shortly...")
        print("   Close the window to continue the test.")

        # Run the test app
        TestApp().run()

        print("✅ Kivy application test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Kivy application test failed: {e}")
        return False


def main():
    """Main test function"""
    print("🚀 Kivy Installation and Functionality Test")
    print("="*50)

    # Check Python version
    if not check_python_version():
        return 1

    print()

    # Test if Kivy is installed
    kivy_installed = test_kivy_import()

    if not kivy_installed:
        print("\n🔧 Kivy is not installed. Attempting automatic installation...")

        # Try to install automatically
        if install_kivy():
            print("\n🔄 Testing installation...")
            if test_kivy_import():
                kivy_installed = True
            else:
                print("❌ Installation verification failed.")

        if not kivy_installed:
            show_manual_installation_instructions()
            return 1

    print()

    # Test basic functionality
    if not test_kivy_basic_functionality():
        print("❌ Basic functionality test failed.")
        print("💡 Try reinstalling Kivy or check the installation guide.")
        return 1

    # Ask user if they want to run the visual test
    print("\n🎯 Basic tests passed!")

    try:
        response = input("\n❓ Run visual test? (opens a window) [y/N]: ").strip().lower()
        if response in ['y', 'yes']:
            if not run_simple_kivy_test():
                return 1
        else:
            print("⏭️ Skipping visual test.")
    except KeyboardInterrupt:
        print("\n⏭️ Visual test skipped.")

    # Final success message
    print("\n" + "="*50)
    print("🎉 ALL TESTS PASSED!")
    print("✅ Kivy is properly installed and working.")
    print("🚀 You can now run the Kivy examples:")
    print("   python kivy_hello.py")
    print("   python kivy_simple.py")
    print("   python kivy_counter.py")
    print("   python kivy_form.py")
    print("   python kivy_game.py")
    print("="*50)

    return 0


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
