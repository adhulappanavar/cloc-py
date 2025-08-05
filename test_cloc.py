#!/usr/bin/env python3
"""
Simple test for cloc-py
"""

import os
import tempfile
import subprocess
from pathlib import Path

def create_test_files():
    """Create test files for different languages"""
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    
    # Python file
    with open(test_dir / "test.py", "w") as f:
        f.write("""#!/usr/bin/env python3
# This is a comment
\"\"\"
This is a docstring
with multiple lines
\"\"\"

def hello_world():
    # Another comment
    print("Hello, World!")  # Inline comment
    
    return True

if __name__ == "__main__":
    hello_world()
""")
    
    # C++ file
    with open(test_dir / "test.cpp", "w") as f:
        f.write("""#include <iostream>

// This is a comment
/* This is a 
   multiline comment */

int main() {
    std::cout << "Hello, World!" << std::endl;  // Inline comment
    return 0;
}
""")
    
    # JavaScript file
    with open(test_dir / "test.js", "w") as f:
        f.write("""// This is a comment
/* This is a 
   multiline comment */

function helloWorld() {
    console.log("Hello, World!");  // Inline comment
    return true;
}

// Export the function
export default helloWorld;
""")
    
    # HTML file
    with open(test_dir / "test.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <!-- This is a comment -->
    <title>Test Page</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <!-- Another comment -->
    <script>
        // JavaScript comment
        console.log("Hello from script");
    </script>
</body>
</html>
""")
    
    # Shell script
    with open(test_dir / "test.sh", "w") as f:
        f.write("""#!/bin/bash
# This is a comment

echo "Hello, World!"  # Inline comment

# Function definition
hello_world() {
    echo "Hello from function"
}

hello_world
""")
    
    return test_dir

def test_cloc_py():
    """Test the cloc-py functionality"""
    print("Creating test files...")
    test_dir = create_test_files()
    
    print("\nTesting cloc-py on test files...")
    try:
        result = subprocess.run(
            ["python", "cloc_py.py", str(test_dir)],
            capture_output=True,
            text=True,
            check=True
        )
        print("✓ cloc-py ran successfully")
        print("\nOutput:")
        print(result.stdout)
        
        # Test JSON output
        result_json = subprocess.run(
            ["python", "cloc_py.py", str(test_dir), "--format", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        print("\n✓ JSON output works")
        
        # Test CSV output
        result_csv = subprocess.run(
            ["python", "cloc_py.py", str(test_dir), "--format", "csv"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✓ CSV output works")
        
        # Test by-file output
        result_by_file = subprocess.run(
            ["python", "cloc_py.py", str(test_dir), "--by-file"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✓ By-file output works")
        
        print("\n🎉 All tests passed!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Test failed: {e}")
        print(f"Error output: {e.stderr}")
    except FileNotFoundError:
        print("❌ cloc_py.py not found in current directory")
    finally:
        # Clean up
        import shutil
        if test_dir.exists():
            shutil.rmtree(test_dir)
            print("\nCleaned up test files")

if __name__ == "__main__":
    test_cloc_py() 