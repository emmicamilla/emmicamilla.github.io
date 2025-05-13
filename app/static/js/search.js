document.addEventListener('DOMContentLoaded', function () {
    // Choices.js valintalistoille (jos käytössä index-sivulla)
    const elements = document.querySelectorAll('.js-choice');
    const choicesInstances = [];
  
    elements.forEach(function (el) {
      const instance = new Choices(el, {
        removeItemButton: true,
        placeholderValue: 'Select...',
        searchPlaceholderValue: 'Search...',
      });
      choicesInstances.push(instance);
    });
  
    // Reset filters -napin toiminta
    const resetButton = document.getElementById('reset-filters');
    if (resetButton) {
      resetButton.addEventListener('click', function () {
        // Tyhjennä valinnat
        choicesInstances.forEach(instance => instance.clearStore());
  
        // Tyhjennä muut mahdolliset hakukentät
        const filterInputs = document.querySelectorAll('.filter-input');
        filterInputs.forEach(input => input.value = '');
  
        // Lähetä lomake uudelleen (oletetaan että on lomake)
        const form = document.getElementById('filter-form');
        if (form) {
          form.submit();
        }
      });
    }
  });
  