function cookiereader() {
    let cookies = {};
    // 既存のCookieを解析
    document.cookie.split(";").forEach(cookie => {
        const [key, value] = cookie.split("=");
        cookies[key.trim()] = value;
    });

    // searchaorb キーの確認と設定
    if (!cookies.hasOwnProperty('searchaorb')) {
        cookies['searchaorb'] = 'b';
        let expirationDate = new Date();
        expirationDate.setFullYear(expirationDate.getFullYear() + 1); // 1年後に有効期限を設定
        document.cookie = 'searchaorb=b; expires=' + expirationDate.toUTCString() + '; path=/';
    }

    return cookies;
}

function cookiewriter(targetList) {
    let cookies = {};
    targetList.forEach(key => {
        const checkbox = document.getElementById(key);
        if (checkbox) {
            cookies[key] = checkbox.checked ? 1 : 0;
        }
    });

    let expirationDate = new Date();
    expirationDate.setFullYear(expirationDate.getFullYear() + 1); // 1年後に有効期限を設定
    let expires = "expires=" + expirationDate.toUTCString();

    for (let [key, value] of Object.entries(cookies)) {
        document.cookie = `${key}=${value}; ${expires}; path=/`;
    }
}

function swsetter(targetList, cookies, defo) {
    targetList.forEach((id, index) => {
        const element = document.getElementById(id);
        if (element) {
            // Cookieに値があればそれを使用し、なければdefoからデフォルト値を取得
            element.checked = (typeof cookies[id] !== "undefined") ? (cookies[id] == 1) : defo[index];
        }
    });
}


function itemfilter(anitem, keyword, trigger) {
    if (!anitem || keyword === "" || !trigger) {
        console.log("itemfilter: true");
        return true;
    }
    return anitem.indexOf(keyword) !== -1;
}

function allfilter(anitem, keyword, trigger) {
    if (!anitem || keyword === "" || !trigger) {
        console.log("allfilter: true");
        return true;
    }
    let regex = new RegExp(keyword);
    console.log(regex);
    return Object.values(anitem).some(value => regex.test(value));
}

function dictioner(anitem, dict, trigger) {
    if (trigger) {
        for (let key in dict) {
            if (anitem.includes(key)) {
                anitem = anitem.replace(key, dict[key]);
            }
        
        }
    }
    return anitem;
}