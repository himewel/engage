import json
import os
import subprocess

import pandas as pd
import requests

_API_URL = "https://87dyrojjxk.execute-api.us-east-1.amazonaws.com/dev/fiap/raw"

schema = {
    "rounds": ["roundid", "name", "roundscorebonus"],
    "activities": ["activityid", "roundid", "activityweight"],
    "answers": [
        "activityid",
        "userid",
        "scoreofaccuracy",
        "answerdatetime",
        "approved",
    ],
    "users": ["userid", "groupid", "image", "username"],
    "groups": ["groupid", "groupname"],
}


def transform_data():
    res = requests.get(_API_URL)
    data = json.loads(res.text)

    users_list = []
    rounds_list = []
    activities_list = []
    answers_list = []
    for user_item in data:
        userid = user_item["userid"]

        for round_item in user_item["rounds"]:
            for activity_item in round_item.get("activities"):
                for answer_item in activity_item.get("answers"):
                    answers_list.append(answer_item)

                activity_item["roundId"] = round_item["roundId"]
                del activity_item["answers"]
                activities_list.append(activity_item)

            round_item["userid"] = userid
            del round_item["activities"]
            rounds_list.append(round_item)

        del user_item["rounds"]
        users_list.append(user_item)

    users_df = pd.DataFrame(users_list)
    rounds_df = pd.DataFrame(rounds_list)
    activities_df = pd.DataFrame(activities_list)
    answers_df = pd.DataFrame(answers_list)

    users_df["userid"] = users_df["userid"].astype(int)
    rounds_df["userid"] = rounds_df["userid"].astype(int)

    full_df = users_df.merge(right=rounds_df, on="userid", how="left")
    full_df = full_df.merge(
        right=activities_df,
        left_on=["roundId", "userid"],
        right_on=["roundId", "ID_USUARIO"],
        how="left",
    )
    full_df = full_df.merge(
        right=answers_df,
        on=["ID_USUARIO", "ID_ATIVIDADE"],
        how="left",
    )

    full_df["groupid"] = full_df["userid"] % 2
    full_df["groupname"] = full_df["groupid"].apply(
        lambda x: "Evens" if x == 0 else "Odds"
    )
    full_df["username"] = "User " + full_df["userid"].astype(str)
    return full_df


def fix_dtypes(df):
    bool_columns = [
        "waiting",
        "showstars",
        "showscore",
        "approved",
        "myranking",
        "userstatus",
    ]
    bool_columns = [column for column in bool_columns if column in df.columns]
    if bool_columns:
        df[bool_columns] = df[bool_columns].astype(bool)

    float_columns = ["maxscore", "score"]
    float_columns = [column for column in float_columns if column in df.columns]
    if float_columns:
        df[float_columns] = df[float_columns].astype(float)

    datetime_columns = ["answerdatetime"]
    datetime_columns = [column for column in datetime_columns if column in df.columns]
    if datetime_columns:
        for column in datetime_columns:
            df[column] = pd.to_datetime(df[column], infer_datetime_format=True)

    int_columns = [
        "position",
        "roundid",
        "roundscorebonus",
        "stars",
        "activityid",
        "userid",
    ]
    int_columns = [column for column in int_columns if column in df.columns]
    if int_columns:
        for name in int_columns:
            df[name] = df[name].astype(str)
            df[name] = df[name].str.replace("\.0", "", regex=True)
            df[name] = df[name].astype(int)
    return df


def rename_columns(df):
    df = df.drop("ID_USUARIO", axis=1)
    columns_to_rename = {
        "ID_ATIVIDADE": "activityid",
        "NU_PESO": "activityweight",
        "DT_RESPOSTA": "answerdatetime",
        "NU_PORCENTAGEM_ACERTOS": "scoreofaccuracy",
    }
    lower_case_columns = {name: name.lower() for name in df.columns}
    df.rename(columns=dict(lower_case_columns, **columns_to_rename), inplace=True)
    return df


def split_files(df):
    csv_path = os.getenv("CSV_PATH", ".")
    os.makedirs(csv_path, exist_ok=True)

    for key, columns in schema.items():
        tmp_df = df[columns].copy()
        tmp_df.drop_duplicates(keep="last", inplace=True)

        if key in ["activities", "answers"]:
            tmp_df.dropna(subset=["activityid"], inplace=True)
        if key == "answers":
            tmp_df.dropna(subset=["answerdatetime"], inplace=True)

        tmp_df = fix_dtypes(tmp_df)
        tmp_df.to_csv(f"{csv_path}/{key}.csv", index=False, header=False)


def ingest_data():
    csv_path = os.getenv("CSV_PATH", ".")

    for key in schema.keys():
        bash_command = f"""
            /opt/mssql-tools/bin/bcp \
                 db.{key} in {csv_path}/{key}.csv \
                 -q -c -t , \
                 -S ${{MSSQL_HOST}} \
                 -U ${{MSSQL_USER}} \
                 -P ${{MSSQL_PASSWD}}
        """

        process = subprocess.Popen(bash_command, shell=True, stdout=subprocess.PIPE)
        result, error = process.communicate()
        print(result.decode("utf-8"))
        if process.returncode != 0:
            raise Exception(
                f"BCP insert failed {process.returncode} {error.decode('utf-8')}"
            )


if __name__ == '__main__':
    df = transform_data()
    df = rename_columns(df)
    split_files(df)
    ingest_data()
