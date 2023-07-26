let oldSelectIndex_mood = 0;
let now_audio = null;
let data = null;
let keys = null;
let keys_index = 0;
let sentence_index = 1;

function text_api(content, file_type){
  fetch("http://127.0.0.1:8000/story", {
    method: "POST",
    headers: {
        'content-type': 'application/json'
    },
    body: JSON.stringify({"user": "bird", "story": content, "type": file_type})
  })
  .then((response) => {
    return response.json();
  }).then((jsonData) => {
    createBook(jsonData);

    data = jsonData;
    keys = Object.keys(data)
  })
}

function createBook(data)
{
  const pages = Object.values(data);
  let cnt = 1;

  pages.forEach(page => {
    let cnt_line = 0
    let node = document.createElement('div');
    node.setAttribute("class", "text");

    page.forEach(line => {
      let node1 = document.createElement('span');
      node1.id = `p${cnt}_${cnt_line}`;
      node1.innerHTML = line.content + " ";
      node.appendChild(node1)
      cnt_line++;
    });

    createPage(node, cnt);

    cnt++;
  });

  createPageEnd();
}

function music(data, pages, pages_index, sentence_index)
{
  let sentence = data[pages[pages_index]];

  if(pages_index < pages.length)
  {
    if(sentence_index <= sentence.length)
    {
      let reply_audio = new Audio()
      now_audio = reply_audio;
      reply_audio.src = sentence[sentence_index - 1].speech;
      reply_audio.play();

      change_mood(sentence[sentence_index - 1].emotion);
      sendEmotion(sentence[sentence_index - 1].emotion);

      let text_el = document.getElementById(`p${pages_index + 1}_${sentence_index - 1}`);
      text_el.style.color = 'red';

      reply_audio.addEventListener("ended", () => {
        console.log(sentence_index);
        console.log(sentence.length);
        text_el.style.color = 'black';

        if(sentence_index < sentence.length && sentence_index + 1 <= sentence.length)
        {
          music(data, pages, pages_index, ++sentence_index)
        }
        else
        {
          sentence_index = 1;

          if (pages_index >= pages.length - 1)
            $("#flipbook").turn("page", 1);
          else if((pages_index + 1) % 2 == 1)
            $("#flipbook").turn("next");

          music(data, pages, ++pages_index, sentence_index)
        }
      })
    }
  }
}

function change_mood(mood)
{
  let moodE1 = document.getElementById("mood")
  let moodList = moodE1.getElementsByTagName("li")

  if (oldSelectIndex_mood != null && mood != moodE1.children[oldSelectIndex_mood].innerHTML) // 刪除前個 motion 的 select
    moodE1.children[oldSelectIndex_mood].classList.remove("selected")

  for(let i=0; i < moodList.length; i++)
  {
    if(moodList[i].innerHTML == mood)
    {
      moodList[i].classList.add("selected");
      oldSelectIndex_mood = i;
    }
  }
}

document.getElementById('story').addEventListener('change', function (event) {
  const file_type = this.files[0].name.split(".")[1];

  document.getElementById('getstory').text = this.files.length + " file(s) selected";

  if(this.files.length > 0)
  {
    let text = this.files[0].text();

    console.log("YYY");
    document.getElementById('choose_story').style.display = "block";
    document.getElementById('story_box').style.display = "none";

    text.then(function(value) {
      text_api(value, file_type);
    });
  }
});

function choose_story()
{
  if (now_audio != null)
  {
    now_audio.pause();
    now_audio.currentTime = 0;
  }

  change_mood("Idle");
  sendEmotion("Idle");

  document.getElementById('flipbook').style.display = "none";
  document.getElementById('choose_story').style.display = "none";
  document.getElementById('story_box').style.display = "block";

  const file = document.getElementById('story');
  file.value = '';
}

function createPageEnd()
{
  const book = document.getElementById('flipbook');

  let node = document.createElement('div');
  node.setAttribute("class", "hard");

  book.appendChild(node);
  book.appendChild(node);

  $("#flipbook").turn({
    width: 900,
    height: 450,
    autoCenter: true
  });

  document.getElementById('flipbook').style.display = "block";
}

function createPage(text_node, page_index)
{
  // <div class="book" id="p1">
  //   <div class="text">
  //       &emsp;&emsp; Little Nini was wearing her favorite cute dress and carrying a backpack, ready for an adventure.
  //       As she walked down the street, she saw a little boy crying. Nini asked, "What happened? Why are you crying?"
  //       <br><br>&emsp;&emsp;The little boy replied, "I'm lost, and I can't find my way home." Nini immediately felt sad
  //       because she had been lost before. She decided to help the little boy find his way home.
  //   </div>
  // </div>
  // <div class="hard"></div>
  // <div class="hard"></div>
  const book = document.getElementById('flipbook');

  let node1 = document.createElement('div');
  node1.setAttribute("class", "book");
  node1.setAttribute("id", `p${page_index}`);

  node1.appendChild(text_node);
  book.appendChild(node1);
}

$("#flipbook").bind("turning", function(event, page, view) {
  document.getElementById("flipbook").style.left = document.getElementById("flipbook").style.left-10;

  if(page == 2)
    music(data, keys, keys_index, sentence_index)
});
