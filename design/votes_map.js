function (doc) {
    norm = require("views/lib/normal").proportionalize_votes

    if (doc && doc.votes) {
        let votes = norm(doc.votes)
        for (const item of Object.keys(votes)) {
            emit(item, votes[item])
        }
    }
}
