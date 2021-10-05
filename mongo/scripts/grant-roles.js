db.runCommand({
    createRole: "listDatabases",
    privileges: [
        { resource: { cluster : true }, actions: ["listDatabases"]}
    ],
    roles: []
});

db.createUser({
    user: "debezium",
    pwd: "debezium",
    roles: [
        { role: "readWrite", db: "engagedb" },
        { role: "read", db: "local" },
        { role: "listDatabases", db: "admin" },
        { role: "read", db: "config" },
        { role: "read", db: "admin" }
    ]
});
