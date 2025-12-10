document.addEventListener('DOMContentLoaded', function() {
    const createResizableTable = function(table) {
        const cols = table.querySelectorAll('thead th');
        [].forEach.call(cols, function(col) {
            // Add a resizer element to the column
            const resizer = document.createElement('div');
            resizer.classList.add('resizer');
            col.appendChild(resizer);

            // When you drag the resizer, adjust the column width
            resizer.addEventListener('mousedown', function(e) {
                let x = e.clientX;
                let w = col.offsetWidth;

                const mouseMoveHandler = function(e) {
                    const dx = e.clientX - x;
                    col.style.width = (w + dx) + 'px';
                };

                const mouseUpHandler = function() {
                    document.removeEventListener('mousemove', mouseMoveHandler);
                    document.removeEventListener('mouseup', mouseUpHandler);
                };

                document.addEventListener('mousemove', mouseMoveHandler);
                document.addEventListener('mouseup', mouseUpHandler);
            });
        });
    };

    const tables = document.querySelectorAll('.table-resizable');
    [].forEach.call(tables, function(table) {
        createResizableTable(table);
    });

    // View More functionality for Job Description
    var descriptionModal = document.getElementById('descriptionModal');
    descriptionModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;
        var description = button.getAttribute('data-description');
        var modalBody = descriptionModal.querySelector('#fullDescriptionContent');
        modalBody.innerHTML = description;
    });

    // Multi-select and Delete functionality
    const selectAllCheckbox = document.getElementById('selectAllJobs');
    const jobCheckboxes = document.querySelectorAll('.job-checkbox');
    const deleteSelectedBtn = document.getElementById('deleteSelectedBtn');

    function toggleDeleteButton() {
        const anyChecked = Array.from(jobCheckboxes).some(checkbox => checkbox.checked);
        deleteSelectedBtn.disabled = !anyChecked;
    }

    selectAllCheckbox.addEventListener('change', function() {
        jobCheckboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
        });
        toggleDeleteButton();
    });

    jobCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (!this.checked) {
                selectAllCheckbox.checked = false;
            }
            toggleDeleteButton();
        });
    });

    deleteSelectedBtn.addEventListener('click', function() {
        const selectedJobIds = Array.from(jobCheckboxes)
                                    .filter(checkbox => checkbox.checked)
                                    .map(checkbox => checkbox.getAttribute('data-job-id'));

        if (selectedJobIds.length > 0 && confirm('Are you sure you want to delete the selected jobs?')) {
            // Send a POST request to a new endpoint to delete multiple jobs
            fetch('/delete_multiple', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ids: selectedJobIds })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload(); // Reload the page to reflect changes
                } else {
                    alert('Error deleting jobs: ' + data.error);
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });

    toggleDeleteButton(); // Initial check on page load
});
