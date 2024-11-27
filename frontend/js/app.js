document.addEventListener("DOMContentLoaded", async () => {
  const cctvListElement = document.getElementById("cctv-list");

  try {
    const response = await fetch("http://localhost:5000/api/cctv");
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const cctvList = await response.json();
    cctvList.forEach((cctv) => {
      const li = document.createElement("li");
      const link = document.createElement("a");
      link.href = `http://localhost:5000/api/video_feed/${cctv.id}`;
      link.textContent = cctv.name;
      link.target = "_blank";
      li.appendChild(link);
      cctvListElement.appendChild(li);
    });
  } catch (error) {
    console.error("Error fetching CCTV list:", error);
    cctvListElement.innerHTML = `<p>Error loading CCTV list: ${error.message}</p>`;
  }
});
