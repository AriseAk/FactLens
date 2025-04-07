// Extract headline and description from the current page
function extractPageContent() {
    const headline = document.title;
    const description = document.querySelector('meta[name="description"]')?.content || '';
    const domain = window.location.href;
    return { headline, description, domain };
  }
  
  // Send data to the Flask API (or handle locally)
  chrome.runtime.sendMessage({
    action: "checkClickbait",
    data: extractPageContent()
  }, (response) => {
    console.log("Clickbait score:", response.result);
  });
  