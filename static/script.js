async function getRecommendation() {
    const movie = document.getElementById("movie").value;

    if (!movie.trim()) {
    alert("Enter a movie name");
    return;
}

    document.getElementById("result").innerHTML = `
    <div style="text-align:center; padding:20px;">
        🔄 Fetching recommendations...
    </div>
`;

    try {
        const res = await fetch("/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ movie })
        });

        const data = await res.json();

        let html = "";

data.movies.forEach(m => {
    html += `
        <div class="movie-card">
            <img src="${m.poster || 'https://via.placeholder.com/80x120?text=No+Image'}" />
            <div class="info">
                <h3>${m.title}</h3>
                <p>${m.desc}</p>
            </div>
        </div>
    `;
});

document.getElementById("result").innerHTML = html;

document.getElementById("result").innerHTML = html;
document.getElementById("result").innerHTML = html;

document.getElementById("result").innerHTML = html;
        document.getElementById("result").innerHTML = html;

    } catch (error) {
        console.error(error);
        document.getElementById("result").innerHTML = "Error loading recommendations";
    }
}