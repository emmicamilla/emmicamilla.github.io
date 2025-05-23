document.addEventListener('DOMContentLoaded', function () {
  // Choices.js alustus (jos käytössä filttereissä)
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

  // Reset-nappi (valintojen tyhjennykseen, jos käytössä)
  const resetButton = document.getElementById('reset-filters');
  if (resetButton) {
    resetButton.addEventListener('click', function () {
      choicesInstances.forEach(instance => instance.clearStore());
    });
  }

  // Gallerian kuvat ja modal
  const galleryImages = document.querySelectorAll('.gallery-image');
  const modal = new bootstrap.Modal(document.getElementById('imageModal'));
  const modalImage = document.getElementById('modalImage');
  const modalCaption = document.getElementById('modalCaption');
  const formImageId = document.getElementById('formImageId');
  const textarea = document.getElementById('markerPurposeTextarea');
  const saveButton = document.getElementById('saveButton');

  galleryImages.forEach(img => {
    img.addEventListener('click', () => {
      // Näytä kuva
      modalImage.src = img.src;

      // Näytä kuvateksti
      const caption = `
        Staining: ${img.dataset.staining}<br>
        Tissue: ${img.dataset.tissue}<br>
        Magnification: ${img.dataset.magnification}<br>
        Diagnosis: ${img.dataset.diagnosis || '–'}
      `;
      if (modalCaption) {
        modalCaption.innerHTML = caption;
      }

      // Aseta hidden inputiin image_id (voit muuttaa tämän image.id:ksi, jos sinulla on se data-attribuuttina)
      if (formImageId) {
        formImageId.value = img.dataset.filename;
      }

      // Aseta marker_purpose-tekstilaatikon arvo
      if (textarea) {
        textarea.value = img.dataset.markerPurpose || '';
      }

      // Näytä Save-nappi
      if (saveButton) {
        saveButton.style.display = 'inline-block';
      }

      modal.show();
    });
  });
});
