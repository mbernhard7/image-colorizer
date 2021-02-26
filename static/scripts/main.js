function readURL(input) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();

    reader.onload = function(e) {
      $('.image-upload-wrap').hide();

      $('.file-upload-image').attr('src', e.target.result);
      $('.file-upload-content').show();

      $('.image-title').html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);

  } else {
    removeUpload();
  }
}

function colorizeImage() {
  const img = document.querySelector('file-upload-image') ;
  console.log(img.attr('src'))
  console.log(img.src)

  fetch(img.src)
  .then(res => res.blob())
  .then(blob => {
    const file = new File([blob], 'dot.png', blob)
    if (file) {
      const formData = new FormData()
      formData.append('imageFile', file)
      const options = {
        method: 'POST',
        body: formData,
        // If you add this, upload won't work
        // headers: {
        //   'Content-Type': 'multipart/form-data',
        // }
      };
      fetch('https://cs121-image-colorizer.herokuapp.com/colorize', options)
      .then(res => {
        res.text()
        .then(data => {
        console.log(data)
      })})
      .catch(error => {
        console.error(error)
      })

    } else {
      removeUpload();
    }})
}

function removeUpload() {
  $('.file-upload-input').replaceWith($('.file-upload-input').clone());
  $('.file-upload-content').hide();
  $('.image-upload-wrap').show();
}