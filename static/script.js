// JavaScript code for interactivity
document.addEventListener('DOMContentLoaded', function() {
    const recipeLinks = document.querySelectorAll('.recipe-link');

    recipeLinks.forEach(link => {
        link.addEventListener('click', function() {
            const url = this.getAttribute('href');
            this.classList.add('animate__animated', 'animate__pulse');
            setTimeout(() => {
                window.location.href = url;
            }, 500);
        });
    });
});
