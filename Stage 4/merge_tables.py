import pandas as pd

'''Rules:
save id from songs table as song_id
save id from tracks table as track_id
save title from tracks table
save artists name from whichever is long
save song from tracks if there else title
from songs
save year from songs
save episode from tracks
save episode year from tracks
'''
def apply_rules(tup1, tup2):
    song_id = tup1['id'].iloc[0]
    track_id = tup2['id'].iloc[0]
    title = tup2['title'].iloc[0]
    tup2_artist = tup2['artists'].iloc[0]
    tup1_artist = tup1['artist_name'].iloc[0]
    if len(tup2_artist) >= len(tup1_artist):
    	artists = tup2_artist
    else:
        artists = tup1_artist
    tup2_song = tup2['song'].iloc[0]
    tup1_song = tup1['title'].iloc[0]
    if len(str(tup2_song)) >= len(tup1_song):
        song = tup2_song
    else:
        song = tup1_song 
    year = tup1['year'].iloc[0]
    episode = tup2['episode'].iloc[0]
    episode_year = tup2['year'].iloc[0]

    data = [{'song_id':song_id, 'track_id':track_id, 'title':title, \
	    'artists':artists, 'song':song , \
            'year':year, 'episode':episode, 'episode_year':episode_year}]
    return data

def save_to_csv(merged):
	merged.to_csv('./merged.csv', index=False)

'''create a schema as union of both tables
For the true matches we found in Linear regression
find corresponding tables from songs and tracks table.
Apply rules to combine the common attributes.
Write the final merged table as merged.csv
'''
def merge_table(table1, table2, matcher):
    schema = ['song_id', 'track_id', 'title', 'artists', 'song', 'year',\
	      'episode', 'episode_year']
    merged_table = pd.DataFrame(columns=schema)
    for index, match in matcher.iterrows():
	if match['logistic regression'] == 1:
        	tup_table1 = table1.loc[table1.id == match['ltable_id']]
		tup_table2 = table2.loc[table2.id == match['rtable_id']]
		data = apply_rules(tup_table1, tup_table2)
		df = pd.DataFrame(data, columns=schema)
		merged_table = merged_table.append(df)
    save_to_csv(merged_table)

if __name__ == '__main__':
    '''Read downsampled files and matcher
    sampleA - downsampled song dataset
    sampleB - downsampled tracks dataset
    Matches - Our matcher's output
    '''
    table1 = pd.read_csv('./sampleA.csv', index_col=False)
    #if pandas version more than 0.17 use table1.sort_values(by=['id'], ascending=True)
    table1.sort('id', ascending=True, inplace=True)
    table2 = pd.read_csv('./sampleB.csv', index_col=False)
    table2.sort('id', ascending=True, inplace=True)
    matcher = pd.read_csv('./Matches_Cleaned.csv', index_col=False)
    matcher.sort('ltable_id', ascending=True, inplace=True)
    merge_table(table1, table2, matcher)
	
