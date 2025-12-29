#!/bin/bash

# YouTube Auto Channel Backup Script
# ===================================

# Configuration
BACKUP_DIR="/backups/youtube_auto"
MAX_BACKUPS=30
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="youtube_auto_backup_$TIMESTAMP.tar.gz"
PROJECT_DIR=$(pwd)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

check_dependencies() {
    log_info "Checking dependencies..."
    
    # Check for tar
    if ! command -v tar &> /dev/null; then
        log_error "tar command not found!"
        exit 1
    fi
    
    # Check for rsync
    if ! command -v rsync &> /dev/null; then
        log_warn "rsync not found, using cp instead"
        USE_RSYNC=false
    else
        USE_RSYNC=true
    fi
}

create_backup() {
    log_info "Creating backup: $BACKUP_NAME"
    
    # Create temporary directory
    TEMP_DIR="/tmp/backup_$TIMESTAMP"
    mkdir -p "$TEMP_DIR"
    
    # List of directories to backup
    DIRS_TO_BACKUP=(
        "config"
        "core"
        "services"
        "utils"
        "database"
        "assets/local_images"
        "assets/local_audio"
        "assets/backgrounds"
        "assets/templates"
    )
    
    # List of files to backup
    FILES_TO_BACKUP=(
        "main.py"
        "requirements.txt"
        ".env"
        "run_daily.sh"
        "backup_script.sh"
        "README.md"
    )
    
    # Copy directories
    for dir in "${DIRS_TO_BACKUP[@]}"; do
        if [ -d "$PROJECT_DIR/$dir" ]; then
            log_info "Backing up directory: $dir"
            mkdir -p "$TEMP_DIR/$dir"
            
            if [ "$USE_RSYNC" = true ]; then
                rsync -av "$PROJECT_DIR/$dir/" "$TEMP_DIR/$dir/" --exclude="*.tmp" --exclude="*.log"
            else
                cp -r "$PROJECT_DIR/$dir/." "$TEMP_DIR/$dir/" 2>/dev/null
            fi
        else
            log_warn "Directory not found: $dir"
        fi
    done
    
    # Copy files
    for file in "${FILES_TO_BACKUP[@]}"; do
        if [ -f "$PROJECT_DIR/$file" ]; then
            log_info "Backing up file: $file"
            cp "$PROJECT_DIR/$file" "$TEMP_DIR/"
        else
            log_warn "File not found: $file"
        fi
    done
    
    # Create database dump
    if [ -f "$PROJECT_DIR/database/youtube_auto.db" ]; then
        log_info "Backing up database..."
        sqlite3 "$PROJECT_DIR/database/youtube_auto.db" ".dump" > "$TEMP_DIR/database_dump.sql"
    fi
    
    # Create backup info file
    cat > "$TEMP_DIR/backup_info.txt" << EOF
Backup Information
==================
Backup Name: $BACKUP_NAME
Timestamp: $(date)
Project Directory: $PROJECT_DIR
System: $(uname -a)

Included Directories:
$(printf '%s\n' "${DIRS_TO_BACKUP[@]}")

Included Files:
$(printf '%s\n' "${FILES_TO_BACKUP[@]}")

Database Size: $(du -h "$PROJECT_DIR/database/youtube_auto.db" 2>/dev/null | cut -f1)
Total Size: $(du -sh "$TEMP_DIR" 2>/dev/null | cut -f1)
EOF
    
    # Create archive
    log_info "Creating archive..."
    mkdir -p "$BACKUP_DIR"
    tar -czf "$BACKUP_DIR/$BACKUP_NAME" -C /tmp "backup_$TIMESTAMP"
    
    # Cleanup
    rm -rf "$TEMP_DIR"
    
    # Verify backup
    if [ -f "$BACKUP_DIR/$BACKUP_NAME" ]; then
        BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_NAME" | cut -f1)
        log_info "Backup created successfully: $BACKUP_NAME ($BACKUP_SIZE)"
    else
        log_error "Backup creation failed!"
        exit 1
    fi
}

clean_old_backups() {
    log_info "Cleaning old backups (keeping last $MAX_BACKUPS)..."
    
    # Count backups
    BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/*.tar.gz 2>/dev/null | wc -l)
    
    if [ "$BACKUP_COUNT" -gt "$MAX_BACKUPS" ]; then
        # Sort by date and remove oldest
        ls -1t "$BACKUP_DIR"/*.tar.gz | tail -n +$((MAX_BACKUPS + 1)) | while read backup; do
            log_info "Removing old backup: $(basename "$backup")"
            rm -f "$backup"
        done
    else
        log_info "No old backups to clean ($BACKUP_COUNT/$MAX_BACKUPS)"
    fi
}

restore_backup() {
    local BACKUP_FILE="$1"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        log_error "Backup file not found: $BACKUP_FILE"
        exit 1
    fi
    
    log_info "Restoring from backup: $(basename "$BACKUP_FILE")"
    
    # Ask for confirmation
    read -p "Are you sure you want to restore this backup? This will overwrite current files. (y/n): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        log_info "Restore cancelled"
        exit 0
    fi
    
    # Create restore directory
    RESTORE_DIR="/tmp/restore_$TIMESTAMP"
    mkdir -p "$RESTORE_DIR"
    
    # Extract backup
    log_info "Extracting backup..."
    tar -xzf "$BACKUP_FILE" -C "$RESTORE_DIR"
    
    # Restore files
    log_info "Restoring files..."
    
    # Restore directories
    for dir in config core services utils; do
        if [ -d "$RESTORE_DIR/backup_$TIMESTAMP/$dir" ]; then
            log_info "Restoring directory: $dir"
            rm -rf "$PROJECT_DIR/$dir"
            cp -r "$RESTORE_DIR/backup_$TIMESTAMP/$dir" "$PROJECT_DIR/"
        fi
    done
    
    # Restore database
    if [ -f "$RESTORE_DIR/backup_$TIMESTAMP/database_dump.sql" ]; then
        log_info "Restoring database..."
        rm -f "$PROJECT_DIR/database/youtube_auto.db"
        sqlite3 "$PROJECT_DIR/database/youtube_auto.db" < "$RESTORE_DIR/backup_$TIMESTAMP/database_dump.sql"
    fi
    
    # Restore individual files
    for file in main.py requirements.txt .env run_daily.sh; do
        if [ -f "$RESTORE_DIR/backup_$TIMESTAMP/$file" ]; then
            log_info "Restoring file: $file"
            cp "$RESTORE_DIR/backup_$TIMESTAMP/$file" "$PROJECT_DIR/"
        fi
    done
    
    # Cleanup
    rm -rf "$RESTORE_DIR"
    
    log_info "Restore completed successfully!"
}

list_backups() {
    log_info "Available backups in $BACKUP_DIR:"
    echo ""
    
    ls -1t "$BACKUP_DIR"/*.tar.gz 2>/dev/null | while read backup; do
        backup_name=$(basename "$backup")
        backup_date=$(echo "$backup_name" | grep -o '[0-9]\{8\}_[0-9]\{6\}')
        formatted_date=$(echo "$backup_date" | sed 's/\([0-9]\{4\}\)\([0-9]\{2\}\)\([0-9]\{2\}\)_\([0-9]\{2\}\)\([0-9]\{2\}\)\([0-9]\{2\}\)/\1-\2-\3 \4:\5:\6/')
        backup_size=$(du -h "$backup" | cut -f1)
        
        echo -e "  ${GREEN}$backup_name${NC}"
        echo -e "    Date: $formatted_date"
        echo -e "    Size: $backup_size"
        echo ""
    done
}

show_usage() {
    echo "YouTube Auto Channel Backup Script"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  create     Create a new backup"
    echo "  list       List available backups"
    echo "  restore    Restore from backup (requires filename)"
    echo "  auto       Create backup and clean old ones"
    echo "  help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 create"
    echo "  $0 list"
    echo "  $0 restore /backups/youtube_auto/backup_20231215_143022.tar.gz"
}

# Main execution
case "$1" in
    "create")
        check_dependencies
        create_backup
        ;;
    "list")
        list_backups
        ;;
    "restore")
        if [ -z "$2" ]; then
            log_error "Please specify backup file to restore"
            show_usage
            exit 1
        fi
        restore_backup "$2"
        ;;
    "auto")
        check_dependencies
        create_backup
        clean_old_backups
        ;;
    "help"|"")
        show_usage
        ;;
    *)
        log_error "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac
