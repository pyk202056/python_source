// 자료 추가시 입력 자료 검증
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("addForm");

    if (!form) return;

    form.addEventListener("submit", (e) => {
        // alert("ok");
        const sang = document.getElementById("sang").value.trim();
        const su = document.getElementById("su").value.trim();
        const dan = document.getElementById("dan").value.trim();
        
        // 1) 필수 입력 체크
        if(sang === ""){
            alert("상품명을 입력하세요");
            document.getElementById("sang").focus();
            e.preventDefault();
            return;
        }

        // 숫자 체크 (정규 표현식)
        if(!/^\d+$/.test(su)){     // 정규표현식.test(검사할대상)
            alert("수량은 숫자만 허용");
            document.getElementById("su").focus();
            e.preventDefault();
            return;
        }
        if(!/^\d+$/.test(dan)){
            alert("단가는 숫자만 허용");
            document.getElementById("dan").focus();
            e.preventDefault();
            return;
        }
    });
})