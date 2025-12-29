#!/bin/bash

# YouTube Auto Channel - Daily Runner Script
# ==========================================

# ألوان للمخرجات
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# دالة لعرض الرسائل
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# التحقق من وجود Python
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python not found! Please install Python 3.8 or higher."
        exit 1
    fi
    
    # التحقق من إصدار Python
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    print_info "Using Python $PYTHON_VERSION"
}

# التحقق من المتطلبات
check_requirements() {
    print_info "Checking requirements..."
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found!"
        exit 1
    fi
    
    # التحقق من تثبيت pip
    if ! command -v pip3 &> /dev/null; then
        if ! command -v pip &> /dev/null; then
            print_error "pip not found! Please install pip."
            exit 1
        else
            PIP_CMD="pip"
        fi
    else
        PIP_CMD="pip3"
    fi
    
    print_info "Using $PIP_CMD"
}

# تثبيت المتطلبات
install_requirements() {
    print_info "Installing requirements..."
    
    $PIP_CMD install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        print_success "Requirements installed successfully"
    else
        print_error "Failed to install requirements"
        exit 1
    fi
}

# التحقق من ملف البيئة
check_env() {
    print_info "Checking environment configuration..."
    
    if [ ! -f ".env" ]; then
        print_warning ".env file not found, creating from example..."
        
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_warning "Please edit .env file with your API keys"
            exit 1
        else
            print_error ".env.example not found!"
            exit 1
        fi
    else
        print_success ".env file found"
    fi
}

# إنشاء المجلدات المطلوبة
create_directories() {
    print_info "Creating required directories..."
    
    mkdir -p assets/backgrounds
    mkdir -p assets/local_images
    mkdir -p assets/local_audio
    mkdir -p assets/generated/images
    mkdir -p assets/generated/audio
    mkdir -p assets/generated/videos
    mkdir -p assets/generated/shorts
    mkdir -p assets/uploads
    mkdir -p database
    mkdir -p logs
    mkdir -p backups
    
    print_success "Directories created"
}

# تنظيف الملفات القديمة
cleanup_old_files() {
    print_info "Cleaning up old files..."
    
    # تنظيف الملفات المؤقتة الأقدم من 3 أيام
    find assets/generated -name "*.mp3" -mtime +3 -delete 2>/dev/null
    find assets/generated -name "*.jpg" -mtime +3 -delete 2>/dev/null
    find assets/generated -name "*.png" -mtime +3 -delete 2>/dev/null
    
    # تنظيف السجلات الأقدم من 7 أيام
    find logs -name "*.log" -mtime +7 -delete 2>/dev/null
    
    print_success "Cleanup completed"
}

# تشغيل النظام
run_system() {
    print_info "Starting YouTube Auto Channel..."
    
    local MODE="$1"
    
    case "$MODE" in
        "daily")
            print_info "Running daily pipeline..."
            $PYTHON_CMD main.py --run-once
            ;;
        "scheduler")
            print_info "Starting scheduler..."
            $PYTHON_CMD main.py --schedule
            ;;
        "test")
            print_info "Running in test mode..."
            $PYTHON_CMD main.py --test --run-once
            ;;
        "status")
            print_info "Checking system status..."
            $PYTHON_CMD main.py --status
            ;;
        *)
            print_error "Unknown mode: $MODE"
            print_info "Available modes: daily, scheduler, test, status"
            exit 1
            ;;
    esac
}

# النسخ الاحتياطي
create_backup() {
    print_info "Creating system backup..."
    
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # نسخ الملفات المهمة
    cp -r database "$BACKUP_DIR/" 2>/dev/null
    cp -r config "$BACKUP_DIR/" 2>/dev/null
    cp .env "$BACKUP_DIR/" 2>/dev/null
    cp requirements.txt "$BACKUP_DIR/" 2>/dev/null
    
    # إنشاء أرشيف
    tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR" 2>/dev/null
    rm -rf "$BACKUP_DIR"
    
    print_success "Backup created: $BACKUP_DIR.tar.gz"
}

# القائمة الرئيسية
main_menu() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}  YouTube Auto Channel Manager${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo "1) Run Daily Pipeline"
    echo "2) Start Scheduler (24/7)"
    echo "3) Test System"
    echo "4) Check System Status"
    echo "5) Create Backup"
    echo "6) Install Requirements"
    echo "7) Exit"
    echo ""
    read -p "Select option [1-7]: " choice
    
    case $choice in
        1) run_system "daily" ;;
        2) run_system "scheduler" ;;
        3) run_system "test" ;;
        4) run_system "status" ;;
        5) create_backup ;;
        6) install_requirements ;;
        7) print_info "Goodbye!"; exit 0 ;;
        *) print_error "Invalid option"; main_menu ;;
    esac
}

# السيناريو التلقائي
auto_run() {
    print_info "Auto-run mode activated"
    
    check_python
    check_requirements
    check_env
    create_directories
    cleanup_old_files
    
    # تشغيل خط العمل اليومي
    run_system "daily"
}

# معالجة الوسائط
if [ $# -eq 0 ]; then
    # وضع التفاعلي
    check_python
    check_requirements
    check_env
    create_directories
    cleanup_old_files
    main_menu
else
    case "$1" in
        "auto") auto_run ;;
        "daily") run_system "daily" ;;
        "scheduler") run_system "scheduler" ;;
        "test") run_system "test" ;;
        "status") run_system "status" ;;
        "backup") create_backup ;;
        "install") install_requirements ;;
        "cleanup") cleanup_old_files ;;
        *) print_error "Unknown command: $1"; exit 1 ;;
    esac
fi
