let rst = {
    "_id": "debezium",
    "members": [
        {
            "_id": 0,
            "host": "mongodb:27017",
            "priority": 2
        },
        {
            "_id": 1,
            "host": "mongodb-rs:27017",
            "priority": 1
        }
    ]
}

rs.initiate(rst, { force: true });
rs.conf();
rs.printSecondaryReplicationInfo();
