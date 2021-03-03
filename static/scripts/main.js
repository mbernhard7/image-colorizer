function readURL(input) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();

    reader.onload = function(e) {
      $('.image-upload-wrap').hide();

      $('.file-upload-image').attr('src', e.target.result);
      $('.file-upload-content').show();

      $('.image-title').html(input.files[0].name);
      var newName=input.files[0].name.split(".")[0];
      newName=newName+'-colorized.jpg';
      $('.new-image-title').html(newName);
      $('.download-link').attr('download',newName);
    };

    reader.readAsDataURL(input.files[0]);

  } else {
    removeUpload();
  }
}

function colorizeImage() {
  fetch($('.file-upload-image').attr('src'))
  .then(res => res.blob())
  .then(blob => {
    const file = new File([blob], 'image.jpg', blob)
    if (file) {
      const formData = new FormData()
      formData.append('imageFile', file)
      const options = {
        method: 'POST',
        body: formData,
      };
      fetch('/colorize', options)
      .then(res => {
        if (res.status==200) {
          res.blob()
          .then(blob => {
            const imgURL = URL.createObjectURL(blob);
            $('.file-return-image').attr('src', imgURL);
            $('.download-link').attr('href', imgURL);
            $('.file-return-content').show();
          });
        } else {
          console.error(status+' '+res.text())
        }
      })
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
  $('.file-return-content').hide();
  $('.image-upload-wrap').show();
}

function downloadImage() {
  $('.download-link').attr("style","");
  document.getElementsByClassName('download-link')[0].click();
}

function openPage(pageName, elmnt) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].className = tabcontent[i].className.replace(" current", "");
  }

  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" current", "");
  }

  document.getElementById(pageName).className += " current";
  elmnt.className+=" current";
}