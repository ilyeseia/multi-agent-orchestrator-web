// ================================
// Dashboard / UI JavaScript
// ================================

// مثال: عرض رسالة تنبيه تلقائية
function showAlert(message, type="success") {
    const container = document.createElement("div");
    container.textContent = message;
    container.className = type === "success" ? "flash-message-success" : "flash-message-error";
    
    document.body.prepend(container);

    // اختفاء الرسالة بعد 3 ثوانٍ
    setTimeout(() => {
        container.remove();
    }, 3000);
}

// مثال: تأكيد قبل حذف مشروع
document.querySelectorAll(".delete-project-btn").forEach(button => {
    button.addEventListener("click", function(e){
        if(!confirm("Are you sure you want to delete this project?")) {
            e.preventDefault();
        }
    });
});

// مثال: تحسين تجربة إرسال النماذج عبر AJAX (يمكن تفعيله لاحقًا)
function ajaxFormSubmit(formId, callback) {
    const form = document.getElementById(formId);
    if(!form) return;

    form.addEventListener("submit", function(e){
        e.preventDefault();
        const formData = new FormData(form);
        fetch(form.action, {
            method: form.method,
            body: formData
        })
        .then(response => response.json())
        .then(data => callback(data))
        .catch(err => console.error(err));
    });
}
