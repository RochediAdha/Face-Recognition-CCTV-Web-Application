document.addEventListener("DOMContentLoaded", async () => {
  const cctvContainer = document.getElementById("cctv-container");

  try {
    const response = await fetch("http://localhost:5000/api/cctv");
    if (!response.ok) {
      throw new Error(`Failed to fetch CCTV list: ${response.status}`);
    }

    const cctvList = await response.json();

    cctvList.forEach((cctv) => {
      const cctvItem = document.createElement("div");
      cctvItem.className = "cctv-item";

      const cctvTitle = document.createElement("h2");
      cctvTitle.textContent = cctv.name;

      const cctvImage = document.createElement("img");
      cctvImage.src = `http://localhost:5000/api/video_feed/${cctv.id}`;
      cctvImage.alt = `Live feed of ${cctv.name}`;
      cctvImage.style.width = "100%";

      cctvItem.appendChild(cctvTitle);
      cctvItem.appendChild(cctvImage);
      cctvContainer.appendChild(cctvItem);
    });
  } catch (error) {
    console.error("Error fetching CCTV list:", error);
    cctvContainer.innerHTML =
      "<p>Error loading CCTV streams. Please try again later.</p>";
  }
});
