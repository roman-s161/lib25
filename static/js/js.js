window.addEventListener('load', function() {
    setTimeout(function() {
        var messages = document.querySelectorAll('.flash-message');
        messages.forEach(function(message) {
            message.style.opacity = '0';
            message.style.transform = 'translateY(20px)';
            setTimeout(function() {
                message.remove();
            }, 500);
        });
    }, 5000);
});