const inFile = document.getElementById("input-file");
const previewBox = document.getElementById("imagePreview");
const previewImage = previewBox.querySelector(".image-preview__image");
const previewText = previewBox.querySelector(".image-preview__default-text");

inFile.addEventListener("change", function() {
  const file = this.files[0];
  
  if (file) {
    const read = new FileReader();
    previewText.style.display = 'none';
    previewImage.style.display = 'block';

    read.addEventListener("load", function() {
      previewImage.setAttribute("src", this.result);
      console.log(this.result);
    });

    read.readAsDataURL(file);

  }else{
      previewText.style.display = 'null';
      previewImage.style.display = 'null';
      previewImage.setAttribute("src", "");
  }

});