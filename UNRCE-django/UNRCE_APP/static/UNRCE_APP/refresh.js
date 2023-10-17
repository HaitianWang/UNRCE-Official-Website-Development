document.addEventListener('DOMContentLoaded', function() {
    const refreshCaptchaLink = document.getElementById('refresh_captcha');
    if (refreshCaptchaLink) {
        const captchaImage = document.getElementById('captcha_image');
        const captchaKeyInput = document.getElementById('captcha_key_input');

        refreshCaptchaLink.addEventListener('click', function(event) {
            event.preventDefault();

            fetch('/new_captcha/')
            .then(response => response.json())
            .then(data => {
                captchaImage.src = data.captcha_image_url;
                captchaKeyInput.value = data.captcha_key;
            });
        });
    }
});