#!/bin/bash
# ============================================================
# ⚡ Multi-Agent Orchestrator - Safe GitHub Push Script
# ============================================================

echo "������ Starting Safe GitHub Deployment"
echo "====================================================="

# ============================================================
# 1️⃣ التحقق من Git
# ============================================================
if ! command -v git &> /dev/null; then
    echo "❌ Git غير مثبت. الرجاء تثبيت Git أولاً"
    exit 1
fi
echo "✅ Git مثبت: $(git --version)"
echo ""

# ============================================================
# 2️⃣ تكوين Git (إذا لم يكن مكوّنًا)
# ============================================================
if [ -z "$(git config --global user.name)" ]; then
    read -p "������‍������ أدخل اسمك في Git: " GIT_NAME
    git config --global user.name "$GIT_NAME"
fi

if [ -z "$(git config --global user.email)" ]; then
    read -p "������ أدخل بريدك الإلكتروني في Git: " GIT_EMAIL
    git config --global user.email "$GIT_EMAIL"
fi

echo "✅ تم تكوين Git باسم: $(git config --global user.name)"
echo "✅ البريد الإلكتروني: $(git config --global user.email)"
echo ""

# ============================================================
# 3️⃣ إعداد المستودع المحلي نظيف
# ============================================================
if [ -d ".git" ]; then
    echo "⚠️ تم العثور على مستودع Git سابق، سيتم تنظيفه لإزالة أي secrets"
    rm -rf .git
fi

git init
git add .
git commit -m "������ Initial clean commit - no secrets"
echo "✅ مستودع محلي نظيف تم إنشاؤه"
echo ""

# ============================================================
# 4️⃣ إضافة remote
# ============================================================
REPO_URL="https://github.com/ilyeseia/multi-agent-orchestrator-web.git"
git remote add origin "$REPO_URL"
git branch -M main
echo "✅ remote تم تعيينه إلى: $REPO_URL"
echo ""

# ============================================================
# 5️⃣ تعليمات آمنة للـ Push
# ============================================================
echo "⚠️ ملاحظات قبل الـ push:"
echo "1️⃣ لا تضع أي Token أو password داخل السكربت!"
echo "2️⃣ عند الطلب:"
echo "   Username: اسم المستخدم على GitHub"
echo "   Password: Personal Access Token (تدخله يدويًا)"
echo ""

read -p "هل تريد المتابعة بالـ Push؟ (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "������ تم الإلغاء."
    exit 1
fi

# ============================================================
# 6️⃣ تنفيذ Push نظيف
# ============================================================
git push -u origin main --force

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ تم النشر بنجاح على GitHub!"
    echo "������ رابط المستودع: $REPO_URL"
    echo "=================================================="
else
    echo "❌ فشل الـ push. تأكد من التوكن والاتصال بالإنترنت."
    exit 1
fi

# ============================================================
# 7️⃣ أوامر مفيدة لاحقًا
# ============================================================
echo ""
echo "������ أوامر مستقبلية:"
echo "git add ."
echo "git commit -m 'رسالة التغيير'"
echo "git push origin main"
echo "git checkout -b feature/اسم_الفرع"
echo "git push -u origin feature/اسم_الفرع"
echo "git log --oneline -10"
echo ""
echo "=================================================="
echo "شكراً لاستخدام Multi-Agent Orchestrator! ������"
