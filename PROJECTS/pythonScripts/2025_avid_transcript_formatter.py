#!/usr/bin/env python3
"""
Final Avid ScriptSync Formatter - ASCII with Margins
Streamlined version using the proven working solution:
- ASCII encoding
- CRLF line endings  
- 60-character margins technique
"""

import re
import os
import sys

def format_for_avid_scriptsync(input_file):
    """
    Format transcript using ASCII encoding, CRLF line endings, and 60-character margins
    This is the proven working solution for Avid ScriptSync line indexing
    
    Args:
        input_file (str): Path to input transcript file
    
    Returns:
        str: Path to the output file if successful, None if failed
    """
    
    # Generate output filename in the same directory
    directory = os.path.dirname(input_file)
    filename = os.path.basename(input_file)
    name, ext = os.path.splitext(filename)
    output_file = os.path.join(directory, f"{name}_ascii{ext}")
    
    try:
        # Read the original file
        with open(input_file, 'r', encoding='utf-8', newline=None) as f:
            content = f.read()
        
        # Normalize line endings
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        lines = content.split('\n')
        
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Empty lines - preserve them (helps with indexing)
            if not line:
                formatted_lines.append('')
                continue
            
            # Check for speaker/timestamp patterns - keep these intact
            speaker_pattern = r'^[A-Z_0-9]+\s*\([0-9:.-]+\):\s*$'
            timestamp_pattern = r'^[0-9:.-]+\s*$'
            
            if re.match(speaker_pattern, line) or re.match(timestamp_pattern, line):
                formatted_lines.append(line)
                continue
            
            # Apply "wide margins" technique - break at 60 characters
            if len(line) <= 60:
                formatted_lines.append(line)
            else:
                # Split at word boundaries near the 60-character limit
                words = line.split()
                current_line = ""
                
                for word in words:
                    test_line = f"{current_line} {word}".strip() if current_line else word
                    
                    if len(test_line) <= 60:
                        current_line = test_line
                    else:
                        if current_line:
                            formatted_lines.append(current_line)
                        current_line = word
                
                if current_line:
                    formatted_lines.append(current_line)
        
        # Write with ASCII encoding and CRLF line endings
        with open(output_file, 'w', encoding='ascii', errors='replace', newline='') as f:
            for i, line in enumerate(formatted_lines):
                # Handle non-ASCII characters by replacing them
                clean_line = line.encode('ascii', errors='replace').decode('ascii')
                f.write(clean_line)
                # Add CRLF line ending after each line except the last
                if i < len(formatted_lines) - 1:
                    f.write('\r\n')
        
        return output_file
        
    except Exception as e:
        raise Exception(f"Error processing file: {str(e)}")

def get_file_path():
    """
    Get the file path from user input with validation
    """
    print("=" * 60)
    print("        AVID SCRIPTSYNC FORMATTER")
    print("=" * 60)
    print("ASCII encoding + 60-character margins for optimal line indexing")
    print()
    
    while True:
        file_path = input("Enter the full path to your transcript file: ").strip()
        
        # Remove quotes if user included them
        file_path = file_path.strip('"\'')
        
        if not file_path:
            print("❌ Please enter a file path.")
            continue
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            print("   Please check the path and try again.")
            continue
        
        if not file_path.lower().endswith('.txt'):
            confirm = input(f"⚠️  File doesn't end with .txt - continue anyway? (y/n): ").strip().lower()
            if confirm not in ['y', 'yes']:
                continue
        
        return file_path

def main():
    """Main function"""
    
    # Check if file was provided as command line argument
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if not os.path.exists(input_file):
            print(f"❌ Error: File '{input_file}' not found.")
            sys.exit(1)
    else:
        # Interactive mode - get file path from user
        input_file = get_file_path()
    
    try:
        print(f"\n🔄 Processing: {os.path.basename(input_file)}")
        print("   Using ASCII encoding + 60-character margins...")
        
        output_file = format_for_avid_scriptsync(input_file)
        
        print(f"\n✅ Success!")
        print(f"📄 Original file: {os.path.basename(input_file)}")
        print(f"📄 Formatted file: {os.path.basename(output_file)}")
        print(f"📁 Location: {os.path.dirname(output_file)}")
        print()
        print("🎬 Your transcript is ready for Avid ScriptSync!")
        print("   Each line should now be indexed individually in Avid.")
        
        # Ask if user wants to process another file
        while True:
            another = input("\nProcess another file? (y/n): ").strip().lower()
            if another in ['y', 'yes']:
                print()
                input_file = get_file_path()
                print(f"\n🔄 Processing: {os.path.basename(input_file)}")
                output_file = format_for_avid_scriptsync(input_file)
                print(f"✅ Created: {os.path.basename(output_file)}")
            elif another in ['n', 'no']:
                print("\n👋 Done! Happy editing!")
                break
            else:
                print("Please enter 'y' or 'n'")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
