document.getElementById('symptom-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fever = document.getElementById('fever').checked;
    const headache = document.getElementById('headache').checked;
    const chills = document.getElementById('chills').checked;

    const btnText = document.getElementById('btn-text');
    const btnLoader = document.getElementById('btn-loader');
    const analyzeBtn = document.querySelector('.analyze-btn');
    const resultsPanel = document.getElementById('results');

    // Loading state
    btnText.style.display = 'none';
    btnLoader.style.display = 'block';
    analyzeBtn.style.opacity = '0.8';
    resultsPanel.classList.remove('visible');

    // Reset bars
    document.getElementById('flu-bar').style.width = '0%';
    document.getElementById('malaria-bar').style.width = '0%';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ fever, headache, chills })
        });

        const data = await response.json();

        // Slight delay for animation effect
        setTimeout(() => {
            // Restore button
            btnText.style.display = 'block';
            btnLoader.style.display = 'none';
            analyzeBtn.style.opacity = '1';

            // Update results
            document.getElementById('flu-val').innerText = `${data.flu_probability}%`;
            document.getElementById('malaria-val').innerText = `${data.malaria_probability}%`;

            resultsPanel.classList.add('visible');

            // Animate progress bars after panel is visible
            setTimeout(() => {
                document.getElementById('flu-bar').style.width = `${data.flu_probability}%`;
                document.getElementById('malaria-bar').style.width = `${data.malaria_probability}%`;
            }, 50);

        }, 600);

    } catch (error) {
        console.error("Error fetching prediction:", error);
        btnText.style.display = 'block';
        btnLoader.style.display = 'none';
        analyzeBtn.style.opacity = '1';
        alert("There was an error communicating with the server.");
    }
});
