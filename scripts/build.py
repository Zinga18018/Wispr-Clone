#!/usr/bin/env python3
"""
WisprClone Build Script

This script builds distributable packages for WisprClone.
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path


def run_command(command, description="", check=True):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}...")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False


def clean_build_dirs():
    """Clean build directories"""
    print("🧹 Cleaning build directories...")
    
    project_root = Path(__file__).parent.parent
    clean_dirs = ["build", "dist", "*.egg-info"]
    
    for pattern in clean_dirs:
        for path in project_root.glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"   Removed: {path}")
            elif path.is_file():
                path.unlink()
                print(f"   Removed: {path}")


def build_wheel():
    """Build wheel package"""
    print("\n📦 Building wheel package...")
    
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    return run_command(
        f"{sys.executable} -m build --wheel",
        "Building wheel"
    )


def build_source():
    """Build source distribution"""
    print("\n📦 Building source distribution...")
    
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    return run_command(
        f"{sys.executable} -m build --sdist",
        "Building source distribution"
    )


def build_executable():
    """Build standalone executable using PyInstaller"""
    print("\n🔧 Building standalone executable...")
    
    try:
        import PyInstaller
    except ImportError:
        print("📦 Installing PyInstaller...")
        if not run_command(f"{sys.executable} -m pip install pyinstaller", "Installing PyInstaller"):
            return False
    
    project_root = Path(__file__).parent.parent
    
    # Create PyInstaller spec
    spec_content = f'''
# WisprClone PyInstaller spec file

import sys
from pathlib import Path

block_cipher = None

# Get project root
project_root = Path(__file__).parent

a = Analysis(
    ['{project_root}/wisprclone/main.py'],
    pathex=['{project_root}'],
    binaries=[],
    datas=[
        ('{project_root}/wisprclone', 'wisprclone'),
        ('{project_root}/requirements.txt', '.'),
        ('{project_root}/README.md', '.'),
        ('{project_root}/LICENSE', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'tkinter',
        'whisper',
        'torch',
        'torchaudio',
        'sounddevice',
        'soundfile',
        'pyaudio',
        'keyboard',
        'pyperclip',
        'scipy',
        'librosa',
        'noisereduce',
        'numpy',
        'PIL',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='wisprclone',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if available
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='wisprclone',
)
'''
    
    spec_path = project_root / "wisprclone.spec"
    spec_path.write_text(spec_content)
    
    # Build executable
    return run_command(
        f"pyinstaller wisprclone.spec --clean",
        "Building executable with PyInstaller"
    )


def create_installer():
    """Create platform-specific installer"""
    system = platform.system().lower()
    
    if system == "windows":
        create_windows_installer()
    elif system == "darwin":
        create_macos_installer()
    elif system == "linux":
        create_linux_installer()


def create_windows_installer():
    """Create Windows installer using NSIS or Inno Setup"""
    print("\n💾 Creating Windows installer...")
    
    # This would require NSIS or Inno Setup to be installed
    print("📝 To create Windows installer:")
    print("   1. Install NSIS (https://nsis.sourceforge.io/)")
    print("   2. Create installer script")
    print("   3. Compile with makensis")


def create_macos_installer():
    """Create macOS app bundle and DMG"""
    print("\n🍎 Creating macOS installer...")
    
    # This would use py2app or similar
    print("📝 To create macOS installer:")
    print("   1. Install py2app: pip install py2app")
    print("   2. Create setup.py for py2app")
    print("   3. Build app bundle: python setup.py py2app")
    print("   4. Create DMG with hdiutil")


def create_linux_installer():
    """Create Linux packages (deb, rpm, AppImage)"""
    print("\n🐧 Creating Linux packages...")
    
    # AppImage creation
    try:
        print("📦 Creating AppImage...")
        # This would require appimage-builder or similar tools
        print("📝 To create AppImage:")
        print("   1. Install appimage-builder")
        print("   2. Create AppImageBuilder.yml")
        print("   3. Build with appimage-builder")
        
    except Exception as e:
        print(f"⚠️  AppImage creation failed: {e}")


def run_tests():
    """Run tests before building"""
    print("\n🧪 Running tests...")
    
    project_root = Path(__file__).parent.parent
    
    # Check if pytest is available
    try:
        import pytest
        test_command = "pytest tests/ -v"
    except ImportError:
        print("📦 Installing pytest...")
        run_command(f"{sys.executable} -m pip install pytest", "Installing pytest")
        test_command = f"{sys.executable} -m pytest tests/ -v"
    
    # Run tests if test directory exists
    test_dir = project_root / "tests"
    if test_dir.exists():
        return run_command(test_command, "Running tests")
    else:
        print("⚠️  No tests directory found, skipping tests")
        return True


def check_build_requirements():
    """Check if build requirements are met"""
    print("🔍 Checking build requirements...")
    
    # Check for build package
    try:
        import build
    except ImportError:
        print("📦 Installing build package...")
        if not run_command(f"{sys.executable} -m pip install build", "Installing build"):
            return False
    
    # Check for wheel package
    try:
        import wheel
    except ImportError:
        print("📦 Installing wheel package...")
        if not run_command(f"{sys.executable} -m pip install wheel", "Installing wheel"):
            return False
    
    return True


def upload_to_pypi():
    """Upload package to PyPI"""
    print("\n📤 Uploading to PyPI...")
    
    # Check for twine
    try:
        import twine
    except ImportError:
        print("📦 Installing twine...")
        if not run_command(f"{sys.executable} -m pip install twine", "Installing twine"):
            return False
    
    # Upload to PyPI
    print("⚠️  Make sure you have PyPI credentials configured!")
    choice = input("Upload to PyPI? (y/N): ").lower()
    
    if choice == 'y':
        return run_command(
            f"{sys.executable} -m twine upload dist/*",
            "Uploading to PyPI"
        )
    else:
        print("📝 To upload later, run: python -m twine upload dist/*")
        return True


def main():
    """Main build function"""
    print("🔨 WisprClone Build Script")
    print("=" * 30)
    
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser(description="Build WisprClone packages")
    parser.add_argument("--wheel", action="store_true", help="Build wheel package")
    parser.add_argument("--source", action="store_true", help="Build source distribution")
    parser.add_argument("--executable", action="store_true", help="Build standalone executable")
    parser.add_argument("--installer", action="store_true", help="Create platform-specific installer")
    parser.add_argument("--all", action="store_true", help="Build all packages")
    parser.add_argument("--upload", action="store_true", help="Upload to PyPI")
    parser.add_argument("--no-tests", action="store_true", help="Skip tests")
    parser.add_argument("--clean", action="store_true", help="Clean build directories")
    
    args = parser.parse_args()
    
    # Clean if requested
    if args.clean:
        clean_build_dirs()
        if not any([args.wheel, args.source, args.executable, args.installer, args.all]):
            return
    
    # Check build requirements
    if not check_build_requirements():
        print("❌ Build requirements not met")
        sys.exit(1)
    
    # Run tests unless skipped
    if not args.no_tests:
        if not run_tests():
            print("❌ Tests failed")
            choice = input("Continue building anyway? (y/N): ").lower()
            if choice != 'y':
                sys.exit(1)
    
    # Clean build directories
    clean_build_dirs()
    
    # Build packages
    success = True
    
    if args.all or args.wheel:
        success &= build_wheel()
    
    if args.all or args.source:
        success &= build_source()
    
    if args.all or args.executable:
        success &= build_executable()
    
    if args.all or args.installer:
        create_installer()
    
    # Upload if requested
    if args.upload and success:
        upload_to_pypi()
    
    # Default: build wheel and source
    if not any([args.wheel, args.source, args.executable, args.installer, args.all]):
        success &= build_wheel()
        success &= build_source()
    
    # Summary
    if success:
        print("\n" + "=" * 40)
        print("🎉 Build completed successfully!")
        print("=" * 40)
        
        dist_dir = Path(__file__).parent.parent / "dist"
        if dist_dir.exists():
            print(f"\n📦 Built packages in {dist_dir}:")
            for file in dist_dir.iterdir():
                if file.is_file():
                    print(f"   {file.name}")
    else:
        print("\n❌ Build failed")
        sys.exit(1)


if __name__ == "__main__":
    main() 