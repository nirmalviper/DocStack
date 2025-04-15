document.addEventListener('DOMContentLoaded', function() {
    const treeNav = document.getElementById('book-tree');
    if (treeNav) {
        treeNav.addEventListener('click', function(event) {
            const header = event.target.closest('.tree-header');
            if (header) {
                const listItem = header.parentElement;
                if (listItem.classList.contains('folder')) {
                    listItem.classList.toggle('open');
                }
            }
        });
    }
});