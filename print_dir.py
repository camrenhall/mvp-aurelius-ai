#!/usr/bin/env python3
"""
Project Structure Enumerator
Recursively prints the directory structure of a Python project.
"""

import os
import sys
from pathlib import Path

def print_tree(directory, prefix="", max_depth=None, current_depth=0, show_hidden=False):
    """
    Recursively print directory structure in tree format.
    
    Args:
        directory: Path to the directory to enumerate
        prefix: Current prefix for tree formatting
        max_depth: Maximum depth to traverse (None for unlimited)
        current_depth: Current recursion depth
        show_hidden: Whether to show hidden files/directories
    """
    if max_depth is not None and current_depth >= max_depth:
        return
    
    try:
        # Get all items in directory
        items = list(Path(directory).iterdir())
        
        # Filter out hidden files if requested
        if not show_hidden:
            items = [item for item in items if not item.name.startswith('.')]
        
        # Sort items: directories first, then files
        items.sort(key=lambda x: (x.is_file(), x.name.lower()))
        
        for i, item in enumerate(items):
            # Determine if this is the last item
            is_last = i == len(items) - 1
            
            # Choose appropriate tree characters
            if is_last:
                current_prefix = "└── "
                next_prefix = prefix + "    "
            else:
                current_prefix = "├── "
                next_prefix = prefix + "│   "
            
            # Print current item
            if item.is_dir():
                print(f"{prefix}{current_prefix}{item.name}/")
                # Recursively print subdirectory
                print_tree(item, next_prefix, max_depth, current_depth + 1, show_hidden)
            else:
                # Add file size for files
                try:
                    size = item.stat().st_size
                    size_str = format_size(size)
                    print(f"{prefix}{current_prefix}{item.name} ({size_str})")
                except (OSError, PermissionError):
                    print(f"{prefix}{current_prefix}{item.name}")
    
    except PermissionError:
        print(f"{prefix}[Permission Denied]")
    except Exception as e:
        print(f"{prefix}[Error: {e}]")

def format_size(size_bytes):
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def main():
    """Main function to run the project structure enumerator."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Enumerate and print Python project structure recursively"
    )
    parser.add_argument(
        "path", 
        nargs="?", 
        default=".", 
        help="Path to the project directory (default: current directory)"
    )
    parser.add_argument(
        "--max-depth", 
        "-d", 
        type=int, 
        help="Maximum depth to traverse"
    )
    parser.add_argument(
        "--show-hidden", 
        "-a", 
        action="store_true", 
        help="Show hidden files and directories"
    )
    parser.add_argument(
        "--no-size", 
        action="store_true", 
        help="Don't show file sizes"
    )
    
    args = parser.parse_args()
    
    # Validate path
    project_path = Path(args.path)
    if not project_path.exists():
        print(f"Error: Path '{args.path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    if not project_path.is_dir():
        print(f"Error: Path '{args.path}' is not a directory.", file=sys.stderr)
        sys.exit(1)
    
    # Print header
    abs_path = project_path.resolve()
    print(f"Project Structure: {abs_path}")
    print("=" * 50)
    print(f"{abs_path.name}/")
    
    # Print the tree structure
    print_tree(
        project_path, 
        max_depth=args.max_depth, 
        show_hidden=args.show_hidden
    )
    
    # Print summary
    print("\n" + "=" * 50)
    try:
        total_files = sum(1 for _ in project_path.rglob('*') if _.is_file())
        total_dirs = sum(1 for _ in project_path.rglob('*') if _.is_dir())
        print(f"Total: {total_dirs} directories, {total_files} files")
    except Exception:
        print("Summary: Unable to calculate totals")

if __name__ == "__main__":
    main()