norm = require("votes/lib/normal")

function (doc) {
    if (doc && doc.votes) {
        let vs = norm(doc.votes)
        emit(doc._id, vs)
    }
}
