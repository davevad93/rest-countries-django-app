document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('language-select').addEventListener('change', function() {
        document.getElementById('language-form').submit();
    });
});
