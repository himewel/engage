db.userScores.aggregate([
    {
        $group: {
            _id: { groupId: "$_id.groupId" },
            groupScore: { $sum: "$roundScores.roundScore" }
        }
    },
    { $merge: { into: "groupScores", on: ["_id"] } }
]);
