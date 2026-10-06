// 엘리먼트(요소) 얻기
const code = document.querySelector("#code");
const sang = document.querySelector("#sang");
const su = document.querySelector("#su");
const dan = document.querySelector("#dan");

const msg = document.querySelector("#msg");
const tbody = document.querySelector("#tbody");

const btnAdd = document.querySelector("#btnAdd");
const btnUpdate = document.querySelector("#btnUpdate");
const btnDelete = document.querySelector("#btnDelete");

function setMsg(text){
    msg.textContent = text;
}

// 입력 폼 초기화
function clearForm(){
    code.value = "";
    sang.value = "";
    su.value = "";
    dan.value = "";

    code.focus();
}

// 전체 자료 읽기 - 시작시, 추가후 실행
async function loadAll(){
    const res = await fetch("/api/sangdata",{
        method:"GET"     // 전체 자료 조회
    });
    const result_datas = await res.json();
    //console.log(datas);
    //alert(datas);

    tbody.innerHTML = "";

    result_datas.datas.forEach(r => {
        const tr = document.createElement("tr");
        tr.innerHTML = "<td>" + r.code + "</td>" + 
            "<td>" + r.sang + "</td>" +
            "<td>" + r.su + "</td>" +
            "<td>" + r.dan + "</td>";
        tbody.appendChild(tr);
    });
    
    clearForm();
    setMsg("조회 완료");
}

// 상품 추가
async function addData(){
    // alert("add");
    // 입력자료 검사가 끝났다고 가정하고 아래 문장 실행

    const add_data = {
        code:code.value,
        sang:sang.value,
        su:Number(su.value),
        dan:Number(dan.value)
    }
    //alert(add_data);
    //alert(JSON.stringify(add_data))  // JS객체를 JSON문자열로 변환
    const res = await fetch("/api/sangdata", {
        method:"POST",   // 자료 추가
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify(add_data)   // JS객체를 JSON문자열로 변환해 서버로 전송
    })

    await res.json();
    setMsg("추가 완료");
    clearForm();

    loadAll();   // 추가 후 전체 자료 보기
}

// 상품 수정
async function updateData(){
    // 입력자료 검사가 끝났다고 가정하고 아래 문장 실행
    const up_data = {
        sang:sang.value,
        su:Number(su.value),
        dan:Number(dan.value)
    }

    const res = await fetch("/api/sangdata/" + code.value, {
        method:"PUT",   // 자료 수정
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify(up_data)
    })

    const imsi = await res.json();
    if(imsi.ok)
        setMsg("수정 완료");
    else
        setMsg("수정 실패");

    clearForm();

    loadAll();   // 수정 후 전체 자료 보기
}

// 상품 삭제
async function deleteData(){
    if(!code.value.trim()){
        alert("삭제할 상품 코드를 입력하세요");
        code.focus();
        return;
    }

    const res = await fetch("/api/sangdata/" + code.value, {
        method:"DELETE"   // 자료 삭제
    });

    const imsi = await res.json();
    if(imsi.ok)
        setMsg(imsi.msg);
    else
        setMsg("삭제 오류 : " + imsi.msg);

    clearForm();
    loadAll();   // 삭제 후 전체 자료 보기
}

// 함수 호출
window.onload = loadAll;
btnAdd.onclick = addData;
btnUpdate.onclick = updateData;
btnDelete.onclick = deleteData;