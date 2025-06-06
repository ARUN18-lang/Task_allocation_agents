document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("uploadForm").addEventListener("submit", async function (event) {
        event.preventDefault();
        const fileInput = document.getElementById("file");
        const file = fileInput.files[0];
        if (!file) {
            alert("Please select a file to upload.");
            return;
        }
        const formData = new FormData();
        formData.append("file", file);
        try {
            const response = await fetch("/upload", {
                method: "POST",
                body: formData
            });
            const result = await response.json();
            const resultDiv = document.getElementById("result");
            resultDiv.classList.remove("d-none");
            if (result.error) {
                resultDiv.innerHTML = `<div class="alert alert-danger">${result.error}</div>`;
            } else {
                let html = `<h5>${result.message}</h5>`;
                html += `<ul class="list-group">`;
                result.report.forEach((employee, index) => {
                    html += `
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                            <div>
                                ${employee.name} - ${employee.role || 'Role not defined'}
                            </div>
                            <div>
                                <button onclick="approve(${index})" class="btn btn-sm btn-success me-2">✔</button>
                                <button onclick="reject(${index})" class="btn btn-sm btn-danger">✖</button>
                            </div>
                        </li>`;
                });
                html += `</ul>`;
                resultDiv.innerHTML = html;
            }
        } catch (error) {
            alert("An error occurred while uploading the file.");
            console.error(error);
        }
    });
    function approve(index) {
        alert(`Employee ${index + 1} approved.`);
    }
    function reject(index) {
        alert(`Employee ${index + 1} rejected.`);
    };
});