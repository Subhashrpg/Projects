import pandas as pd

# file open function 
def file_open(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(e)

df1 = pd.read_csv(r"D:\imp\Projects\ipl_analysis\ipl_datasets\ipl1.csv",usecols=["ID","ballnumber","batter","bowler","batsman_run","isWicketDelivery","player_out","kind","BattingTeam"])
df2 = pd.read_csv(r"D:\imp\Projects\ipl_analysis\ipl_datasets\ipl2.csv",usecols = ["ID","City","Season","MatchNumber","Team1","Team2","WinningTeam","Player_of_Match"])
batter = df1["batter"].unique().tolist()
bowler = df1["bowler"].unique().tolist()


# batter's performance analysis
def batsman_analysis(batter):
    batsman_runs = df1[df1["batter"] == batter]["batsman_run"].sum()
    temp_df = df1[(df1["batsman_run"] == 4) | (df1["batsman_run"] == 6)]
    fours = temp_df[temp_df["batter"] == batter].groupby(["batter","batsman_run"])["batsman_run"].count().unstack()[4].values[0]
    sixes = temp_df[temp_df["batter"] == batter].groupby(["batter","batsman_run"])["batsman_run"].count().unstack()[6].values[0]
    total_balls = df1[df1["batter"] == batter].groupby(["batter"])["batsman_run"].count().values[0]
    strike_rate = round((batsman_runs/total_balls)*100,2)
    highest_score = df1[df1["batter"] == batter].groupby("ID")["batsman_run"].sum().max()
    match = len(df1[df1["batter"] == batter].groupby("ID")["batter"].count().index.tolist())
    new_df = df1[df1["batter"] == batter].groupby("ID")["batsman_run"].sum().reset_index()
    fifties = new_df.query("batsman_run >= 50 and batsman_run < 100")["batsman_run"].count()
    hundreds = new_df.query("batsman_run >= 100")["batsman_run"].count()
    avg_score = round(batsman_runs/match,2)

    data = {"Match": match, "Runs":batsman_runs,"HS": highest_score,"Avg": avg_score,"Strike_rate":strike_rate,"100": hundreds,"50": fifties,"4s": fours,"6s":sixes}
    batsman_df = pd.DataFrame(data, index = [batter])
    return batsman_df

def batsman_overall(batter):
    df1[["ID","batter","batsman_run","BattingTeam"]]

    final_df = df1.merge(df2, on = "ID")[["ID","batter","batsman_run","Team1","Team2","BattingTeam"]]
    new_df = final_df[final_df["batter"] == batter]

    batsman_team = new_df["BattingTeam"].values[0]
    yb = new_df[new_df["Team1"] == batsman_team].loc[:,["Team1","Team2"]]
    tm1 = yb.shift(-1,axis = 1)["Team1"].values
    yb1 = new_df[new_df["Team2"] == "Rajasthan Royals"].loc[:,["Team1","Team2"]]
    tm2 = yb1.shift(1,axis = 1)["Team2"].values
    new_df.loc[yb.index,["Team1"]] = tm1
    new_df.loc[yb1.index,["Team2"]] = tm2

    overall = new_df.groupby(["batter","Team1"])["batsman_run"].sum().sort_values(ascending = False).reset_index()
    balls = new_df.groupby(["batter","Team1"])["batsman_run"].count().reset_index().rename(columns = {"batsman_run":"balls"})

    four_df = new_df[(new_df["batsman_run"] == 4)]
    fours = four_df.groupby(["Team1"])["batsman_run"].count().reset_index().rename(columns = {"batsman_run":"4s"})
    six_df = new_df[(new_df["batsman_run"] == 6)]
    sixes = six_df.groupby(["Team1"])["batsman_run"].count().reset_index().rename(columns = {"batsman_run":"6s"})
    six_fours = sixes.merge(fours, on = "Team1")

    hundred_df = new_df.groupby(["ID","Team1"])["batsman_run"].sum().reset_index()
    hundreds = hundred_df[hundred_df["batsman_run"] >= 100].groupby(["Team1"])["batsman_run"].count().reset_index()
    fifties = hundred_df[(hundred_df["batsman_run"] >= 50) & (hundred_df["batsman_run"] < 100)].groupby(["Team1"])["batsman_run"].count().reset_index()
    fifties.rename(columns = {"batsman_run": "50"}, inplace = True)
    hundreds.rename(columns = {"batsman_run": "100"},inplace = True)
    hundred_fifties = fifties.merge(hundreds, on = "Team1", how = "left").fillna(0)

    matches = new_df.groupby(["ID","Team1"])["batter"].count().reset_index()["Team1"].value_counts().reset_index().rename(columns = {"index":"Team1","Team1":"Match"})
    max_score = new_df.groupby(["ID","Team1"])["batsman_run"].sum().reset_index().groupby("Team1")["batsman_run"].max().reset_index()
    max_score.rename(columns= {"batsman_run":"HS"}, inplace = True)

    overall = overall.merge(matches, on = "Team1").merge(max_score, on = "Team1").merge(balls, on = ["batter","Team1"])
    overall = overall.merge(hundred_fifties, on = "Team1", how = "left").merge(six_fours, on = "Team1", how = "left")

    overall["strike_rate"] =  round((overall["batsman_run"]/overall["balls"])*100,2)
    overall["average"] =  round(overall["batsman_run"]/overall["Match"],2)
    overall.fillna(0,inplace = True)

    overall["50"] = overall["50"].astype("int")
    overall["100"] = overall["100"].astype("int")
    overall["6s"] = overall["6s"].astype("int")
    overall["4s"] = overall["4s"].astype("int")
    overall.drop(columns= ["batter","balls"], inplace = True)
    overall.rename(columns= {"Team1":"Teams"}, inplace = True)
    overall.rename(columns= {"batsman_run":"Runs"}, inplace = True)
    overall.set_index("Teams", inplace = True)

    overall = overall.iloc[:,[1,0,2,8,7,3,4,6,5]]
    return overall

def bowler_analysis(bowler):
    pass
