function search(){
  var input, filter, ul, li, a, i, textValue;
  input = document.getElementById("search_list");
  filter = input.value.toUpperCase();
  ul = document.getElementById("app_list");
  li = document.getElementsByTagName("li");
  for(i = 0; i < li.length; i++){
    a = li[i].getElementsByTagName("button")[0];
    textValue = a.textContent || a.innerText;
    if(textValue.toUpperCase().indexOf(filter) > -1){
      li[i].style.display = "";
    }
    else {
      li[i].style.display = "none";
    }
  }
}

function openDiv(evt, divName) {
  var i, listcontent, listlinks;
  listcontent = document.getElementsByClassName("listcontent");
  for (i = 0; i < listcontent.length; i++) {
    listcontent[i].style.display = "none";
  }
  listlinks = document.getElementsByClassName("listlinks");
  document.getElementById(divName).style.display = "block";
}
