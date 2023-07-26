
// if (window.account == null)
//   location.href="./login.html";

function goToStory()
{
  document.getElementById("select").style.display = "block";
  document.getElementById("container").style.display = "none";
  document.getElementById("story").style.display = "block";
  document.getElementById("chat").style.display = "none";

}

function goToChat()
{
  document.getElementById("select").style.display = "block";
  document.getElementById("container").style.display = "none";
  document.getElementById("story").style.display = "none";
  document.getElementById("chat").style.display = "block";
}

