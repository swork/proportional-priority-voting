function (votes) {
    let vs = {}
    let total = 0
    for (const item of Object.keys(votes)) {
        console.log(votes[item])
        if (votes[item] === 0) {
            continue
        }
        vs[item] = votes[item]
        total = total + votes[item]
    }

    let adjust = 100 / total;
    console.log(adjust)
    let vs2 = {}
    for (const item of Object.keys(vs)) {
        console.log(vs[item] * adjust)
        vs2[item] = Math.floor(vs[item] * adjust)
    }
    return vs2
}
