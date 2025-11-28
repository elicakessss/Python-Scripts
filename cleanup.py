import os
import shutil
import sys
from pathlib import Path

def get_temp_folders():
    """
    Returns list of common temp folders based on OS.
    """
    if sys.platform == "win32":
        return [
            os.path.expandvars(r"%TEMP%"),
            os.path.expandvars(r"%LOCALAPPDATA%\Temp"),
            os.path.expandvars(r"%WINDIR%\Temp"),
        ]
    else:  # Linux/Mac
        return [
            "/tmp",
            os.path.expanduser("~/.cache"),
        ]

def get_folder_size(path):
    """
    Calculate total size of a folder in MB.
    """
    try:
        total = sum(f.stat().st_size for f in Path(path).rglob('*') if f.is_file())
        return total / (1024 * 1024)  # Convert to MB
    except:
        return 0

def cleanup_folder(folder_path, dry_run=True):
    """
    Delete files and folders in the specified directory.
    """
    deleted_count = 0
    deleted_size = 0
    skipped_count = 0
    
    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            
            try:
                size = get_folder_size(item_path) if os.path.isdir(item_path) else os.path.getsize(item_path) / (1024 * 1024)
                
                if dry_run:
                    print(f"  [DRY RUN] Would delete: {item} ({size:.2f} MB)")
                else:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                    print(f"  ✓ Deleted: {item} ({size:.2f} MB)")
                
                deleted_count += 1
                deleted_size += size
                
            except PermissionError:
                print(f"  ✗ Permission denied: {item}")
                skipped_count += 1
            except Exception as e:
                print(f"  ✗ Error deleting {item}: {e}")
                skipped_count += 1
    
    except Exception as e:
        print(f"✗ Error accessing folder: {e}")
        return 0, 0, 0
    
    return deleted_count, deleted_size, skipped_count

def main():
    print("File Cleanup Utility")
    print("=" * 50)
    print()
    
    temp_folders = get_temp_folders()
    
    print("Available temp folders:")
    for i, folder in enumerate(temp_folders, 1):
        if os.path.exists(folder):
            size = get_folder_size(folder)
            print(f"  {i}. {folder} ({size:.2f} MB)")
        else:
            print(f"  {i}. {folder} (NOT FOUND)")
    
    print()
    print("Options:")
    print("  1. Cleanup specific folder")
    print("  2. Cleanup all temp folders")
    print("  3. Custom folder path")
    print("  0. Exit")
    print()
    
    choice = input("Enter your choice (0-3): ").strip()
    
    if choice == "0":
        print("Exiting...")
        sys.exit(0)
    elif choice == "1":
        try:
            folder_idx = int(input("Enter folder number: ")) - 1
            if 0 <= folder_idx < len(temp_folders):
                target_folder = temp_folders[folder_idx]
            else:
                print("✗ Invalid selection!")
                sys.exit(1)
        except ValueError:
            print("✗ Invalid input!")
            sys.exit(1)
    elif choice == "2":
        target_folder = None
    elif choice == "3":
        target_folder = input("Enter folder path: ").strip()
        if not os.path.exists(target_folder):
            print(f"✗ Folder not found: {target_folder}")
            sys.exit(1)
    else:
        print("✗ Invalid choice!")
        sys.exit(1)
    
    print()
    print("Running in DRY RUN mode first (no files deleted)...")
    print()
    
    if target_folder:
        print(f"Scanning: {target_folder}")
        count, size, skipped = cleanup_folder(target_folder, dry_run=True)
        print(f"\nWould delete: {count} items ({size:.2f} MB), Skipped: {skipped}")
    else:
        total_count = 0
        total_size = 0
        total_skipped = 0
        for folder in temp_folders:
            if os.path.exists(folder):
                print(f"\nScanning: {folder}")
                count, size, skipped = cleanup_folder(folder, dry_run=True)
                total_count += count
                total_size += size
                total_skipped += skipped
        print(f"\nTotal would delete: {total_count} items ({total_size:.2f} MB), Skipped: {total_skipped}")
    
    print()
    confirm = input("Proceed with actual cleanup? (yes/no): ").strip().lower()
    
    if confirm == "yes":
        print()
        print("Running actual cleanup...")
        print()
        
        if target_folder:
            count, size, skipped = cleanup_folder(target_folder, dry_run=False)
            print(f"\n✓ Cleanup complete! Deleted: {count} items ({size:.2f} MB), Skipped: {skipped}")
        else:
            total_count = 0
            total_size = 0
            total_skipped = 0
            for folder in temp_folders:
                if os.path.exists(folder):
                    print(f"Cleaning: {folder}")
                    count, size, skipped = cleanup_folder(folder, dry_run=False)
                    total_count += count
                    total_size += size
                    total_skipped += skipped
            print(f"\n✓ Cleanup complete! Total deleted: {total_count} items ({total_size:.2f} MB), Skipped: {total_skipped}")
    else:
        print("Cleanup cancelled.")

if __name__ == "__main__":
    main()