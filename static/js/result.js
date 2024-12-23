document.addEventListener("DOMContentLoaded", () => {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);

  const selectedValues = {};
  for (const [key, value] of urlParams.entries()) {
    selectedValues[key] = value;
  }

  //   if (Object.keys(selectedValues).length > 0) {
  //     console.log("Final Selection:", selectedValues);
  //     displayResult(selectedValues);
  //   } else {
  //     console.error("No data found in URL parameters.");
  //   }
  // });
  if (Object.keys(selectedValues).length > 0) {
    console.log("Final Selection:", selectedValues);
    displayResult(selectedValues);
  } else {
    console.error("No data found in URL parameters.");
  }
});

function displayResult(choices) {
  const resultContent = document.getElementById("result-content");

  //   callPredictAPI(choices).then((data) => {
  //     resultContent.innerHTML = `<h1>추천 여행지: ${data}</h1>`;
  //   });
  // }
  callPredictAPI(choices).then((data) => {
    alert(data);
    if (data != null) {
      const parsedData = JSON.parse(data); // JSON 데이터를 객체로 변환
      const recommendation = parsedData
        .map((item) => `<li>${item.VISIT_AREA_NM} - Score: ${item.SCORE}</li>`)
        .join("");

      resultContent.innerHTML = `<h1>추천 여행지</h1><ul>${recommendation}</ul>`;
    } else {
      resultContent.innerHTML = `<h1>추천 결과를 가져오는 데 실패했습니다.</h1>`;
    }
  });
}
function callPredictAPI(features) {
  const url = "http://127.0.0.1:5500/predict";

  return $.ajax({
    url: url,
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify(features),
  })
    .then((response) => {
      if (response.error) {
        throw new Error(response.error);
      }
      // console.log("Traveler 객체:", response.traveler); // traveler 객체를 콘솔에 출력
      // console.log("Prediction 결과:", response.prediction); // 예측 결과를 콘솔에 출력
      return response;
    })
    .catch((error) => {
      console.error("API 호출 중 오류 발생:", error);
    });
}
