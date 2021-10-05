db.users.aggregate([
    {
        $lookup: {
            from: "roundScores",
            localField: "userId",
            foreignField: "_id.userId",
            as: "roundScores"
        }
    },
    { $unwind: { path: "$roundScores" } },
    {
        $lookup: {
            from: "groups",
            localField: "groupId",
            foreignField: "groupId",
            as: "groups"
        }
    },
    { $unwind: { path: "$groups" } },
    {
        $project: {
            _id: {
                userId: "$roundScores._id.userId",
                roundId: "$roundScores._id.roundId",
                groupId: "$groupId"
            },
            groupName: "$groups.groupName",
            userName: "$userName",
            image: "$image"
            roundScores: "$roundScores",
        }
    },
    { $merge: { into: "userScores", on: ["_id"] } }
]);
