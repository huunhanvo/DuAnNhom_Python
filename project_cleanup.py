#!/usr/bin/env python3
"""
Script to automatically clean up unnecessary files in the barbershop project
"""

import os
import shutil
from pathlib import Path

def cleanup_files():
    """Clean up unnecessary files"""
    print("🧹 Starting cleanup process...\n")
    
    # Files to remove (specific files)
    files_to_remove = [
        # Test and debug files
        "test_admin_login.py",
        "test_avatar_display.py", 
        "test_avatar_views.py",
        "test_booking_data.py",
        "test_create_voucher.py",
        "test_db.py",
        "test_direct_view.py",
        "test_filter_requests.py",
        "test_password_hash.py",
        "test_profile.py",
        "test_profile_functionality.py",
        "test_reports_data.py",
        "test_reports_page.py",
        "test_reviews_view.py",
        "test_view.py",
        "test_voucher_direct.py",
        "debug_avatar.py",
        "debug_date_filter.py",
        "debug_new_trend.py", 
        "debug_trend.py",
        "check_all_passwords.py",
        "check_dates.py",
        "check_null_bytes.py",
        "check_password.py",
        "check_password_hash.py",
        "check_reviews_data.py",
        "check_table_structure.py",
        
        # Test HTML files
        "test_edit_button.html",
        "test_filter_js.html",
        "test_login.html",
        "test_reviews_js.html",
        "direct_button_test.html",
        "simple_test.html",
        
        # Temporary files
        "temp_my_customers.py",
        "clean_null_bytes.py",
        "schedule_api_endpoints.py",
        "schedule_endpoints.py",
        "cleanup_analysis.py",  # This script itself
        
        # Backup files
        "barbershop/views_backup.py",
        "update_passwords.py",
        "update_views.py",
        "fix_dich_vu_fields.py",
        "fix_fields.py", 
        "fix_hoadon.py",
        "fix_invalid_passwords.py",
        "fix_lich_lam_viec.py",
        "fix_service_status.py",
        "drop_old_table.py",
        "final_profile_check.py",
        
        # Database migration files (keep only the important ones)
        "create_admin.py",
        "create_sample_bookings.py",
        "create_sample_reviews.py",
        "create_template.py",
        "them_du_lieu.sql",
        "DB_quan_ly_barbershop.sql",
        
        # Templates to remove
        "templates/test_avatar.html",
    ]
    
    # Directories to remove entirely
    dirs_to_remove = [
        "__pycache__",
        "barbershop/__pycache__",
        "barbershop/migrations/__pycache__",
    ]
    
    removed_files = []
    removed_dirs = []
    
    # Remove files
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                removed_files.append(file_path)
                print(f"✅ Removed: {file_path}")
            except Exception as e:
                print(f"❌ Failed to remove {file_path}: {e}")
        else:
            print(f"⚠️  Not found: {file_path}")
    
    # Remove directories
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            try:
                shutil.rmtree(dir_path)
                removed_dirs.append(dir_path)
                print(f"✅ Removed directory: {dir_path}")
            except Exception as e:
                print(f"❌ Failed to remove directory {dir_path}: {e}")
    
    print(f"\n📊 CLEANUP SUMMARY:")
    print(f"Files removed: {len(removed_files)}")
    print(f"Directories removed: {len(removed_dirs)}")
    
    return removed_files, removed_dirs

def create_gitignore():
    """Create comprehensive .gitignore file"""
    print("\n📝 Creating .gitignore file...")
    
    gitignore_content = """# Python
__pycache__/**
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
ENV/
.env

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Media files (uploaded by users)
media/

# Static files (collected)
staticfiles/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp
temp_*
test_*
debug_*
check_*
fix_*
cleanup_*

# Backup files
*_backup.*
*.bak

# Documentation drafts
DRAFT_*
TODO_*
"""
    
    try:
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore file")
        return True
    except Exception as e:
        print(f"❌ Failed to create .gitignore: {e}")
        return False

if __name__ == "__main__":
    removed_files, removed_dirs = cleanup_files()
    create_gitignore()
    
    print("\n🎉 Cleanup completed!")
    print("\n📋 REMAINING ESSENTIAL FILES:")
    print("✅ manage.py - Django management")
    print("✅ db.sqlite3 - Database")
    print("✅ barbershop/ - Main application")
    print("✅ templates/ - HTML templates")
    print("✅ static/ - CSS, JS, images")
    print("✅ media/ - User uploads")
    print("✅ *.pdf - Documentation")
    print("✅ .git/ - Version control")