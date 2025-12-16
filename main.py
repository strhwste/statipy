import time
import traceback
import sys
import csv
from io import StringIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from filemgr import load_zipped_data
from stats import (
    history_range, play_time, play_counts, play_counts_by_artist, play_counts_by_album,
    artist_history_over_time, platform_usage, listening_by_hour, skipped_ratio,
    location_counts, most_skipped_artist, most_skipped_track, longest_played_artist, top_artist_per_month,
    listening_by_day_of_week, discovery_rate, seasonal_listening, one_hit_wonders, day_night_split, longest_listening_streak,
    true_skip_rate, most_consecutive_plays, album_loyalty, longest_artist_relationship, forgotten_favorites, hourly_heatmap_data,
    most_musical_day, weekend_vs_weekday, immediate_skips, variety_score,
    listening_velocity, the_comeback, clockwork_artists, session_analysis, skipless_albums, sampler_vs_completionist,
    commute_heroes, marathon_tracks, one_week_wonders, sound_of_silence,
    calendar_heatmap_data, picky_grid_data, device_habits_data, artist_eras_data,
    control_freak_data, shuffle_paradox_data, natural_death_data,
    active_listening_heatmap_data, active_listening_trend_data,
    get_artist_traits,
    night_shift_artists, new_years_transitions, consistency_king, alphabet_challenge, longest_played_tracks,
    obsession_score, early_bird_artists, nine_to_five_artists, party_animal_tracks, sunday_scaries_tracks,
    unskippable_streak, artist_hopper, discovery_peak, comfort_zone, single_day_record,
    manual_laborer, shuffle_roulette, session_starter, session_closer, quick_fix, skippers_remorse,
    remix_junkie, live_fanatic, short_king, epic_saga, collaborator, alphabet_artists, spelling_bee, same_name_game,
    midnight_club, lunch_break, monday_blues, hump_day_hero, quarterly_review, album_purist,
    instant_skips, get_full_song_stats
)
from stats.graphs import (
    plot_top_items, plot_artist_trends, plot_platform_usage, plot_listening_by_hour,
    plot_location_counts, plot_longest_played_artist, plot_skipped_items,
    plot_listening_by_day_of_week, plot_discovery_rate, plot_seasonal_listening, plot_day_night_split, plot_hourly_heatmap,
    plot_variety_score,
    plot_calendar_heatmap, plot_picky_grid, plot_device_habits, plot_artist_eras,
    plot_active_heatmap, plot_active_trend,
    plot_artist_radar,
    create_text_pages,
    plot_longest_played_tracks,
    plot_comfort_zone
)

class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
    def flush(self):
        for f in self.files:
            f.flush()

if __name__ == '__main__':
    try:
        print('Loading data... \n')
        DATA = load_zipped_data()
        start, end = history_range(DATA.streaming_history)

        temp_start = input('Starting date (empty for earliest, otherwise in the form of <yyyy-mm-dd HH:MM>): \n -> ')
        temp_end = input('End date (empty for latest, otherwise in the form of <yyyy-mm-dd HH:MM>): \n -> ')
        print('\n')

        start = start if temp_start == '' else temp_start
        end = end if temp_end == '' else temp_end

        # Start capturing output
        captured_output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = Tee(sys.stdout, captured_output)

        print(f' ===> Statistics from [{time.strftime("%Y-%m-%d %H:%M", start)}] to [{time.strftime("%Y-%m-%d %H:%M", end)}]: \n')

        total_time = play_time(DATA.streaming_history, start, end)

        print(f'Total Play Time:')
        print(f'{total_time!s}  or {int(total_time.total_seconds() / 60)} minutes')
        print('\n')

        # Tracks
        track_counts = play_counts(DATA.streaming_history)
        print('Top Played Tracks:')
        for i, k, v in zip(range(1, 101), track_counts.keys(), track_counts.values()):
            print(f'#{i:2} - {v:4} : {k}')
        print('\n')

        # Artists
        artist_counts = play_counts_by_artist(DATA.streaming_history)
        print('Top Played Artists:')
        for i, k, v in zip(range(1, 101), artist_counts.keys(), artist_counts.values()):
            print(f'#{i:2} - {v:4} : {k}')
        print('\n')

        # Albums
        album_counts = play_counts_by_album(DATA.streaming_history)
        print('Top Played Albums:')
        for i, k, v in zip(range(1, 101), album_counts.keys(), album_counts.values()):
            print(f'#{i:2} - {v:4} : {k}')
        print('\n')

        # Location
        locations = location_counts(DATA.streaming_history)
        print('Top Locations:')
        for k, v in locations.items():
            print(f'{k}: {v}')
        print('\n')

        # Longest Played Artists
        time_artists = longest_played_artist(DATA.streaming_history)
        print('Top Artists by Time Played:')
        for i, (k, v) in enumerate(list(time_artists.items())[:20], 1):
            print(f'#{i:2} - {int(v.total_seconds() // 3600)}h {int((v.total_seconds() % 3600) // 60)}m : {k}')
        print('\n')

        # Longest Played Tracks
        time_tracks = longest_played_tracks(DATA.streaming_history)
        print('Top Tracks by Time Played:')
        for i, (k, v) in enumerate(list(time_tracks.items())[:20], 1):
            print(f'#{i:2} - {int(v.total_seconds() // 3600)}h {int((v.total_seconds() % 3600) // 60)}m : {k}')
        print('\n')

        # Most Skipped
        skipped_artists = most_skipped_artist(DATA.streaming_history)
        print('Most Skipped Artists:')
        for i, (k, v) in enumerate(list(skipped_artists.items())[:100], 1):
            print(f'#{i:2} - {v:4} : {k}')
        print('\n')

        # Top Artist Per Month
        print('Top Artist Per Month:')
        monthly_tops = top_artist_per_month(DATA.streaming_history)
        for month, (artist, count) in monthly_tops.items():
            print(f'{month}: {artist} ({count} plays)')
        print('\n')

        # One Hit Wonders
        one_hits = one_hit_wonders(DATA.streaming_history)
        print('Top One-Hit Wonders (Artists with > 5 plays but only 1 unique track):')
        for i, (artist, (track, count)) in enumerate(list(one_hits.items())[:100], 1):
            print(f'#{i:2} - {artist} : {track} ({count} plays)')
        print('\n')

        # Longest Streak
        streak_start, streak_end, streak_duration = longest_listening_streak(DATA.streaming_history)
        if streak_start:
            print(f'Longest Listening Streak:')
            print(f'Duration: {streak_duration}')
            print(f'From: {streak_start}')
            print(f'To:   {streak_end}')
        print('\n')

        # True Skip Rate
        print('True Skip Rate (Artists with > 20 plays):')
        skip_rates = true_skip_rate(DATA.streaming_history)
        for i, (k, v) in enumerate(list(skip_rates.items())[:100], 1):
            print(f'#{i:2} - {v:5.1f}% : {k}')
        print('\n')

        # Consecutive Plays
        streak_track, streak_count = most_consecutive_plays(DATA.streaming_history)
        print(f'Most Consecutive Plays: {streak_track} ({streak_count} times in a row)\n')

        # Album Loyalty
        print('Top Albums by "Loyalty" (Listening to >3 tracks in a row):')
        loyal_albums = album_loyalty(DATA.streaming_history)
        for i, (k, v) in enumerate(list(loyal_albums.items())[:100], 1):
            print(f'#{i:2} - {v:4} sessions : {k}')
        print('\n')

        # Longest Relationship
        print('Longest Artist Relationships:')
        relationships = longest_artist_relationship(DATA.streaming_history)
        for i, (k, v) in enumerate(list(relationships.items())[:100], 1):
            days = v.days
            print(f'#{i:2} - {days:4} days : {k}')
        print('\n')

        # Forgotten Favorites
        print('Forgotten Favorites (Popular > 6 months ago, 0 plays recently):')
        forgotten = forgotten_favorites(DATA.streaming_history)
        for i, (k, v) in enumerate(forgotten[:100], 1):
            print(f'#{i:2} - {v:4} past plays : {k}')
        print('\n')

        # Most Musical Day
        musical_day, musical_time = most_musical_day(DATA.streaming_history)
        print(f'Most Musical Day: {musical_day} ({int(musical_time.total_seconds() // 3600)}h {int((musical_time.total_seconds() % 3600) // 60)}m)\n')

        # Weekend vs Weekday
        weekday_top, weekend_top = weekend_vs_weekday(DATA.streaming_history)
        print('Top 5 Weekday Artists:')
        for i, (k, v) in enumerate(list(weekday_top.items())[:10], 1):
            print(f'#{i:2} - {v:4} : {k}')
        print('Top 5 Weekend Artists:')
        for i, (k, v) in enumerate(list(weekend_top.items())[:10], 1):
            print(f'#{i:2} - {v:4} : {k}')
        print('\n')

        # Immediate Skips
        print('Top "Nope" Songs (Skipped < 30s):')
        nopes = immediate_skips(DATA.streaming_history)
        for i, (k, v) in enumerate(list(nopes.items())[:50], 1):
            print(f'#{i:2} - {v:4} skips : {k}')
        print('\n')

        # Variety Score
        print('Variety Score (Unique Artists / Total Plays):')
        variety = variety_score(DATA.streaming_history)
        for year, score in variety.items():
            print(f'{year}: {score:.3f}')
        print('\n')

        # Listening Velocity
        print('Listening Velocity (Fastest to 100 plays):')
        velocity = listening_velocity(DATA.streaming_history)
        for i, (k, v) in enumerate(list(velocity.items())[:50], 1):
            print(f'#{i:2} - {v:4} days : {k}')
        print('\n')

        # The Comeback
        print('The Comeback (Artists with > 1 year gap):')
        comebacks = the_comeback(DATA.streaming_history)
        for i, (k, v) in enumerate(list(comebacks.items())[:50], 1):
            print(f'#{i:2} - {v:4} days gap : {k}')
        print('\n')

        # Clockwork Artists
        print('Clockwork Artists (>70% plays in 4h window):')
        clockwork = clockwork_artists(DATA.streaming_history)
        for i, (k, v) in enumerate(list(clockwork.items())[:30], 1):
            print(f'#{i:2} - {v} : {k}')
        print('\n')

        # Session Analysis
        avg_sess_dur, avg_sess_tracks = session_analysis(DATA.streaming_history)
        print(f'Average Session: {avg_sess_dur:.1f} minutes, {avg_sess_tracks:.1f} tracks\n')

        # Skipless Albums
        print('Skipless Albums (Lowest skip rate, min 50 plays):')
        skipless = skipless_albums(DATA.streaming_history)
        for i, (k, v) in enumerate(list(skipless.items())[:50], 1):
            print(f'#{i:2} - {v:5.1f}% skips : {k}')
        print('\n')

        # Sampler vs Completionist
        print('Completionist Score (Unique Tracks / Total Plays):')
        completionist = sampler_vs_completionist(DATA.streaming_history)
        for i, (k, v) in enumerate(list(completionist.items())[:10], 1):
            print(f'#{i:2} - {v:.2f} : {k}')
        print('\n')

        # Commute Heroes
        print('Commute Heroes (Mon-Fri 7-9am & 5-7pm):')
        commuters = commute_heroes(DATA.streaming_history)
        for i, (k, v) in enumerate(list(commuters.items())[:10], 1):
            print(f'#{i:2} - {v:4} plays : {k}')
        print('\n')

        # Marathon Tracks
        print('Marathon Tracks (> 5 mins):')
        marathons = marathon_tracks(DATA.streaming_history)
        for i, (k, v) in enumerate(list(marathons.items())[:100], 1):
            print(f'#{i:2} - {v:4} plays : {k}')
        print('\n')

        # One Week Wonders
        print('One Week Wonders (>50 plays in 1 week, <10 others):')
        wonders = one_week_wonders(DATA.streaming_history)
        for i, (k, v) in enumerate(list(wonders.items())[:100], 1):
            print(f'#{i:2} - {v} : {k}')
        print('\n')

        # Sound of Silence
        silence_start, silence_end, silence_days = sound_of_silence(DATA.streaming_history)
        print(f'Sound of Silence (Longest gap): {silence_days} days')
        print(f'From: {silence_start}')
        print(f'To:   {silence_end}\n')

        # Control Freak
        cf_data, (cf_artist, cf_count) = control_freak_data(DATA.streaming_history)
        print('Control Freak vs Passenger:')
        print(f"Active Listening (You clicked): {cf_data['active']:.1f}%")
        print(f"Passive Listening (Autoplay/Queue): {cf_data['passive']:.1f}%")
        print(f"Most Clicked Artist: {cf_artist} ({cf_count} active starts)")
        print('\n')

        # Shuffle Paradox
        shuf_data = shuffle_paradox_data(DATA.streaming_history)
        print('The Shuffle Paradox:')
        print(f"Skip Rate with Shuffle ON:  {shuf_data['shuffle_skip_rate']:.1f}%")
        print(f"Skip Rate with Shuffle OFF: {shuf_data['normal_skip_rate']:.1f}%")
        print('\n')

        # Natural Death
        nat_data, respected_artists = natural_death_data(DATA.streaming_history)
        print("The 'Natural Causes' Death Rate:")
        print(f"Songs finished naturally: {nat_data['natural']:.1f}%")
        print(f"Songs killed by user:     {nat_data['killed']:.1f}%")
        print('Top "Respected" Artists (Highest completion rate):')
        for i, (k, v) in enumerate(respected_artists, 1):
            print(f'#{i:2} - {v:.1f}% finished : {k}')
        print('\n')

        # Skipped Ratio
        skipped_stats = skipped_ratio(DATA.streaming_history)
        print('Skipped Ratio:')
        for k, v in skipped_stats.items():
            print(f'{k}: {v}')
        print('\n')

        # Night Shift
        print('The Night Shift (Top Artists 2 AM - 5 AM):')
        night_artists = night_shift_artists(DATA.streaming_history)
        for i, (k, v) in enumerate(list(night_artists.items())[:20], 1):
            print(f'#{i:2} - {v:4} plays : {k}')
        print('\n')

        # New Year's Transitions
        print("New Year's Transitions:")
        transitions = new_years_transitions(DATA.streaming_history)
        for year, (last, first) in transitions.items():
            print(f"{year} -> {year+1}:")
            print(f"  Last:  {last}")
            print(f"  First: {first}")
        print('\n')

        # Consistency King
        print('Consistency King (Tracks played on most unique days):')
        consistent_tracks = consistency_king(DATA.streaming_history)
        for i, (k, v) in enumerate(list(consistent_tracks.items())[:20], 1):
            print(f'#{i:2} - {v:4} days : {k}')
        print('\n')

        # Alphabet Challenge
        print('The Alphabet Challenge (Most played track for A-Z):')
        alphabet_data = alphabet_challenge(DATA.streaming_history)
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if char in alphabet_data:
                track, count = alphabet_data[char]
                print(f"{char}: {track} ({count} plays)")
            else:
                print(f"{char}: -")
        print('\n')

        # Obsession Score
        print('Obsession Score (Plays / Unique Days):')
        obsessions = obsession_score(DATA.streaming_history)
        for i, (k, v) in enumerate(list(obsessions.items())[:10], 1):
            print(f'#{i:2} - {v:.2f} : {k}')
        print('\n')

        # Early Bird
        print('The Early Bird (Top Artists 5 AM - 9 AM):')
        early_birds = early_bird_artists(DATA.streaming_history)
        for i, (k, v) in enumerate(list(early_birds.items())[:10], 1):
            print(f'#{i:2} - {v:4} plays : {k}')
        print('\n')

        # 9-to-5
        print('The 9-to-5 (Top Artists Mon-Fri 9 AM - 5 PM):')
        workers = nine_to_five_artists(DATA.streaming_history)
        for i, (k, v) in enumerate(list(workers.items())[:10], 1):
            print(f'#{i:2} - {v:4} plays : {k}')
        print('\n')

        # Party Animal
        print('The Party Animal (Top Tracks Fri/Sat 10 PM - 4 AM):')
        party_tracks = party_animal_tracks(DATA.streaming_history)
        for i, (k, v) in enumerate(list(party_tracks.items())[:20], 1):
            print(f'#{i:2} - {v:4} plays : {k}')
        print('\n')

        # Sunday Scaries
        print('The Sunday Scaries (Top Tracks Sun 6 PM - Midnight):')
        scary_tracks = sunday_scaries_tracks(DATA.streaming_history)
        for i, (k, v) in enumerate(list(scary_tracks.items())[:20], 1):
            print(f'#{i:2} - {v:4} plays : {k}')
        print('\n')

        # Unskippable Streak
        streak_count, streak_start, streak_end = unskippable_streak(DATA.streaming_history)
        print(f'Unskippable Streak: {streak_count} songs in a row')
        print(f'From: {streak_start}')
        print(f'To:   {streak_end}\n')

        # Artist Hopper
        hopper_score = artist_hopper(DATA.streaming_history)
        print(f'Artist Hopper Score (Avg consecutive plays per artist): {hopper_score:.2f}')
        print('(Low = Shuffle lover, High = Album listener)\n')

        # Discovery Peak
        peak_month, peak_count = discovery_peak(DATA.streaming_history)
        print(f'Discovery Peak: {peak_month} ({peak_count} new artists)\n')

        # Comfort Zone
        comfort_pct, comfort_top10 = comfort_zone(DATA.streaming_history)
        print(f'The Comfort Zone: {comfort_pct:.1f}% of time spent on Top 10 Artists')
        print('Top 10 Contributors:')
        for i, (artist, duration) in enumerate(comfort_top10, 1):
            print(f'#{i:2} - {int(duration.total_seconds() // 3600)}h : {artist}')
        print('\n')

        # Single Day Record
        rec_artist, rec_date, rec_time = single_day_record(DATA.streaming_history)
        print(f'Single Day Record: {rec_artist} on {rec_date}')
        print(f'Duration: {int(rec_time.total_seconds() // 3600)}h {int((rec_time.total_seconds() % 3600) // 60)}m\n')

        # --- NEW FUN STATS ---

        # Manual Laborer
        print('The Manual Laborer (Top Clicked Tracks):')
        manual = manual_laborer(DATA.streaming_history)
        for i, (k, v) in enumerate(list(manual.items())[:100], 1):
            print(f'#{i:2} - {v:4} clicks : {k}')
        print('\n')

        # Shuffle Roulette
        print('The Shuffle Roulette (Top Tracks with Shuffle ON):')
        shuffled = shuffle_roulette(DATA.streaming_history)
        for i, (k, v) in enumerate(list(shuffled.items())[:50], 1):
            print(f'#{i:2} - {v:4} plays : {k}')
        print('\n')

        # Session Starter
        print('The Session Starter (Most frequent session openers):')
        starters = session_starter(DATA.streaming_history)
        for i, (k, v) in enumerate(list(starters.items())[:50], 1):
            print(f'#{i:2} - {v:4} starts : {k}')
        print('\n')

        # Session Closer
        print('The Session Closer (Most frequent session enders):')
        closers = session_closer(DATA.streaming_history)
        for i, (k, v) in enumerate(list(closers.items())[:50], 1):
            print(f'#{i:2} - {v:4} ends : {k}')
        print('\n')

        # Quick Fix
        qf_count = quick_fix(DATA.streaming_history)
        print(f'The Quick Fix: {qf_count} "Single Song Sessions" (Opened app, played 1 song, closed)\n')

        # Skipper's Remorse
        print("Skipper's Remorse (Skipped >50% but played >20 times):")
        remorse = skippers_remorse(DATA.streaming_history)
        for i, (k, v) in enumerate(list(remorse.items())[:50], 1):
            print(f'#{i:2} - {v:.1f}% skipped : {k}')
        print('\n')

        # Remix Junkie
        remix_pct, remix_cnt = remix_junkie(DATA.streaming_history)
        print(f'The Remix Junkie: {remix_pct:.1f}% of tracks are Remixes/Edits ({remix_cnt} tracks)\n')

        # Live Fanatic
        live_pct, live_cnt = live_fanatic(DATA.streaming_history)
        print(f'The Live Fanatic: {live_pct:.1f}% of tracks are Live/Concert ({live_cnt} tracks)\n')

        # Short King
        print('The Short King (Most played tracks < 2 mins):')
        shorts = short_king(DATA.streaming_history)
        for i, (k, v) in enumerate(list(shorts.items())[:15], 1):
            print(f'#{i:2} - {v:4} plays : {k}')
        print('\n')

        # Epic Saga
        print('The Epic Saga (Most played tracks > 7 mins):')
        epics = epic_saga(DATA.streaming_history)
        for i, (k, v) in enumerate(list(epics.items())[:15], 1):
            print(f'#{i:2} - {v:4} plays : {k}')
        print('\n')

        # Collaborator
        print('The Collaborator (Most played tracks featuring others):')
        collabs = collaborator(DATA.streaming_history)
        for i, (k, v) in enumerate(list(collabs.items())[:5], 1):
            print(f'#{i:2} - {v:4} plays : {k}')
        print('\n')

        # Alphabet Artists
        print('The Alphabet Artists (Top Artist for A-Z):')
        alpha_artists = alphabet_artists(DATA.streaming_history)
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if char in alpha_artists:
                artist, count = alpha_artists[char]
                print(f"{char}: {artist} ({count} plays)")
            else:
                print(f"{char}: -")
        print('\n')

        # Spelling Bee
        long_art, len_art, long_trk, len_trk = spelling_bee(DATA.streaming_history)
        print(f'The Spelling Bee:')
        print(f'Longest Artist Name: {long_art} ({len_art} chars)')
        print(f'Longest Track Title: {long_trk} ({len_trk} chars)\n')

        # Same Name Game
        print('The Same Name Game (Titles played from most different artists):')
        same_names = same_name_game(DATA.streaming_history)
        for i, (k, v) in enumerate(list(same_names.items())[:5], 1):
            print(f'#{i:2} - {v:4} artists : {k}')
        print('\n')

        # Midnight Club
        print('The Midnight Club (Top Artists 00:00 - 01:00):')
        midnighters = midnight_club(DATA.streaming_history)
        for i, (k, v) in enumerate(list(midnighters.items())[:15], 1):
            print(f'#{i:2} - {v:4} plays : {k}')
        print('\n')

        # Lunch Break
        print('The Lunch Break (Top Artists 12:00 - 14:00):')
        lunchers = lunch_break(DATA.streaming_history)
        for i, (k, v) in enumerate(list(lunchers.items())[:15], 1):
            print(f'#{i:2} - {v:4} plays : {k}')
        print('\n')

        # Monday Blues
        print('The Monday Blues (Top Tracks on Mondays):')
        mondays = monday_blues(DATA.streaming_history)
        for i, (k, v) in enumerate(list(mondays.items())[:15], 1):
            print(f'#{i:2} - {v:4} plays : {k}')
        print('\n')

        # Hump Day Hero
        print('The Hump Day Hero (Top Tracks on Wednesdays):')
        wednesdays = hump_day_hero(DATA.streaming_history)
        for i, (k, v) in enumerate(list(wednesdays.items())[:15], 1):
            print(f'#{i:2} - {v:4} plays : {k}')
        print('\n')

        # Quarterly Review
        print('The Quarterly Review (Top Track per Quarter):')
        quarters = quarterly_review(DATA.streaming_history)
        for q, (track, count) in quarters.items():
            print(f'Q{q}: {track} ({count} plays)')
        print('\n')

        # Album Purist
        purist_streak, purist_album, purist_artist = album_purist(DATA.streaming_history)
        print(f'The Album Purist:')
        print(f'Longest streak of unique songs from one album: {purist_streak}')
        print(f'Album: {purist_album} by {purist_artist}\n')

        # Instant Skips (all removed tracks from spotify because it was started but immediately skipped)
        print('Instant Skips Probably removed tracks (Skipped < 1s):')
        inst_skips = instant_skips(DATA.streaming_history)
        total_inst_skips = sum(inst_skips.values())
        print(f'Total Instant Skips: {total_inst_skips}')
        for i, (k, v) in enumerate(list(inst_skips.items())[:20], 1):
            print(f'#{i:2} - {v:4} skips : {k}')
        print('\n')

        print('--- End of Report ---')

        # Stop capturing output
        sys.stdout = original_stdout
        report_text = captured_output.getvalue()

        # Export CSV
        print('Exporting song stats to song_stats.csv...')
        song_stats = get_full_song_stats(DATA.streaming_history)
        with open('song_stats.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Artist', 'Track Name', 'Times Played', 'First Played', 'Last Played', 'Skipped', 'Instant Skips', 'User Started']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(song_stats)
        print('Done! CSV exported.\n')

        # Graphs
        print('\n')
        graph_mode = input('Do you want to (s)how graphs, (e)xport to PDF, or (n)one? (s/e/n): ').lower()

        if graph_mode in ['s', 'e']:
            figures = []
            print('Generating graphs...')

            figures.append(plot_top_items(track_counts, 'Top 10 Played Tracks'))
            figures.append(plot_top_items(artist_counts, 'Top 10 Played Artists'))
            figures.append(plot_top_items(album_counts, 'Top 10 Played Albums'))

            figures.append(plot_location_counts(locations, 'Plays by Location'))
            figures.append(plot_longest_played_artist(time_artists, 'Top 10 Artists by Listening Time'))
            figures.append(plot_longest_played_tracks(time_tracks, 'Top 10 Tracks by Listening Time'))
            figures.append(plot_skipped_items(skipped_artists, 'Top 10 Skipped Artists'))
            figures.append(plot_skipped_items(most_skipped_track(DATA.streaming_history), 'Top 10 Skipped Tracks'))
            
            figures.append(plot_top_items(night_artists, 'The Night Shift (Top Artists 2AM-5AM)'))

            # Fun Stats Graphs
            figures.append(plot_listening_by_day_of_week(listening_by_day_of_week(DATA.streaming_history), 'Listening by Day of Week'))
            figures.append(plot_discovery_rate(discovery_rate(DATA.streaming_history), 'Artist Discovery Rate (New Artists per Month)'))
            figures.append(plot_seasonal_listening(seasonal_listening(DATA.streaming_history), 'Seasonal Listening Habits'))
            figures.append(plot_day_night_split(day_night_split(DATA.streaming_history), 'Day vs Night Listening'))
            figures.append(plot_hourly_heatmap(hourly_heatmap_data(DATA.streaming_history), 'Listening Heatmap (Day vs Hour)'))
            figures.append(plot_variety_score(variety, 'Variety Score Over Years'))
            figures.append(plot_comfort_zone(comfort_pct, 'The Comfort Zone (% Time on Top 10 Artists)'))

            # Heatmaps
            cal_matrix, cal_years, cal_months = calendar_heatmap_data(DATA.streaming_history)
            figures.append(plot_calendar_heatmap(cal_matrix, cal_years, cal_months, 'Listening Calendar (Year vs Month)'))

            figures.append(plot_picky_grid(picky_grid_data(DATA.streaming_history), 'The Picky Grid (Skip Rate % by Day & Hour)'))

            dev_matrix, dev_platforms = device_habits_data(DATA.streaming_history)
            figures.append(plot_device_habits(dev_matrix, dev_platforms, 'Device Habits (Platform vs Hour)'))

            eras_matrix, eras_artists, eras_time = artist_eras_data(DATA.streaming_history, top_n=300)
            figures.append(plot_artist_eras(eras_matrix, eras_artists, eras_time, 'Artist Eras (Top 300 Artists vs Time)'))

            # Active Listening Deep Dive
            figures.append(plot_active_heatmap(active_listening_heatmap_data(DATA.streaming_history), 'Active Listening Heatmap (When do you click play?)'))
            figures.append(plot_active_trend(active_listening_trend_data(DATA.streaming_history), 'Active Listening Trend (% of starts that were clicks)'))

            # Artist Trends
            top_50_artists = list(artist_counts.keys())[:50]
            artist_trends = artist_history_over_time(DATA.streaming_history, top_50_artists)
            figures.append(plot_artist_trends(artist_trends, 'Top 50 Artists Trends Over Years'))

            # Platform Usage
            platforms = platform_usage(DATA.streaming_history)
            figures.append(plot_platform_usage(platforms, 'Platform Usage'))

            # Listening by Hour
            hourly_stats = listening_by_hour(DATA.streaming_history)
            figures.append(plot_listening_by_hour(hourly_stats, 'Listening Activity by Hour of Day'))

            # Artist Personality Radar
            # print("Calculating Artist Personalities...")
            # traits = get_artist_traits(DATA.streaming_history)
            # Pick top 5 artists
            # top_5_artists = list(artist_counts.keys())[:5]
            # for artist in top_5_artists:
            #     if artist in traits:
            #         figures.append(plot_artist_radar({artist: traits[artist]}, f'Artist Personality: {artist}'))

            # Filter out None figures
            figures = [f for f in figures if f is not None]

            if graph_mode == 'e':
                filename = f'spotify_stats_report_{int(time.time())}.pdf'
                
                # Add text pages
                print('Generating text pages...')
                text_figures = create_text_pages(report_text)
                all_figures = text_figures + figures
                
                print(f'Saving {len(all_figures)} pages to {filename}...')
                with PdfPages(filename) as pdf:
                    for fig in all_figures:
                        pdf.savefig(fig)
                        plt.close(fig)
                print(f'Done! Report saved to {filename}')
            elif graph_mode == 's':
                print('Showing graphs...')
                plt.show()

    except Exception:
        traceback.print_exc()

    input('\nPress Enter to Exit.')
