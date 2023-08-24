import pandas as pd

# file open function 
def file_open(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(e)

df1 = file_open(r"D:\imp\Projects\ipl_analysis\ipl_datasets\ipl1.csv")
df2 = file_open(r"D:\imp\Projects\ipl_analysis\ipl_datasets\ipl1.csv")

batter = df1["batter"].unique().tolist()

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
