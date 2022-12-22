function proportionalize_votes(votes) {
    let vs = {}
    let total = 0
    for (const item of Object.keys(votes)) {
        log(votes[item])
        if (votes[item] === 0) {
            continue
        }
        vs[item] = votes[item]
        total = total + votes[item]
    }

    let adjust = 100 / total;
    log(adjust)
    let vs2 = {}
    for (const item of Object.keys(vs)) {
        log(vs[item] * adjust)
        vs2[item] = Math.floor(vs[item] * adjust)
    }
    return vs2
}

exports['proportionalize_votes'] = proportionalize_votes
