// sidebar.js
document.addEventListener('DOMContentLoaded', function() {
    var navItems = document.querySelectorAll('.nav-item');

    navItems.forEach(function(item) {
        item.addEventListener('mouseover', function() {
            document.querySelector('.sidebar').classList.add('active');
        });

        item.addEventListener('mouseout', function() {
            document.querySelector('.sidebar').classList.remove('active');
        });
    });
});
