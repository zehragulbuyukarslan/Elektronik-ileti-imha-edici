const form = document.getElementById('deleteForm');
        const statusDiv = document.getElementById('status');
        const deleteBtn = document.getElementById('deleteBtn');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const keywords = document.getElementById('keywords').value;
            const deleteFrom = document.getElementById('deleteFrom').value;
            const startDate = document.getElementById('startDate').value;
            const endDate = document.getElementById('endDate').value;

            // Validasyon
            if (!email || !password || !keywords) {
                showStatus('Email, şifre ve anahtar kelimeler gereklidir!', 'error');
                return;
            }

            // Loading durumu
            showStatus('<span class="spinner"></span>İşlem başladı... Lütfen bekleyin...', 'loading');
            deleteBtn.disabled = true;

            try {
                const response = await fetch('/delete', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password,
                        keywords: keywords,
                        delete_from: deleteFrom,
                        start_date: startDate,
                        end_date: endDate
                    })
                });

                const result = await response.json();

                if (result.status === 'success') {
                    showStatus(`✅ ${result.deleted} e-posta başarıyla silindi!`, 'success');
                    form.reset();
                } else {
                    showStatus('❌ Hata: ' + result.message, 'error');
                }
            } catch (error) {
                showStatus('❌ Bir hata oluştu: ' + error.message, 'error');
            } finally {
                deleteBtn.disabled = false;
            }
        });

        function showStatus(message, type) {
            statusDiv.className = 'status ' + type;
            statusDiv.innerHTML = message;
        }