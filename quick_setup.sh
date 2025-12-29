#!/bin/bash

echo "🚀 YouTube Auto Channel - GitHub Actions Quick Setup"
echo "====================================================="

# 1. إنشاء مجلدات Workflows
echo "📁 Creating GitHub Actions directories..."
mkdir -p .github/workflows

# 2. جعل ملفات Python قابلة للتنفيذ
chmod +x setup_github_actions.py

# 3. تشغيل سكريبت الإعداد
echo "🔧 Running setup script..."
python setup_github_actions.py

# 4. تحديث ملف requirements.txt للـ GitHub Actions
echo "📦 Updating requirements for GitHub Actions..."
cat > requirements_github.txt << EOF
# متطلبات GitHub Actions (مختصرة)
Pillow>=10.0.0
moviepy>=1.0.3
google-api-python-client>=2.100.0
google-auth-oauthlib>=1.0.0
openai>=1.3.0
google-generativeai>=0.3.0
requests>=2.31.0
gTTS>=2.3.2
pydub>=0.25.1
EOF

echo "✅ Setup complete!"
echo ""
echo "📋 What to do next:"
echo "1. git add .github/ setup_github_actions.py quick_setup.sh"
echo "2. git commit -m 'Add GitHub Actions workflows'"
echo "3. git push"
echo "4. Go to GitHub → Settings → Secrets and variables → Actions"
echo "5. Add your API keys as secrets"
echo "6. Go to Actions tab and enable all workflows"
echo "7. Run 'Daily System Test' manually"
