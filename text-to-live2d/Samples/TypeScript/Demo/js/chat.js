let add_chat = document.getElementById("msg-page")
let frames_oldSelectIndex_mood = {"frame1": 0, "frame2": 0};

function text_api(content)
{
  document.getElementById("form-control").disabled = true;

  const iframe1 = window.frames[0].document;
  const iframe2 = window.frames[1].document;
  const account = getCookie("userAccount")
  fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
          'content-type': 'application/json'
      },
      body: JSON.stringify({"user": account, "msg": content})
  })
  .then((response) => {
    return response.json();
  }).then((jsonData) => {
    const me_emotion = jsonData.me.emotion;
    const me_speech = jsonData.me.speech;
    console.log(me_speech);

    change_mood(iframe2.getElementById("mood"), me_emotion, "frame2");
    window.frames[1].sendEmotion(me_emotion);

    const audio = new Audio(me_speech);
    audio.play()

    audio.onended = function() {
      let cnt = 0
      const robot = jsonData.robot;

      let reply_audio = new Audio()

      reply_audio.src = robot[cnt].speech;
      reply_audio.play()

      received(robot[cnt].sentence)
      change_mood(iframe1.getElementById("mood"), robot[cnt].emotion, "frame1");
      window.frames[0].sendEmotion(robot[cnt].emotion);

      reply_audio.addEventListener('ended', function() {
        cnt++;

        if(cnt < robot.length)
        {
          reply_audio.src = robot[cnt].speech;
          reply_audio.play()

          received(robot[cnt].sentence)
          change_mood(iframe1.getElementById("mood"), robot[cnt].emotion, "frame1");
          window.frames[0].sendEmotion(robot[cnt].emotion);
        }

        if(cnt >= robot.length)
          document.getElementById("form-control").disabled = false;
      }, false);
    };  // }
  })
}

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return null;
}
// music(robot, 0)
// function music(robot, index){
//   if (index < robot.length){
//     let reply_audio = new Audio()
//     reply_audio.src = robot[index].speech;
//     reply_audio.play()
//     reply_audio.addEventListener("ended", () => {
//       music(robot, index++)
//     })
//   }
// }

document.querySelector('textarea').addEventListener('input', function (event) {
  const iframe1 = window.frames[0].document;
  const iframe2 = window.frames[1].document;

  change_mood(iframe1.getElementById("mood"), 'Idle', "frame1");
  change_mood(iframe2.getElementById("mood"), 'Idle', "frame2");

  window.frames[0].sendEmotion('Idle');
  window.frames[1].sendEmotion('Idle');
});


function change_mood(moodEl, mood, frame)
{
  let moodList = moodEl.getElementsByTagName("li")

  if (frames_oldSelectIndex_mood[frame] != null && mood != moodEl.children[frames_oldSelectIndex_mood[frame]].innerHTML) // 刪除前個 motion 的 select
    moodEl.children[frames_oldSelectIndex_mood[frame]].classList.remove("selected")

  for(let i=0; i < moodList.length; i++)
  {
    if(moodList[i].innerHTML == mood)
    {
      moodList[i].classList.add("selected");
      frames_oldSelectIndex_mood[frame] = i;
    }
  }
}

function outgoing()
{
  if(document.getElementById("form-control").value != "")
  {
    console.log(document.getElementById("form-control").value)

    let node1 = document.createElement('div');
    node1.setAttribute("class", "outgoing-chats");

    let node2 = document.createElement('div');
    node2.setAttribute("class", "outgoing-chats-msg");

    let node3 = document.createElement('div');
    node3.setAttribute("class", "outgoing-chats-time");

    let node4 = document.createElement('div');
    node4.setAttribute("class", "text");

    let node5 = document.createElement('div');
    node5.setAttribute("class", "outgoing-chats-inbox");

    let node6 = document.createElement('p');
    node6.innerHTML=document.getElementById("form-control").value;

    node4.innerHTML="11:0.PM";

    // node3.appendChild(node4)
    node5.appendChild(node6)
    node2.appendChild(node3)
    node2.appendChild(node5)
    // node3.appendChild(node5)
    add_chat.appendChild(node1).appendChild(node2)
    add_chat.scrollTop = add_chat.scrollHeight;

    text_api(document.getElementById("form-control").value);
    document.getElementById("form-control").value = "";
  }
}

function received(content)
{
  let node1 = document.createElement('div');
  node1.setAttribute("class", "received-chats");

  let node2 = document.createElement('div');
  node2.setAttribute("class", "received-chats-img");

  let node3 = document.createElement('img');
  node3.src = "img/model.png";

  let node4 = document.createElement('div');
  node4.setAttribute("class", "received-msg");

  let node5 = document.createElement('div');
  node5.setAttribute("class", "received-msg-inbox");

  let node6 = document.createElement('p');
  node6.innerHTML=content;

  let node7 = document.createElement('div');
  node7.setAttribute("class", "received-time");

  let node8 = document.createElement('div');
  node8.setAttribute("class", "text");
  node8.innerHTML="11:0.PM";

  node2.appendChild(node3);
  node4.appendChild(node5).appendChild(node6);
  // node7.appendChild(node8);
  node1.appendChild(node2);
  node1.appendChild(node4);
  node1.appendChild(node7);
  add_chat.appendChild(node1);

  add_chat.scrollTop = add_chat.scrollHeight;
}

document.querySelector('textarea').addEventListener('input', function (event) {
  console.log("qqqqqqqqqqqqqqq");
});
