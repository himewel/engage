db.activities.aggregate([
    {
        $lookup: {
            from: "answers",
            localField: "activityId",
            foreignField: "activityId",
            as: "answers"
        }
    },
    { $unwind: { path: "$answers" } },
    {
        $group: {
            _id: {
                userId: "$answers.userId",
                activityId: "$answers.activityId",
                roundId: "$roundId",
                activityWeight: "$activityWeight"
            },
            maxScore: { $max: "$answers.scoreOfAccuracy" }
        }
    },
    {
        $project: {
            _id: {
                userId: "$_id.userId",
                activityId: "$_id.activityId",
                roundId: "$_id.roundId"
            },
            activityScore: {
                $multiply: ["$maxScore", "$_id.activityWeight"]
            },
            activityWeight: "$_id.activityWeight"
        }
    },
    { $merge: { into: "activityScores", on: ["_id"] } }
]);
