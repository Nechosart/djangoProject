var maxLen = 30;
var titles = document.getElementsByTagName("short");

for (i = 0; i < titles.length; i++) {
    if (titles[i].innerText.length > maxLen) {
        titles[i].innerHTML = titles[i].innerHTML.substr(0, maxLen)+"...";
    }
}