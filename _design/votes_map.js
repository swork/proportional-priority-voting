norm = require("votes/lib/normal")

function (doc) {
    if (doc && doc.votes) {
        let vs = norm(doc.votes)
        for (const [item, rank] of vs) {
            emit(item, rank)
        }
    }
}
