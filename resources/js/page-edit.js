document.addEventListener('DOMContentLoaded', function () {
    const editButton = document.getElementById('main-edit-page-button');
    const backButton = document.getElementById('main-back-page-button');
    const mainShowPageData = document.getElementById('main-show-page-data');
    const mainEditPageData = document.getElementById('main-edit-page-data');
    const mainContent = document.getElementById('content');
    const mainPageContent = document.getElementById('main-page-html-render');
    const pageTitle = document.getElementById('bkmrk-page-title');
    const pageEditForm = document.getElementById('page-edit-form');

    let isSubmitting = false; // submission lock

    // Initial visibility setup
    if (mainShowPageData) mainShowPageData.hidden = false;
    if (mainEditPageData) mainEditPageData.hidden = true;
    if (editButton) editButton.hidden = false;
    if (backButton) backButton.hidden = true;

    // Toggle Edit/View Mode
    if (editButton && backButton && mainShowPageData && mainEditPageData) {
        editButton.addEventListener('click', () => {
            mainShowPageData.hidden = true;
            mainEditPageData.hidden = false;
            editButton.hidden = true;
            backButton.hidden = false;
            if (mainContent) mainContent.style.backgroundColor = 'rgb(239 241 255)';
        });

        backButton.addEventListener('click', () => {
            mainShowPageData.hidden = false;
            mainEditPageData.hidden = true;
            editButton.hidden = false;
            backButton.hidden = true;
            if (mainContent) mainContent.style.backgroundColor = '';
        });
    } else {
        console.warn('One or more toggle elements are missing from the DOM.');
    }

    // Handle AJAX Form Submit
    if (pageEditForm) {
        // Ensure listener is only bound once
        pageEditForm.addEventListener('submit', function(e) {
            e.preventDefault();

            if (isSubmitting === false){
                isSubmitting = true;
                return; // prevent double submission
            }

            const url = pageEditForm.action;
            const formData = new FormData(pageEditForm);
            const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content || '';
            const method = pageEditForm.querySelector('input[name="_method"]')?.value || 'POST';
            formData.append('_method', method);

            // Clear previous validation errors
            pageEditForm.querySelectorAll('.error-message').forEach(el => el.textContent = '');

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRF-TOKEN': csrfToken,
                    'Accept': 'application/json',
                },
                body: formData
            })
                .then(async res => {
                    const data = await res.json();
                    if (res.ok && data.status === 'success') {
                        // alert(data.message || 'Page saved successfully!');
                        // Update content
                        pageTitle.innerHTML = '';
                        pageTitle.innerHTML = data.name;
                        mainPageContent.innerHTML = '';
                        mainPageContent.innerHTML = data.html;
                        backButton?.click(); // Return to view mode
                    } else if (res.status === 422 && data.errors) {
                        // Laravel validation errors
                        for (const [field, messages] of Object.entries(data.errors)) {
                            const errorEl = pageEditForm.querySelector(`[data-error-for="${field}"]`);
                            if (errorEl) errorEl.textContent = messages.join(', ');
                        }
                    } else {
                        alert(data.message || 'An unexpected error occurred.');
                    }
                })
                .catch(error => {
                    console.error('Save error:', error);
                    alert('Unexpected error. Try again.');
                })
                .finally(() => {
                    isSubmitting = false;
                });
        }
        );
    }
});
