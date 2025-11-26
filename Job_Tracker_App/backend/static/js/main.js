document.addEventListener('DOMContentLoaded', function() {
    // Check if the form is in 'add new job' mode (not editing)
    // This logic needs to be handled by the backend or by checking a specific element/class in the form
    // For now, we'll assume if the application_date field is empty, it's a new form.
    var applicationDateInput = document.querySelector('input[name="application_date"]');
    if (applicationDateInput && !applicationDateInput.value) {
        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();
        today = yyyy + '-' + mm + '-' + dd;
        applicationDateInput.value = today;
    }
});
