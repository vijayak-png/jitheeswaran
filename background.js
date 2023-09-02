// background.js
chrome.runtime.onInstalled.addListener(function () {
  console.log("Extension installed");
  performAutomaticActions();
});

function performAutomaticActions() {
  const selectedText = "Sample text for prediction";
  const textForReport = "Sample text for report";

  predictText(selectedText);
  generateReport(textForReport);
}

function predictText(text) {
  fetch('YOUR_PREDICTION_SERVER_ENDPOINT', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title: text })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Prediction Result:', data);
    // Handle the prediction data here
  })
  .catch(error => console.error('Prediction Error:', error));
}

function generateReport(text) {
  fetch('YOUR_REPORT_SERVER_ENDPOINT', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ website: 'example.com', fake_news: text })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Report Generation Result:', data);
    // Handle the report generation data here
  })
  .catch(error => console.error('Report Generation Error:', error));
}
