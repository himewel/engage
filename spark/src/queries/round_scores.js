db.rounds.aggregate([
    {
        $lookup: {
            from: "activityScores",
            localField: "roundId",
            foreignField: "_id.roundId",
            as: "activityScores"
        }
    },
    { $unwind: { path: "$activityScores" } },
    {
        $group: {
            _id: {
                roundId: "$activityScores._id.roundId",
                userId: "$activityScores._id.userId",
                roundScoreBonus: "$roundScoreBonus",
                roundName: "$roundName"
            },
            sumScores: { $sum: "$activityScores.activityScore" },
            sumWeights: { $sum: "$activityScores.activityWeight" }
        }
    },
    {
        $project: {
            _id: {
                userId: "$_id.userId",
                roundId: "$_id.roundId"
            },
            roundName: "$_id.roundName",
            roundScore: {
                $cond: [
                    {
                        $or: [
                            { $eq: ["$sumScores",  0 ] },
                            { $eq: ["$sumWeights", 0 ] },
                        ]
                    },
                    0,
                    {
                        $multiply: [
                            { $divide: ["$sumScores", "$sumWeights"] },
                            "$_id.roundScoreBonus"
                        ]
                    }
                ]
            }
        }
    },
    { $merge: { into: "roundScores", on: ["_id"] } }
]);