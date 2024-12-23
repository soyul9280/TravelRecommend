const selectedValues = JSON.parse(localStorage.getItem('user_info')) || {}; // Load previous data

document.addEventListener("DOMContentLoaded", () => {
  const questionBoxes = document.querySelectorAll(".question-box");

  questionBoxes.forEach((item) => {
    item.addEventListener("click", function (event) {
      event.preventDefault();

      const questionArea = this.closest(".question-area");
      const questionKey = questionArea.getAttribute("data-question");
      const value = this.getAttribute("data-value");
      selectedValues[questionKey] = value;

      questionArea.querySelectorAll(".question-box").forEach((box) => {
        box.classList.remove("selected");
      });

      this.classList.add("selected");
      console.log(selectedValues);
    });
  });
});

function moveBus() {
    const busIcon = document.querySelector('.bus-icon');
    busIcon.classList.add('move-right');

    setTimeout(function() {
        // URL 쿼리 문자열 생성
        const queryParams = new URLSearchParams(selectedValues).toString();
        
        // `result.html`로 이동하며 쿼리 문자열 전달
        window.location.href = `result.html?${queryParams}`;
    }, 2000);
}




function moveBus() {
    const busIcon = document.querySelector('.bus-icon');
    busIcon.classList.add('move-right');

    setTimeout(function() {
        const queryParams = new URLSearchParams(selectedValues).toString();
        window.location.href = `result.html?${queryParams}`;
    }, 2000);
}
