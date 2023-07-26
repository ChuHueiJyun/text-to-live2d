let motionEl = document.getElementById("motions");
let moodEl = document.getElementById("mood");
let moodList = moodEl.getElementsByTagName("li")
var mysentence = []; // 存故事句子
var mymood = []; // 存故事情緒
let oldSelectIndex = null;
const moodGroup =  ["Idle","happy", "sad", "anger", "surprised", "fearful"];
let motionGroupList = [];
let playMotion = ""

moodList[0].classList.add("selected");

function mood_motion(mood)
{
  let feel = mood
  const moods = motionGroupList[moodGroup.indexOf(feel)]

  for(let i=0;i < motionEl.children.length;i++)
  {
    const children_el = motionEl.children[i];
    children_el.classList.remove("color");

    if (moods.includes(children_el.innerHTML) && children_el.innerHTML != playMotion)
      children_el.classList.add("color");

  }
}

/**
 * 取得所有 motion 名稱並生成列表
 * @param {list} AllMotionFileName motion list
 * @param {list} motionGroup motionGroup list
 */
function getAllMotionFileName(AllMotionFileName, motionGroup)
{
  var childs = motionEl.lastElementChild;

  while(childs)
  {
    motionEl.removeChild(childs);
    childs=motionEl.lastElementChild;
  }

  motionGroupList = motionGroup;

  for(let i=0; i < AllMotionFileName.length; i++)
  {
    const children = document.createElement("li");

    children.innerHTML = AllMotionFileName[i];
		motionEl.append(children);
  }
}

/**
 * 從 lappmodel.ts 取得正在執行的 motion 名稱
 * @param {string} MotionFileName 執行的 motion 名稱
 * @param {string} SentenceMood 將句子情緒傳給 lappmodel.ts
 */
function getSelectMotionFileName(MotionFileName)
{
  playMotion = MotionFileName;

  if (oldSelectIndex != null && MotionFileName != motionEl.children[oldSelectIndex].innerHTML) // 刪除前個 motion 的 select
    motionEl.children[oldSelectIndex].classList.remove("selected")

  // 將正在執行的 motion 加入 select
  for (var i = 0;i <motionEl.children.length;i++)
  {
    if (MotionFileName == motionEl.children[i].innerHTML)
    {
      motionEl.children[i].classList.add("selected");
      oldSelectIndex = i;
    }
  }
}
