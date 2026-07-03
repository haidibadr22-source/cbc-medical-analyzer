document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("uploadForm");
    const pdfInput = document.getElementById("pdf");

    const loading = document.getElementById("loading");
    const result = document.getElementById("result");

    const jsonOutput = document.getElementById("jsonOutput");
    const validation = document.getElementById("validation");
    const summary = document.getElementById("summary");

    const downloadBtn = document.getElementById("downloadBtn");

    let extractedJSON = null;

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        if (pdfInput.files.length === 0) {
            alert("Please select a PDF file.");
            return;
        }

        loading.style.display = "block";
        result.style.display = "none";

        const formData = new FormData();
        formData.append("file", pdfInput.files[0]);

        try {

            const response = await fetch("/analyze", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {

                const error = await response.json();
                throw new Error(error.error || "Server Error");

            }

            const data = await response.json();

            extractedJSON = data.json;

            jsonOutput.textContent =
                JSON.stringify(extractedJSON, null, 4);

            validation.textContent = data.validation;

            summary.textContent = data.summary;

            result.style.display = "block";

        }
        catch (err) {

            alert(err.message);

        }
        finally {

            loading.style.display = "none";

        }

    });


    downloadBtn.addEventListener("click", function () {

        if (!extractedJSON)
            return;

        const blob = new Blob(
            [JSON.stringify(extractedJSON, null, 4)],
            {
                type: "application/json"
            }
        );

        const url = URL.createObjectURL(blob);

        const a = document.createElement("a");

        a.href = url;

        a.download = "cbc_report.json";

        document.body.appendChild(a);

        a.click();

        a.remove();

        URL.revokeObjectURL(url);

    });

});
