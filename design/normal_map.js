
function (doc) {
    norm = require("views/lib/normal").proportionalize_votes
    log(norm)
    log(doc.votes)
    if (doc && doc.votes) {
        let vs = norm(doc.votes)
        log(vs)
        emit(doc._id, vs)
    }
}
