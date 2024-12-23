document.addEventListener("DOMContentLoaded", () => {
    const selectedValues = {};
  
    const ageMapping = {
      "20대": 20.0,
      "30대": 30.0,
      "40대": 40.0,
      "50대": 50.0,
      "60대": 60.0,
    };
  
    const genderMapping = {
      "여성": 1,
      "남성": 0,
    };
  
    const dropdownItems = document.querySelectorAll(".dropdown-item");
  
    dropdownItems.forEach((item) => {
      item.addEventListener("click", function (event) {
        event.preventDefault();
  
        const value = this.textContent.trim();
        const dropdownKey = this.closest(".dropdown")
          .querySelector(".dropdown-toggle")
          .getAttribute("data-key");
  
        let convertedValue = value;
        if (dropdownKey === "age") {
          convertedValue = parseFloat(ageMapping[value]);
        } else if (dropdownKey === "gender") {
          convertedValue = parseFloat(genderMapping[value]);
        }
  
        this.closest(".dropdown").querySelector(".dropdown-toggle").textContent =
          value;
  
        selectedValues[dropdownKey] = convertedValue;
  
        console.log(selectedValues);
      });
    });
  
    document.querySelector(".bus-icon").addEventListener("click", () => {
      // Store the selectedValues in localStorage
      localStorage.setItem('user_info', JSON.stringify(selectedValues));
  
      // Redirect to the next page
      window.location.href = "/index";
    });
  });
  