import pandas as pd

pd.set_option('display.max_colwidth', None)

# Read in a siegfried CSV
df = pd.read_csv("mc00685_optical_sha256.csv", delimiter=",")

df1 = df['filename'].str.split('/').str[4].to_frame()
df1.rename(columns={'filename': 'directory'}, inplace=True)
df2 = df['sha256']
df3 = df1.join(df2)

# Add column for duplicate where yes = 1
df3['duplicate'] = df3['sha256'].duplicated(keep=False).astype(int)

# Get number of dupes for each dir
number_dupes = df3.groupby('directory')['duplicate'].sum()
# Get number of files in each dir
number_files = df3.groupby(df3['directory']).size()
# Calculate percentage of dupes
dupe_percents = (round(((number_dupes/number_files)*100), 1)).reset_index(name='dupe percentages')
# Add number of dupes and files as two columns
dupe_percents['number of dupes'] = (number_dupes.reset_index(name='number of dupes'))['number of dupes']
dupe_percents['number of files'] = (number_files.reset_index(name='number of files'))['number of files']
# Sort percentages in descending order
dupe_percents.sort_values(by=['dupe percentages'], inplace=True, ascending=False)

# See if directory exists in CSV listing SCPS dirs
df_scps = pd.read_csv("scps.csv")
dupe_percents['in SCPS'] = dupe_percents['directory'].isin(df_scps['filename'])

print(dupe_percents)
# Save as CSV
dupe_percents.to_csv('hall_optical_dupe_percents.csv', index=False)