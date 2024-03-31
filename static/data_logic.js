function resParse(res) {
    //console.log(res);
    const json_data = res.split('\n');
    //console.log(json_data)

    const date = json_data[0].split('\t')[0];
    const valid = json_data[0].split('\t')[1];
    const header = json_data[1].split('\t');
    // console.log(header)
    // console.log(date)
    // console.log(valid)

    const data = [];
    for (let i = 2; i < json_data.length; i++) {
        const row = json_data[i].split('\t');
        const obj = {};
        for (let j = 0; j < header.length; j++) {
            obj[header[j]] = row[j];
        }
        data.push(obj);
    }
    console.log(data)
    return {date: date, data: data, valid: valid, header: header};
}

function dictioner (hikisu, dict, bool) {
    if (bool) {
        return dict[hikisu];
    } else {
        return hikisu;
    }
}   

