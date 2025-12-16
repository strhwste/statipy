from datetime import timedelta, datetime
from collections import defaultdict
import time

from time import gmtime, struct_time, mktime

from filemgr.types import History


def play_time(streaming_history: list[History],
              start_date: struct_time = gmtime(0),
              end_date: struct_time = gmtime()) -> timedelta:
    """
    calculates total listening time between (optionally) specified time ranges
    no start/end time specified will use the earliest/latest dates in history
    """
    total_time = timedelta()
    for i in streaming_history:
        if start_date <= i['endTime'] <= end_date:
            total_time += i['msPlayed']

    return total_time


def history_range(streaming_history: list[History]) -> tuple[struct_time, struct_time]:
    """
    find the time range the streaming history covers;
    returns tuple of the earliest and latest dates
    """
    return streaming_history[0]['endTime'], streaming_history[-1]['endTime']


def play_counts(streaming_history: list[History]) -> dict[History, int]:
    """
    Generates dictionary with unique artist-track-name keys and number of times played as values

    :return: descending sorted dictionary by play count
    """
    result = {}
    for i in streaming_history:
        key = f"{i['artistName']} - {i['trackName']}"
        if key not in result:
            result[key] = 0
        result[key] += 1

    sort = {k: result[k] for k in sorted(result, key=result.get, reverse=True)}

    return sort


def play_counts_by_artist(streaming_history: list[History]) -> dict[str, int]:
    """
    Generates dictionary with unique artist names and number of times played as values

    :return: descending sorted dictionary by play count
    """
    result = {}
    for i in streaming_history:
        key = i['artistName']
        if key not in result:
            result[key] = 0
        result[key] += 1

    sort = {k: result[k] for k in sorted(result, key=result.get, reverse=True)}

    return sort


def play_counts_by_album(streaming_history: list[History]) -> dict[str, int]:
    """
    Generates dictionary with unique album names and number of times played as values

    :return: descending sorted dictionary by play count
    """
    result = {}
    for i in streaming_history:
        key = f"{i['artistName']} - {i['albumName']}"
        if key not in result:
            result[key] = 0
        result[key] += 1

    sort = {k: result[k] for k in sorted(result, key=result.get, reverse=True)}

    return sort


def artist_history_over_time(streaming_history: list[History], top_artists: list[str]) -> dict[str, dict[int, int]]:
    """
    Generates a dictionary of artist play counts per year for the specified top artists.
    Structure: { 'Artist Name': { 2012: 10, 2013: 50, ... }, ... }
    """
    result = {artist: {} for artist in top_artists}

    for item in streaming_history:
        artist = item['artistName']
        if artist in result:
            year = item['endTime'].tm_year
            if year not in result[artist]:
                result[artist][year] = 0
            result[artist][year] += 1

    return result


def platform_usage(streaming_history: list[History]) -> dict[str, int]:
    """
    Calculates the number of plays per platform.
    """
    result = {}
    for item in streaming_history:
        platform = item['platform']
        if platform not in result:
            result[platform] = 0
        result[platform] += 1
    return {k: result[k] for k in sorted(result, key=result.get, reverse=True)}


def listening_by_hour(streaming_history: list[History]) -> dict[int, int]:
    """
    Calculates the number of plays per hour of the day (0-23).
    """
    result = {h: 0 for h in range(24)}
    for item in streaming_history:
        hour = item['endTime'].tm_hour
        result[hour] += 1
    return result


def skipped_ratio(streaming_history: list[History]) -> dict[str, int]:
    """
    Calculates the number of skipped vs not skipped tracks.
    """
    skipped = 0
    not_skipped = 0
    for item in streaming_history:
        if item['skipped']:
            skipped += 1
        else:
            not_skipped += 1
    return {'Skipped': skipped, 'Not Skipped': not_skipped}

def location_counts(streaming_history: list[History]) -> dict[str, int]:
    """
    Calculates the number of plays per country.
    """
    result = {}
    for item in streaming_history:
        country = item['connCountry']
        if country not in result:
            result[country] = 0
        result[country] += 1
    return {k: result[k] for k in sorted(result, key=result.get, reverse=True)}


def most_skipped_artist(streaming_history: list[History]) -> dict[str, int]:
    """
    Calculates the number of skips per artist.
    """
    result = {}
    for item in streaming_history:
        if item['skipped']:
            artist = item['artistName']
            if artist not in result:
                result[artist] = 0
            result[artist] += 1
    return {k: result[k] for k in sorted(result, key=result.get, reverse=True)}


def most_skipped_track(streaming_history: list[History]) -> dict[str, int]:
    """
    Calculates the number of skips per track.
    """
    result = {}
    for item in streaming_history:
        if item['skipped']:
            track = f"{item['artistName']} - {item['trackName']}"
            if track not in result:
                result[track] = 0
            result[track] += 1
    return {k: result[k] for k in sorted(result, key=result.get, reverse=True)}


def longest_played_artist(streaming_history: list[History]) -> dict[str, timedelta]:
    """
    Calculates the total listening time per artist.
    """
    result = defaultdict(timedelta)
    for item in streaming_history:
        result[item['artistName']] += item['msPlayed']

    return {k: result[k] for k in sorted(result, key=result.get, reverse=True)}


def top_artist_per_month(streaming_history: list[History]) -> dict[str, tuple[str, int]]:
    """
    Finds the most played artist for each month.
    Returns: {'YYYY-MM': ('Artist Name', play_count), ...}
    """
    monthly_counts = defaultdict(lambda: defaultdict(int))

    for item in streaming_history:
        month_key = f"{item['endTime'].tm_year}-{item['endTime'].tm_mon:02d}"
        monthly_counts[month_key][item['artistName']] += 1

    result = {}
    for month, artists in monthly_counts.items():
        top_artist = max(artists.items(), key=lambda x: x[1])
        result[month] = top_artist

    return dict(sorted(result.items()))

def listening_by_day_of_week(streaming_history: list[History]) -> dict[str, int]:
    """
    Calculates plays by day of the week.
    """
    days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    result = {day: 0 for day in days.values()}

    for item in streaming_history:
        day_idx = item['endTime'].tm_wday
        result[days[day_idx]] += 1

    return result


def discovery_rate(streaming_history: list[History]) -> dict[str, int]:
    """
    Calculates new artists discovered per month.
    """
    seen_artists = set()
    result = defaultdict(int)

    # Ensure history is sorted by time
    sorted_history = sorted(streaming_history, key=lambda x: x['endTime'])

    for item in sorted_history:
        artist = item['artistName']
        if artist not in seen_artists:
            seen_artists.add(artist)
            month_key = f"{item['endTime'].tm_year}-{item['endTime'].tm_mon:02d}"
            result[month_key] += 1

    return dict(sorted(result.items()))


def seasonal_listening(streaming_history: list[History]) -> dict[str, int]:
    """
    Calculates plays by season.
    """
    seasons = {'Winter': 0, 'Spring': 0, 'Summer': 0, 'Autumn': 0}

    for item in streaming_history:
        month = item['endTime'].tm_mon
        if month in [12, 1, 2]:
            seasons['Winter'] += 1
        elif month in [3, 4, 5]:
            seasons['Spring'] += 1
        elif month in [6, 7, 8]:
            seasons['Summer'] += 1
        elif month in [9, 10, 11]:
            seasons['Autumn'] += 1

    return seasons


def one_hit_wonders(streaming_history: list[History], min_plays: int = 5) -> dict[str, tuple[str, int]]:
    """
    Finds artists with > min_plays but only 1 unique track.
    Returns {artist: (track_name, play_count)}
    """
    artist_tracks = defaultdict(set)
    artist_plays = defaultdict(int)

    for item in streaming_history:
        artist = item['artistName']
        track = item['trackName']
        artist_tracks[artist].add(track)
        artist_plays[artist] += 1

    result = {}
    for artist, tracks in artist_tracks.items():
        if len(tracks) == 1 and artist_plays[artist] >= min_plays:
            result[artist] = (list(tracks)[0], artist_plays[artist])

    return dict(sorted(result.items(), key=lambda x: x[1][1], reverse=True))


def day_night_split(streaming_history: list[History]) -> dict[str, int]:
    """
    Calculates plays during Day (6-18) vs Night (18-6).
    """
    result = {'Day': 0, 'Night': 0}
    for item in streaming_history:
        hour = item['endTime'].tm_hour
        if 6 <= hour < 18:
            result['Day'] += 1
        else:
            result['Night'] += 1
    return result


def longest_listening_streak(streaming_history: list[History], gap_tolerance_minutes: int = 10) -> tuple[datetime, datetime, timedelta]:
    """
    Calculates the longest continuous listening streak.
    """
    if not streaming_history:
        return None

    sorted_history = sorted(streaming_history, key=lambda x: x['endTime'])

    max_streak_duration = timedelta(0)
    max_streak_start = None
    max_streak_end = None

    current_streak_start = None
    current_streak_end = None

    for item in sorted_history:
        # Calculate start time of the track
        end_dt = datetime.fromtimestamp(mktime(item['endTime']))
        duration = item['msPlayed'] # timedelta
        start_dt = end_dt - duration

        if current_streak_end is None:
            current_streak_start = start_dt
            current_streak_end = end_dt
            continue

        # Check gap
        gap = start_dt - current_streak_end

        if gap <= timedelta(minutes=gap_tolerance_minutes):
            # Extend streak
            current_streak_end = end_dt
        else:
            # End of streak, check if it's the longest
            streak_duration = current_streak_end - current_streak_start
            if streak_duration > max_streak_duration:
                max_streak_duration = streak_duration
                max_streak_start = current_streak_start
                max_streak_end = current_streak_end

            # Start new streak
            current_streak_start = start_dt
            current_streak_end = end_dt

    # Check last streak
    if current_streak_end and current_streak_start:
        streak_duration = current_streak_end - current_streak_start
        if streak_duration > max_streak_duration:
            max_streak_duration = streak_duration
            max_streak_start = current_streak_start
            max_streak_end = current_streak_end

    return max_streak_start, max_streak_end, max_streak_duration

def true_skip_rate(streaming_history: list[History], min_plays: int = 20) -> dict[str, float]:
    """
    Calculates skip percentage per artist (skips / total_starts).
    Only considers artists with > min_plays to avoid skewed data.
    """
    stats = defaultdict(lambda: {'plays': 0, 'skips': 0})
    for item in streaming_history:
        artist = item['artistName']
        stats[artist]['plays'] += 1
        if item['skipped']:
            stats[artist]['skips'] += 1

    results = {}
    for artist, data in stats.items():
        if data['plays'] > min_plays:
            results[artist] = (data['skips'] / data['plays']) * 100

    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))


def most_consecutive_plays(streaming_history: list[History]) -> tuple[str, int]:
    """
    Finds the track played the most times consecutively (back-to-back).
    """
    if not streaming_history:
        return ("None", 0)

    max_streak = 0
    max_track = ""

    current_streak = 1
    # Create a unique identifier for the track
    current_track = f"{streaming_history[0]['artistName']} - {streaming_history[0]['trackName']}"

    for i in range(1, len(streaming_history)):
        track = f"{streaming_history[i]['artistName']} - {streaming_history[i]['trackName']}"
        if track == current_track:
            current_streak += 1
        else:
            if current_streak > max_streak:
                max_streak = current_streak
                max_track = current_track
            current_track = track
            current_streak = 1

    return (max_track, max_streak)


def album_loyalty(streaming_history: list[History]) -> dict[str, int]:
    """
    Counts how many times a user listened to at least 3 songs from the same album in a row.
    """
    loyalty_counts = defaultdict(int)
    if not streaming_history:
        return loyalty_counts

    current_album = streaming_history[0]['albumName']
    current_streak = 1

    for i in range(1, len(streaming_history)):
        album = streaming_history[i]['albumName']
        # Ignore singles or unknown albums if necessary, but keeping it simple for now
        if album == current_album and album:
            current_streak += 1
        else:
            if current_streak >= 3:
                loyalty_counts[current_album] += 1
            current_album = album
            current_streak = 1

    return dict(sorted(loyalty_counts.items(), key=lambda x: x[1], reverse=True))


def longest_artist_relationship(streaming_history: list[History]) -> dict[str, timedelta]:
    """
    Calculates time between first and last listen for each artist.
    """
    first_seen = {}
    last_seen = {}

    for item in streaming_history:
        artist = item['artistName']
        # Convert struct_time to datetime
        ts = item['endTime']
        dt = datetime.fromtimestamp(time.mktime(ts))

        if artist not in first_seen or dt < first_seen[artist]:
            first_seen[artist] = dt
        if artist not in last_seen or dt > last_seen[artist]:
            last_seen[artist] = dt

    durations = {}
    for artist in first_seen:
        diff = last_seen[artist] - first_seen[artist]
        # Filter out artists listened to for less than a day
        if diff.total_seconds() > 86400:
            durations[artist] = diff

    return dict(sorted(durations.items(), key=lambda x: x[1], reverse=True))


def forgotten_favorites(streaming_history: list[History], months_forgotten: int = 6) -> list[tuple[str, int]]:
    """
    Identifies artists that were popular in the past but have 0 plays in the last X months.
    """
    if not streaming_history:
        return []

    # Sort history by time
    sorted_history = sorted(streaming_history, key=lambda x: x['endTime'])
    last_date = datetime.fromtimestamp(mktime(sorted_history[-1]['endTime']))
    cutoff_date = last_date - timedelta(days=30 * months_forgotten)

    recent_artists = set()
    past_counts = defaultdict(int)

    for item in sorted_history:
        dt = datetime.fromtimestamp(mktime(item['endTime']))
        artist = item['artistName']
        if dt > cutoff_date:
            recent_artists.add(artist)
        else:
            past_counts[artist] += 1

    forgotten = []
    for artist, count in past_counts.items():
        if artist not in recent_artists and count > 20: # Minimum plays to be considered a "favorite"
            forgotten.append((artist, count))

    return sorted(forgotten, key=lambda x: x[1], reverse=True)


def hourly_heatmap_data(streaming_history: list[History]) -> list[list[int]]:
    """
    Prepares data for a 2D heatmap: 7 days x 24 hours.
    Returns a 7x24 matrix where cell [d][h] is the play count.
    """
    # 7 rows (Mon-Sun), 24 columns (0-23 hours)
    matrix = [[0 for _ in range(24)] for _ in range(7)]

    for item in streaming_history:
        day = item['endTime'].tm_wday # 0=Mon, 6=Sun
        hour = item['endTime'].tm_hour
        matrix[day][hour] += 1

    return matrix

def most_musical_day(streaming_history: list[History]) -> tuple[str, timedelta]:
    """
    Finds the single date with the most listening time.
    """
    daily_time = defaultdict(timedelta)
    
    for item in streaming_history:
        date_key = time.strftime("%Y-%m-%d", item['endTime'])
        daily_time[date_key] += item['msPlayed']
        
    if not daily_time:
        return ("None", timedelta(0))
        
    max_day = max(daily_time.items(), key=lambda x: x[1])
    return max_day


def weekend_vs_weekday(streaming_history: list[History]) -> tuple[dict[str, int], dict[str, int]]:
    """
    Returns top artists for Weekdays (Mon-Fri) and Weekends (Sat-Sun).
    """
    weekday_counts = defaultdict(int)
    weekend_counts = defaultdict(int)
    
    for item in streaming_history:
        day = item['endTime'].tm_wday
        artist = item['artistName']
        
        if day < 5: # 0-4 is Mon-Fri
            weekday_counts[artist] += 1
        else: # 5-6 is Sat-Sun
            weekend_counts[artist] += 1
            
    top_weekday = dict(sorted(weekday_counts.items(), key=lambda x: x[1], reverse=True))
    top_weekend = dict(sorted(weekend_counts.items(), key=lambda x: x[1], reverse=True))
    
    return top_weekday, top_weekend


def immediate_skips(streaming_history: list[History]) -> dict[str, int]:
    """
    Counts tracks skipped within 30 seconds (30000 ms).
    """
    skips = defaultdict(int)
    
    for item in streaming_history:
        if item['skipped'] and item['msPlayed'] < timedelta(seconds=30):
            track = f"{item['artistName']} - {item['trackName']}"
            skips[track] += 1
            
    return dict(sorted(skips.items(), key=lambda x: x[1], reverse=True))


def variety_score(streaming_history: list[History]) -> dict[int, float]:
    """
    Calculates Diversity Index (Unique Artists / Total Plays) per year.
    """
    yearly_stats = defaultdict(lambda: {'plays': 0, 'artists': set()})
    
    for item in streaming_history:
        year = item['endTime'].tm_year
        yearly_stats[year]['plays'] += 1
        yearly_stats[year]['artists'].add(item['artistName'])
        
    scores = {}
    for year, data in yearly_stats.items():
        if data['plays'] > 0:
            scores[year] = len(data['artists']) / data['plays']
            
    return dict(sorted(scores.items()))

def listening_velocity(streaming_history: list[History], target_plays: int = 100) -> dict[str, int]:
    """
    Calculates days taken to reach X plays for an artist.
    """
    artist_plays = defaultdict(list)
    
    # Collect all timestamps for each artist
    for item in streaming_history:
        artist_plays[item['artistName']].append(item['endTime'])
        
    velocity = {}
    for artist, timestamps in artist_plays.items():
        if len(timestamps) >= target_plays:
            # Sort timestamps just in case
            sorted_ts = sorted(timestamps)
            first_play = datetime.fromtimestamp(mktime(sorted_ts[0]))
            target_play = datetime.fromtimestamp(mktime(sorted_ts[target_plays-1]))
            
            days_taken = (target_play - first_play).days
            velocity[artist] = days_taken
            
    # Sort by fastest (lowest days)
    return dict(sorted(velocity.items(), key=lambda x: x[1]))


def the_comeback(streaming_history: list[History], gap_days: int = 365) -> dict[str, int]:
    """
    Finds artists with a gap of > X days between plays.
    Returns {artist: max_gap_days}
    """
    artist_timestamps = defaultdict(list)
    for item in streaming_history:
        artist_timestamps[item['artistName']].append(datetime.fromtimestamp(mktime(item['endTime'])))
        
    comebacks = {}
    for artist, timestamps in artist_timestamps.items():
        if len(timestamps) < 2:
            continue
            
        sorted_ts = sorted(timestamps)
        max_gap = 0
        
        for i in range(1, len(sorted_ts)):
            gap = (sorted_ts[i] - sorted_ts[i-1]).days
            if gap > max_gap:
                max_gap = gap
                
        if max_gap >= gap_days:
            comebacks[artist] = max_gap
            
    return dict(sorted(comebacks.items(), key=lambda x: x[1], reverse=True))


def clockwork_artists(streaming_history: list[History]) -> dict[str, str]:
    """
    Identifies artists played mostly (>70%) in specific 4-hour windows.
    """
    artist_hours = defaultdict(lambda: defaultdict(int))
    artist_total = defaultdict(int)
    
    for item in streaming_history:
        artist = item['artistName']
        hour = item['endTime'].tm_hour
        
        # Define windows: 0-4, 4-8, 8-12, 12-16, 16-20, 20-24
        window_start = (hour // 4) * 4
        window_label = f"{window_start:02d}:00-{window_start+4:02d}:00"
        
        artist_hours[artist][window_label] += 1
        artist_total[artist] += 1
        
    clockwork = {}
    for artist, total in artist_total.items():
        if total < 50: # Minimum plays
            continue
            
        for window, count in artist_hours[artist].items():
            if count / total >= 0.7:
                clockwork[artist] = f"{window} ({int(count/total*100)}%)"
                
    return clockwork


def session_analysis(streaming_history: list[History], session_break_min: int = 20) -> tuple[float, float]:
    """
    Calculates average session length (minutes) and tracks per session.
    """
    if not streaming_history:
        return (0.0, 0.0)
        
    sorted_history = sorted(streaming_history, key=lambda x: x['endTime'])
    
    sessions = []
    current_session_start = datetime.fromtimestamp(mktime(sorted_history[0]['endTime']))
    current_session_end = current_session_start
    current_session_tracks = 0
    
    for i in range(len(sorted_history)):
        ts = datetime.fromtimestamp(mktime(sorted_history[i]['endTime']))
        
        if i > 0:
            prev_ts = datetime.fromtimestamp(mktime(sorted_history[i-1]['endTime']))
            gap = (ts - prev_ts).total_seconds() / 60
            
            if gap > session_break_min:
                # End previous session
                duration = (current_session_end - current_session_start).total_seconds() / 60
                sessions.append({'duration': duration, 'tracks': current_session_tracks})
                
                # Start new session
                current_session_start = ts
                current_session_tracks = 0
        
        current_session_end = ts
        current_session_tracks += 1
        
    # Add last session
    duration = (current_session_end - current_session_start).total_seconds() / 60
    sessions.append({'duration': duration, 'tracks': current_session_tracks})
    
    avg_duration = sum(s['duration'] for s in sessions) / len(sessions)
    avg_tracks = sum(s['tracks'] for s in sessions) / len(sessions)
    
    return avg_duration, avg_tracks


def skipless_albums(streaming_history: list[History], min_plays: int = 50) -> dict[str, float]:
    """
    Finds albums with lowest skip rate (min 50 plays).
    """
    album_stats = defaultdict(lambda: {'plays': 0, 'skips': 0})
    
    for item in streaming_history:
        album = item['albumName']
        if not album: continue
        
        album_stats[album]['plays'] += 1
        if item['skipped']:
            album_stats[album]['skips'] += 1
            
    results = {}
    for album, data in album_stats.items():
        if data['plays'] >= min_plays:
            skip_rate = (data['skips'] / data['plays']) * 100
            results[album] = skip_rate
            
    # Sort by lowest skip rate
    return dict(sorted(results.items(), key=lambda x: x[1]))


def sampler_vs_completionist(streaming_history: list[History], min_plays: int = 50) -> dict[str, float]:
    """
    Calculates Unique Tracks / Total Plays ratio for top artists.
    """
    artist_stats = defaultdict(lambda: {'plays': 0, 'tracks': set()})
    
    for item in streaming_history:
        artist = item['artistName']
        track = item['trackName']
        artist_stats[artist]['plays'] += 1
        artist_stats[artist]['tracks'].add(track)
        
    ratios = {}
    for artist, data in artist_stats.items():
        if data['plays'] >= min_plays:
            ratios[artist] = len(data['tracks']) / data['plays']
            
    return dict(sorted(ratios.items(), key=lambda x: x[1], reverse=True))


def commute_heroes(streaming_history: list[History]) -> dict[str, int]:
    """
    Top artists during commute hours (Mon-Fri, 7-9 & 17-19).
    """
    commute_counts = defaultdict(int)
    
    for item in streaming_history:
        day = item['endTime'].tm_wday
        hour = item['endTime'].tm_hour
        
        if day < 5: # Mon-Fri
            if (7 <= hour < 9) or (17 <= hour < 19):
                commute_counts[item['artistName']] += 1
                
    return dict(sorted(commute_counts.items(), key=lambda x: x[1], reverse=True))


def marathon_tracks(streaming_history: list[History]) -> dict[str, int]:
    """
    Most played tracks > 5 minutes long.
    """
    long_tracks = defaultdict(int)
    
    for item in streaming_history:
        if item['msPlayed'] > timedelta(minutes=5):
            track = f"{item['artistName']} - {item['trackName']}"
            long_tracks[track] += 1
            
    return dict(sorted(long_tracks.items(), key=lambda x: x[1], reverse=True))


def one_week_wonders(streaming_history: list[History]) -> dict[str, str]:
    """
    Artists with >50 plays in one week but <10 in all others.
    """
    artist_weekly = defaultdict(lambda: defaultdict(int))
    
    for item in streaming_history:
        # ISO Year and Week
        year, week, _ = datetime.fromtimestamp(mktime(item['endTime'])).isocalendar()
        week_key = f"{year}-W{week:02d}"
        artist_weekly[item['artistName']][week_key] += 1
        
    wonders = {}
    for artist, weeks in artist_weekly.items():
        max_week = max(weeks.items(), key=lambda x: x[1])
        max_plays = max_week[1]
        
        if max_plays > 50:
            other_plays = sum(count for w, count in weeks.items() if w != max_week[0])
            if other_plays < 10:
                wonders[artist] = f"{max_week[0]} ({max_plays} plays)"
                
    return wonders


def sound_of_silence(streaming_history: list[History]) -> tuple[str, str, int]:
    """
    Longest gap between any two plays.
    """
    if not streaming_history:
        return ("None", "None", 0)
        
    sorted_history = sorted(streaming_history, key=lambda x: x['endTime'])
    
    max_gap = timedelta(0)
    gap_start = None
    gap_end = None
    
    for i in range(1, len(sorted_history)):
        curr = datetime.fromtimestamp(mktime(sorted_history[i]['endTime']))
        prev = datetime.fromtimestamp(mktime(sorted_history[i-1]['endTime']))
        
        # Subtract duration of previous track to get true silence start
        prev_end = prev # endTime is already the end of the track
        
        gap = curr - prev_end
        if gap > max_gap:
            max_gap = gap
            gap_start = prev_end
            gap_end = curr
            
    return (str(gap_start), str(gap_end), max_gap.days)

def calendar_heatmap_data(streaming_history: list[History]) -> tuple[list[list[int]], list[int], list[str]]:
    """
    Prepares data for Year vs Month heatmap.
    Returns (matrix, years, months).
    """
    years = sorted(list(set(item['endTime'].tm_year for item in streaming_history)))
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Matrix: Rows = Years, Cols = Months
    matrix = [[0 for _ in range(12)] for _ in range(len(years))]
    
    year_to_idx = {y: i for i, y in enumerate(years)}
    
    for item in streaming_history:
        y = item['endTime'].tm_year
        m = item['endTime'].tm_mon - 1 # 0-11
        matrix[year_to_idx[y]][m] += 1
        
    return matrix, years, months


def picky_grid_data(streaming_history: list[History]) -> list[list[float]]:
    """
    Prepares data for Day vs Hour Skip Rate heatmap.
    Returns 7x24 matrix of skip percentages.
    """
    # 7 rows (Mon-Sun), 24 columns (0-23 hours)
    plays = [[0 for _ in range(24)] for _ in range(7)]
    skips = [[0 for _ in range(24)] for _ in range(7)]
    
    for item in streaming_history:
        day = item['endTime'].tm_wday
        hour = item['endTime'].tm_hour
        plays[day][hour] += 1
        if item['skipped']:
            skips[day][hour] += 1
            
    # Calculate percentages
    matrix = [[0.0 for _ in range(24)] for _ in range(7)]
    for d in range(7):
        for h in range(24):
            if plays[d][h] > 0:
                matrix[d][h] = (skips[d][h] / plays[d][h]) * 100
                
    return matrix


def device_habits_data(streaming_history: list[History]) -> tuple[list[list[int]], list[str]]:
    """
    Prepares data for Platform vs Hour heatmap.
    Returns (matrix, platforms).
    """
    platforms = sorted(list(set(item['platform'] for item in streaming_history)))
    # Limit to top 10 platforms to keep heatmap readable if there are many
    platform_counts = defaultdict(int)
    for item in streaming_history:
        platform_counts[item['platform']] += 1
    
    top_platforms = [p for p, c in sorted(platform_counts.items(), key=lambda x: x[1], reverse=True)[:10]]
    platform_to_idx = {p: i for i, p in enumerate(top_platforms)}
    
    # Matrix: Rows = Platforms, Cols = Hours
    matrix = [[0 for _ in range(24)] for _ in range(len(top_platforms))]
    
    for item in streaming_history:
        p = item['platform']
        if p in platform_to_idx:
            h = item['endTime'].tm_hour
            matrix[platform_to_idx[p]][h] += 1
            
    return matrix, top_platforms


def artist_eras_data(streaming_history: list[History], top_n: int = 20, normalize: bool = True) -> tuple[list[list[float]], list[str], list[str]]:
    """
    Prepares data for Top Artists vs Month (Eras) heatmap.
    Returns (matrix, artists, time_labels).
    If normalize is True, each artist's row is scaled 0-1 based on their peak month.
    """
    # Get top artists
    artist_counts = defaultdict(int)
    for item in streaming_history:
        artist_counts[item['artistName']] += 1
    top_artists = [a for a, c in sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]]
    artist_to_idx = {a: i for i, a in enumerate(top_artists)}
    
    # Get time range (Year-Month)
    sorted_history = sorted(streaming_history, key=lambda x: x['endTime'])
    start_date = datetime.fromtimestamp(mktime(sorted_history[0]['endTime']))
    end_date = datetime.fromtimestamp(mktime(sorted_history[-1]['endTime']))
    
    # Generate month labels
    time_labels = []
    curr = start_date.replace(day=1)
    while curr <= end_date:
        time_labels.append(curr.strftime("%Y-%m"))
        if curr.month == 12:
            curr = curr.replace(year=curr.year+1, month=1)
        else:
            curr = curr.replace(month=curr.month+1)
            
    time_to_idx = {t: i for i, t in enumerate(time_labels)}
    
    # Matrix: Rows = Artists, Cols = Months
    # Using float for potential normalization
    matrix = [[0.0 for _ in range(len(time_labels))] for _ in range(len(top_artists))]
    
    for item in streaming_history:
        a = item['artistName']
        if a in artist_to_idx:
            t = time.strftime("%Y-%m", item['endTime'])
            if t in time_to_idx:
                matrix[artist_to_idx[a]][time_to_idx[t]] += 1.0
                
    # Normalize per artist (row-wise)
    if normalize:
        for i in range(len(matrix)):
            row_max = max(matrix[i])
            if row_max > 0:
                for j in range(len(matrix[i])):
                    matrix[i][j] = matrix[i][j] / row_max
                
    return matrix, top_artists, time_labels

def control_freak_data(streaming_history: list[History]) -> tuple[dict[str, float], tuple[str, int]]:
    """
    Analyzes Active (User initiated) vs Passive (Queue/Autoplay) listening.
    Returns ({'active': %, 'passive': %}, (most_clicked_artist, count))
    """
    active_reasons = {'clickrow', 'playbtn'}
    
    active_count = 0
    total_count = 0
    artist_clicks = defaultdict(int)
    
    for item in streaming_history:
        total_count += 1
        if item['reasonStart'] in active_reasons:
            active_count += 1
            artist_clicks[item['artistName']] += 1
            
    if total_count == 0:
        return {'active': 0.0, 'passive': 0.0}, ('None', 0)
        
    active_pct = (active_count / total_count) * 100
    passive_pct = 100 - active_pct
    
    most_clicked = sorted(artist_clicks.items(), key=lambda x: x[1], reverse=True)
    top_click = most_clicked[0] if most_clicked else ('None', 0)
    
    return {'active': active_pct, 'passive': passive_pct}, top_click


def shuffle_paradox_data(streaming_history: list[History]) -> dict[str, float]:
    """
    Compares skip rates when Shuffle is On vs Off.
    Returns {'shuffle_skip_rate': %, 'normal_skip_rate': %}
    """
    shuffle_plays = 0
    shuffle_skips = 0
    normal_plays = 0
    normal_skips = 0
    
    for item in streaming_history:
        is_shuffle = item.get('shuffle', False)
        
        if is_shuffle:
            shuffle_plays += 1
            if item['skipped']:
                shuffle_skips += 1
        else:
            normal_plays += 1
            if item['skipped']:
                normal_skips += 1
                
    shuffle_rate = (shuffle_skips / shuffle_plays * 100) if shuffle_plays > 0 else 0.0
    normal_rate = (normal_skips / normal_plays * 100) if normal_plays > 0 else 0.0
    
    return {'shuffle_skip_rate': shuffle_rate, 'normal_skip_rate': normal_rate}


def natural_death_data(streaming_history: list[History], min_plays: int = 50) -> tuple[dict[str, float], list[tuple[str, float]]]:
    """
    Analyzes how tracks end (Natural 'trackdone' vs User intervention).
    Returns ({'natural': %, 'killed': %}, top_respected_artists)
    """
    natural_ends = 0
    total_ends = 0
    
    artist_respect = defaultdict(lambda: {'finished': 0, 'total': 0})
    
    for item in streaming_history:
        total_ends += 1
        is_natural = item['reasonEnd'] == 'trackdone'
        
        if is_natural:
            natural_ends += 1
            
        artist_respect[item['artistName']]['total'] += 1
        if is_natural:
            artist_respect[item['artistName']]['finished'] += 1
            
    if total_ends == 0:
        return {'natural': 0.0, 'killed': 0.0}, []
        
    natural_pct = (natural_ends / total_ends) * 100
    killed_pct = 100 - natural_pct
    
    # Calculate respect score for artists
    respect_scores = []
    for artist, data in artist_respect.items():
        if data['total'] >= min_plays:
            score = (data['finished'] / data['total']) * 100
            respect_scores.append((artist, score))
            
    # Sort by highest respect score
    top_respected = sorted(respect_scores, key=lambda x: x[1], reverse=True)[:10]
    
    return {'natural': natural_pct, 'killed': killed_pct}, top_respected

def active_listening_heatmap_data(streaming_history: list[History]) -> list[list[int]]:
    """
    Prepares data for Active Starts (Day vs Hour) heatmap.
    Returns 7x24 matrix of active start counts.
    """
    active_reasons = {'clickrow', 'playbtn'}
    # 7 rows (Mon-Sun), 24 columns (0-23 hours)
    matrix = [[0 for _ in range(24)] for _ in range(7)]
    
    for item in streaming_history:
        if item['reasonStart'] in active_reasons:
            day = item['endTime'].tm_wday
            hour = item['endTime'].tm_hour
            matrix[day][hour] += 1
            
    return matrix


def active_listening_trend_data(streaming_history: list[History]) -> dict[int, float]:
    """
    Calculates percentage of active starts per year.
    Returns {year: active_percentage}
    """
    active_reasons = {'clickrow', 'playbtn'}
    yearly_stats = defaultdict(lambda: {'active': 0, 'total': 0})
    
    for item in streaming_history:
        year = item['endTime'].tm_year
        yearly_stats[year]['total'] += 1
        if item['reasonStart'] in active_reasons:
            yearly_stats[year]['active'] += 1
            
    trends = {}
    for year, data in yearly_stats.items():
        if data['total'] > 0:
            trends[year] = (data['active'] / data['total']) * 100
            
    return dict(sorted(trends.items()))

def get_artist_traits(streaming_history: list[History], top_n: int = 5) -> dict:
    """
    Calculates personality traits for the top N artists.
    Traits: Loyalty (1-skip), Discovery (unique/total), Night Owl (night/total), 
            Weekend Warrior (weekend/total), Active Choice (active/total).
    """
    # 1. Identify Top N Artists
    artist_counts = defaultdict(int)
    for item in streaming_history:
        artist_counts[item['artistName']] += 1
    
    top_artists = [k for k, v in sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]]
    
    # 2. Calculate Traits
    traits = defaultdict(lambda: {'plays': 0, 'skips': 0, 'unique_tracks': set(), 
                                  'night_plays': 0, 'weekend_plays': 0, 'active_starts': 0})
    
    for item in streaming_history:
        artist = item['artistName']
        if artist in top_artists:
            t = traits[artist]
            t['plays'] += 1
            if item['skipped']: t['skips'] += 1
            t['unique_tracks'].add(item['trackName'])
            
            # Night (6pm - 6am)
            if item['endTime'].tm_hour < 6 or item['endTime'].tm_hour >= 18:
                t['night_plays'] += 1
                
            # Weekend (Sat=5, Sun=6)
            if item['endTime'].tm_wday >= 5:
                t['weekend_plays'] += 1
                
            # Active Start
            if item['reasonStart'] in ['clickrow', 'playbtn', 'appload', 'remote']:
                t['active_starts'] += 1

    # 3. Normalize to 0-1 scale
    result = {}
    for artist in top_artists:
        data = traits[artist]
        total = data['plays']
        if total == 0: continue
        
        result[artist] = [
            1 - (data['skips'] / total),                # Loyalty
            len(data['unique_tracks']) / total,         # Discovery (approx)
            data['night_plays'] / total,                # Night Owl
            data['weekend_plays'] / total,              # Weekend Warrior
            data['active_starts'] / total               # Active Choice
        ]
        
    return result

def longest_played_tracks(streaming_history: list[History]) -> dict[str, timedelta]:
    """Calculates the total listening time per track."""
    result = defaultdict(timedelta)
    for item in streaming_history:
        track = f"{item['artistName']} - {item['trackName']}"
        result[track] += item['msPlayed']
    
    return {k: result[k] for k in sorted(result, key=result.get, reverse=True)}

def night_shift_artists(streaming_history: list[History]) -> dict[str, int]:
    """Top artists played between 2 AM and 5 AM."""
    counts = defaultdict(int)
    for item in streaming_history:
        if 2 <= item['endTime'].tm_hour < 5:
            counts[item['artistName']] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def new_years_transitions(streaming_history: list[History]) -> dict[int, tuple[str, str]]:
    """Returns {year: (last_song_of_year, first_song_of_next_year)}"""
    sorted_history = sorted(streaming_history, key=lambda x: x['endTime'])
    transitions = {}
    
    if not sorted_history:
        return {}

    by_year = defaultdict(list)
    for item in sorted_history:
        by_year[item['endTime'].tm_year].append(item)
    
    years = sorted(by_year.keys())
    for i in range(len(years) - 1):
        current_year = years[i]
        next_year = years[i+1]
        
        last_song = by_year[current_year][-1]
        first_song = by_year[next_year][0]
        
        last_str = f"{last_song['artistName']} - {last_song['trackName']} ({time.strftime('%Y-%m-%d %H:%M', last_song['endTime'])})"
        first_str = f"{first_song['artistName']} - {first_song['trackName']} ({time.strftime('%Y-%m-%d %H:%M', first_song['endTime'])})"
        
        transitions[current_year] = (last_str, first_str)
        
    return transitions

def consistency_king(streaming_history: list[History]) -> dict[str, int]:
    """Track played on the most unique dates."""
    track_dates = defaultdict(set)
    for item in streaming_history:
        track = f"{item['artistName']} - {item['trackName']}"
        date_str = f"{item['endTime'].tm_year}-{item['endTime'].tm_mon}-{item['endTime'].tm_mday}"
        track_dates[track].add(date_str)
    
    result = {k: len(v) for k, v in track_dates.items()}
    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

def alphabet_challenge(streaming_history: list[History]) -> dict[str, tuple[str, int]]:
    """Most played track for each letter A-Z."""
    track_counts = defaultdict(int)
    for item in streaming_history:
        track = f"{item['artistName']} - {item['trackName']}"
        track_counts[track] += 1
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    best_of_letter = {}
    
    for char in alphabet:
        candidates = {k: v for k, v in track_counts.items() if k.upper().startswith(char)}
        if candidates:
            best = max(candidates.items(), key=lambda x: x[1])
            best_of_letter[char] = best
            
    return best_of_letter

def obsession_score(streaming_history: list[History]) -> dict[str, float]:
    """
    Calculates Obsession Score: Total Plays / Unique Days Played.
    High score means many plays in few days.
    Returns dict {track_name: score}
    """
    track_stats = defaultdict(lambda: {'plays': 0, 'days': set()})
    
    for item in streaming_history:
        track = f"{item['artistName']} - {item['trackName']}"
        date_str = time.strftime('%Y-%m-%d', item['endTime'])
        track_stats[track]['plays'] += 1
        track_stats[track]['days'].add(date_str)
        
    scores = {}
    for track, stats in track_stats.items():
        if stats['plays'] > 10:  # Minimum plays to qualify
            scores[track] = stats['plays'] / len(stats['days'])
            
    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

def early_bird_artists(streaming_history: list[History]) -> dict[str, int]:
    """
    Top artists played between 5 AM and 9 AM.
    """
    counts = defaultdict(int)
    for item in streaming_history:
        hour = item['endTime'].tm_hour
        if 5 <= hour < 9:
            counts[item['artistName']] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def nine_to_five_artists(streaming_history: list[History]) -> dict[str, int]:
    """
    Top artists played Mon-Fri, 9 AM - 5 PM.
    """
    counts = defaultdict(int)
    for item in streaming_history:
        hour = item['endTime'].tm_hour
        wday = item['endTime'].tm_wday
        if 0 <= wday <= 4 and 9 <= hour < 17:
            counts[item['artistName']] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def party_animal_tracks(streaming_history: list[History]) -> dict[str, int]:
    """
    Top tracks played Fri/Sat nights (10 PM - 4 AM).
    """
    counts = defaultdict(int)
    for item in streaming_history:
        hour = item['endTime'].tm_hour
        wday = item['endTime'].tm_wday
        
        is_fri_night = (wday == 4 and hour >= 22)
        is_sat_early = (wday == 5 and hour < 4)
        is_sat_night = (wday == 5 and hour >= 22)
        is_sun_early = (wday == 6 and hour < 4)
        
        if is_fri_night or is_sat_early or is_sat_night or is_sun_early:
            track = f"{item['artistName']} - {item['trackName']}"
            counts[track] += 1
            
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def sunday_scaries_tracks(streaming_history: list[History]) -> dict[str, int]:
    """
    Top tracks played Sunday 6 PM - Midnight.
    """
    counts = defaultdict(int)
    for item in streaming_history:
        hour = item['endTime'].tm_hour
        wday = item['endTime'].tm_wday
        if wday == 6 and 18 <= hour <= 23:
            track = f"{item['artistName']} - {item['trackName']}"
            counts[track] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def unskippable_streak(streaming_history: list[History]) -> tuple[int, str, str]:
    """
    Longest sequence of songs played without skipping.
    Returns (count, start_date, end_date)
    """
    # Sort by time just in case
    sorted_history = sorted(streaming_history, key=lambda x: x['endTime'])
    
    max_streak = 0
    current_streak = 0
    streak_start = None
    best_start = None
    best_end = None
    
    for item in sorted_history:
        # Check if skipped. Note: 'skipped' might be None in some data exports, 
        # so we fallback to checking if msPlayed is reasonably long (e.g. > 30s) if skipped is missing
        was_skipped = item.get('skipped')
        if was_skipped is None:
             # Fallback logic: if played < 30s and reasonEnd is not 'trackdone'
             was_skipped = (item['msPlayed'].total_seconds() < 30 and item.get('reasonEnd') != 'trackdone')

        if not was_skipped:
            if current_streak == 0:
                streak_start = item['endTime']
            current_streak += 1
        else:
            if current_streak > max_streak:
                max_streak = current_streak
                best_start = streak_start
                best_end = item['endTime']
            current_streak = 0
            
    # Check last streak
    if current_streak > max_streak:
        max_streak = current_streak
        best_start = streak_start
        best_end = sorted_history[-1]['endTime']
        
    start_str = time.strftime('%Y-%m-%d %H:%M', best_start) if best_start else "-"
    end_str = time.strftime('%Y-%m-%d %H:%M', best_end) if best_end else "-"
    
    return max_streak, start_str, end_str

def artist_hopper(streaming_history: list[History]) -> float:
    """
    Average consecutive plays per artist switch.
    """
    sorted_history = sorted(streaming_history, key=lambda x: x['endTime'])
    if not sorted_history:
        return 0.0
        
    streaks = []
    current_streak = 0
    last_artist = None
    
    for item in sorted_history:
        artist = item['artistName']
        if artist == last_artist:
            current_streak += 1
        else:
            if current_streak > 0:
                streaks.append(current_streak)
            current_streak = 1
            last_artist = artist
            
    if current_streak > 0:
        streaks.append(current_streak)
        
    return sum(streaks) / len(streaks) if streaks else 0.0

def discovery_peak(streaming_history: list[History]) -> tuple[str, int]:
    """
    Month with most new artist discoveries.
    Returns (month_str, count)
    """
    sorted_history = sorted(streaming_history, key=lambda x: x['endTime'])
    known_artists = set()
    discoveries = defaultdict(int)
    
    for item in sorted_history:
        artist = item['artistName']
        if artist not in known_artists:
            month = time.strftime('%Y-%m', item['endTime'])
            discoveries[month] += 1
            known_artists.add(artist)
            
    if not discoveries:
        return ("-", 0)
        
    best_month = max(discoveries.items(), key=lambda x: x[1])
    return best_month

def comfort_zone(streaming_history: list[History]) -> tuple[float, list[tuple[str, timedelta]]]:
    """
    % of total time spent on Top 10 Artists.
    Returns (percentage, top_10_list)
    """
    artist_time = defaultdict(timedelta)
    total_time = timedelta()
    
    for item in streaming_history:
        artist_time[item['artistName']] += item['msPlayed']
        total_time += item['msPlayed']
        
    if total_time.total_seconds() == 0:
        return 0.0, []
        
    sorted_artists = sorted(artist_time.items(), key=lambda x: x[1], reverse=True)
    top_10 = sorted_artists[:10]
    
    top_10_time = sum((t for a, t in top_10), timedelta())
    percentage = (top_10_time.total_seconds() / total_time.total_seconds()) * 100
    
    return percentage, top_10

def single_day_record(streaming_history: list[History]) -> tuple[str, str, timedelta]:
    """
    Most time spent listening to a single artist in one day.
    Returns (artist, date_str, duration)
    """
    day_artist_time = defaultdict(timedelta)
    
    for item in streaming_history:
        date_str = time.strftime('%Y-%m-%d', item['endTime'])
        key = (date_str, item['artistName'])
        day_artist_time[key] += item['msPlayed']
        
    if not day_artist_time:
        return ("-", "-", timedelta(0))
        
    (best_date, best_artist), best_time = max(day_artist_time.items(), key=lambda x: x[1])
    
    return best_artist, best_date, best_time

def manual_laborer(streaming_history: list[History]) -> dict[str, int]:
    """
    Top tracks played by clicking (reasonStart='clickrow').
    """
    counts = defaultdict(int)
    for item in streaming_history:
        # reasonStart might vary by platform/year, but 'clickrow' is standard for manual selection
        if item.get('reasonStart') == 'clickrow':
            track = f"{item['artistName']} - {item['trackName']}"
            counts[track] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def shuffle_roulette(streaming_history: list[History]) -> dict[str, int]:
    """
    Top tracks played when Shuffle was ON.
    """
    counts = defaultdict(int)
    for item in streaming_history:
        if item.get('shuffle') is True:
            track = f"{item['artistName']} - {item['trackName']}"
            counts[track] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def _get_sessions(streaming_history: list[History], gap_minutes: int = 30) -> list[list[History]]:
    """Helper to group history into sessions."""
    sorted_history = sorted(streaming_history, key=lambda x: x['endTime'])
    sessions = []
    if not sorted_history:
        return sessions
        
    current_session = [sorted_history[0]]
    
    for i in range(1, len(sorted_history)):
        prev_end = sorted_history[i-1]['endTime']
        curr_end = sorted_history[i]['endTime']
        
        # Convert struct_time to timestamp for comparison
        prev_ts = mktime(prev_end)
        curr_ts = mktime(curr_end)
        
        # Calculate gap. Note: endTime is when the song ENDED.
        # So gap = (curr_end - curr_duration) - prev_end
        # But we only have endTime and msPlayed.
        # Start time of current = curr_end - msPlayed
        curr_duration_sec = sorted_history[i]['msPlayed'].total_seconds()
        curr_start_ts = curr_ts - curr_duration_sec
        
        if (curr_start_ts - prev_ts) > (gap_minutes * 60):
            sessions.append(current_session)
            current_session = []
            
        current_session.append(sorted_history[i])
        
    if current_session:
        sessions.append(current_session)
        
    return sessions

def session_starter(streaming_history: list[History]) -> dict[str, int]:
    """
    Track that most frequently starts a session.
    """
    sessions = _get_sessions(streaming_history)
    counts = defaultdict(int)
    for sess in sessions:
        if sess:
            item = sess[0]
            track = f"{item['artistName']} - {item['trackName']}"
            counts[track] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def session_closer(streaming_history: list[History]) -> dict[str, int]:
    """
    Track that most frequently ends a session.
    """
    sessions = _get_sessions(streaming_history)
    counts = defaultdict(int)
    for sess in sessions:
        if sess:
            item = sess[-1]
            track = f"{item['artistName']} - {item['trackName']}"
            counts[track] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def quick_fix(streaming_history: list[History]) -> int:
    """
    Count of 'Single Song Sessions'.
    """
    sessions = _get_sessions(streaming_history)
    return sum(1 for s in sessions if len(s) == 1)

def skippers_remorse(streaming_history: list[History]) -> dict[str, float]:
    """
    Tracks skipped >50% of time, but played >20 times.
    Returns {track: skip_rate}
    """
    track_stats = defaultdict(lambda: {'plays': 0, 'skips': 0})
    
    for item in streaming_history:
        track = f"{item['artistName']} - {item['trackName']}"
        track_stats[track]['plays'] += 1
        
        # Check skip logic
        was_skipped = item.get('skipped')
        if was_skipped is None:
             was_skipped = (item['msPlayed'].total_seconds() < 30 and item.get('reasonEnd') != 'trackdone')
        
        if was_skipped:
            track_stats[track]['skips'] += 1
            
    results = {}
    for track, stats in track_stats.items():
        if stats['plays'] > 20:
            rate = (stats['skips'] / stats['plays']) * 100
            if rate > 50:
                results[track] = rate
                
    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

def remix_junkie(streaming_history: list[History]) -> tuple[float, int]:
    """
    Percentage and count of tracks that are Remix/Mix/Edit.
    """
    total = len(streaming_history)
    if total == 0:
        return 0.0, 0
        
    keywords = ['remix', ' mix', ' edit', 'club', 'vip', 'dub']
    count = 0
    for item in streaming_history:
        name = item['trackName'].lower()
        if any(k in name for k in keywords):
            count += 1
            
    return (count / total) * 100, count

def live_fanatic(streaming_history: list[History]) -> tuple[float, int]:
    """
    Percentage and count of tracks that are Live/Concert.
    """
    total = len(streaming_history)
    if total == 0:
        return 0.0, 0
        
    keywords = ['live', 'concert', 'performance', 'session', 'tour']
    count = 0
    for item in streaming_history:
        # Check both track and album
        name = (item['trackName'] + " " + item['albumName']).lower()
        if any(k in name for k in keywords):
            count += 1
            
    return (count / total) * 100, count

def short_king(streaming_history: list[History]) -> dict[str, int]:
    """
    Most played tracks under 2 minutes (that were finished).
    """
    counts = defaultdict(int)
    for item in streaming_history:
        # 2 mins = 120 seconds
        if item['msPlayed'].total_seconds() < 120 and item.get('reasonEnd') == 'trackdone':
            track = f"{item['artistName']} - {item['trackName']}"
            counts[track] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def epic_saga(streaming_history: list[History]) -> dict[str, int]:
    """
    Most played tracks over 7 minutes (that were finished).
    """
    counts = defaultdict(int)
    for item in streaming_history:
        # 7 mins = 420 seconds
        if item['msPlayed'].total_seconds() > 420 and item.get('reasonEnd') == 'trackdone':
            track = f"{item['artistName']} - {item['trackName']}"
            counts[track] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def collaborator(streaming_history: list[History]) -> dict[str, int]:
    """
    Most played tracks featuring other artists.
    """
    counts = defaultdict(int)
    keywords = ['feat.', 'ft.', 'with ', 'featuring']
    for item in streaming_history:
        name = (item['trackName'] + " " + item['artistName']).lower()
        if any(k in name for k in keywords):
            track = f"{item['artistName']} - {item['trackName']}"
            counts[track] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def alphabet_artists(streaming_history: list[History]) -> dict[str, tuple[str, int]]:
    """
    Most played Artist for A-Z.
    """
    # First count all artists
    artist_counts = defaultdict(int)
    for item in streaming_history:
        artist_counts[item['artistName']] += 1
        
    # Group by letter
    letter_best = {}
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        # Filter artists starting with char
        candidates = {k: v for k, v in artist_counts.items() if k.upper().startswith(char)}
        if candidates:
            best_artist = max(candidates.items(), key=lambda x: x[1])
            letter_best[char] = best_artist
            
    return letter_best

def spelling_bee(streaming_history: list[History]) -> tuple[str, int, str, int]:
    """
    Longest Artist Name and Track Title.
    Returns (artist, len, track, len)
    """
    max_artist = ""
    max_track = ""
    
    for item in streaming_history:
        if len(item['artistName']) > len(max_artist):
            max_artist = item['artistName']
        if len(item['trackName']) > len(max_track):
            max_track = item['trackName']
            
    return max_artist, len(max_artist), max_track, len(max_track)

def same_name_game(streaming_history: list[History]) -> dict[str, int]:
    """
    Track titles listened to from the most DIFFERENT artists.
    """
    title_artists = defaultdict(set)
    
    for item in streaming_history:
        # Normalize title slightly to catch "Home" vs "Home "
        title = item['trackName'].strip()
        # Ignore generic titles like "Intro", "Untitled"
        if title.lower() in ['intro', 'untitled', 'track 1', 'outro']:
            continue
        title_artists[title].add(item['artistName'])
        
    # Count unique artists per title
    counts = {t: len(a) for t, a in title_artists.items() if len(a) > 1}
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def midnight_club(streaming_history: list[History]) -> dict[str, int]:
    """
    Top artists played between Midnight and 1 AM.
    """
    counts = defaultdict(int)
    for item in streaming_history:
        hour = item['endTime'].tm_hour
        if hour == 0:
            counts[item['artistName']] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def lunch_break(streaming_history: list[History]) -> dict[str, int]:
    """
    Top artists played between 12 PM and 2 PM.
    """
    counts = defaultdict(int)
    for item in streaming_history:
        hour = item['endTime'].tm_hour
        if 12 <= hour < 14:
            counts[item['artistName']] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def monday_blues(streaming_history: list[History]) -> dict[str, int]:
    """
    Top tracks played on Mondays.
    """
    counts = defaultdict(int)
    for item in streaming_history:
        if item['endTime'].tm_wday == 0:  # Monday is 0
            track = f"{item['artistName']} - {item['trackName']}"
            counts[track] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def hump_day_hero(streaming_history: list[History]) -> dict[str, int]:
    """
    Top tracks played on Wednesdays.
    """
    counts = defaultdict(int)
    for item in streaming_history:
        if item['endTime'].tm_wday == 2:  # Wednesday is 2
            track = f"{item['artistName']} - {item['trackName']}"
            counts[track] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def quarterly_review(streaming_history: list[History]) -> dict[int, tuple[str, int]]:
    """
    Top track for each Quarter (Q1-Q4).
    """
    q_counts = defaultdict(lambda: defaultdict(int))
    
    for item in streaming_history:
        month = item['endTime'].tm_mon
        quarter = (month - 1) // 3 + 1
        track = f"{item['artistName']} - {item['trackName']}"
        q_counts[quarter][track] += 1
        
    results = {}
    for q in range(1, 5):
        if q_counts[q]:
            best = max(q_counts[q].items(), key=lambda x: x[1])
            results[q] = best
        else:
            results[q] = ("-", 0)
            
    return results

def album_purist(streaming_history: list[History]) -> tuple[int, str, str]:
    """
    Longest streak of unique songs played from the same album in a row.
    Returns (streak_length, album_name, artist_name)
    """
    sorted_history = sorted(streaming_history, key=lambda x: x['endTime'])
    
    max_streak = 0
    best_album = "-"
    best_artist = "-"
    
    current_album = None
    current_artist = None
    current_tracks = set()
    
    for item in sorted_history:
        album = item['albumName']
        artist = item['artistName']
        track = item['trackName']
        
        # Ignore empty albums or singles (often album name is same as track name)
        if not album or album == track:
            current_album = None
            current_tracks = set()
            continue
            
        if album == current_album and artist == current_artist:
            current_tracks.add(track)
        else:
            # Check previous streak
            if len(current_tracks) > max_streak:
                max_streak = len(current_tracks)
                best_album = current_album
                best_artist = current_artist
                
            # Start new streak
            current_album = album
            current_artist = artist
            current_tracks = {track}
            
    # Check last
    if len(current_tracks) > max_streak:
        max_streak = len(current_tracks)
        best_album = current_album
        best_artist = current_artist
        
    return max_streak, best_album, best_artist

def instant_skips(streaming_history: list[History]) -> dict[str, int]:
    """
    Returns a dictionary of songs skipped in less than 1 second (1000ms).
    Key: "Artist - Track"
    Value: Count of instant skips
    """
    skips = {}
    for item in streaming_history:
        # Check if skipped and duration < 1 second
        # msPlayed is a timedelta, so we check total_seconds()
        if item['skipped'] and item['msPlayed'].total_seconds() < 1.0:
            key = f"{item['artistName']} - {item['trackName']}"
            if key not in skips:
                skips[key] = 0
            skips[key] += 1
    
    return {k: v for k, v in sorted(skips.items(), key=lambda item: item[1], reverse=True)}



def get_full_song_stats(streaming_history: list[History]) -> list[dict]:
    """
    Aggregates stats for all songs for CSV export.
    Returns a list of dicts with keys:
    Artist, Track Name, Times Played, First Played, Last Played, Skipped, Instant Skips, User Started
    """
    stats = {}
    
    for item in streaming_history:
        key = (item['artistName'], item['trackName'])
        
        if key not in stats:
            stats[key] = {
                'Artist': item['artistName'],
                'Track Name': item['trackName'],
                'Times Played': 0,
                'First Played': item['endTime'],
                'Last Played': item['endTime'],
                'Skipped': 0,
                'Instant Skips': 0,
                'User Started': 0
            }
        
        entry = stats[key]
        entry['Times Played'] += 1
        
        # Update dates
        if item['endTime'] < entry['First Played']:
            entry['First Played'] = item['endTime']
        if item['endTime'] > entry['Last Played']:
            entry['Last Played'] = item['endTime']
            
        # Update counts
        if item['skipped']:
            entry['Skipped'] += 1
            if item['msPlayed'].total_seconds() < 1.0:
                entry['Instant Skips'] += 1
            
        if item['reasonStart'] in ['clickrow', 'playbtn']:
            entry['User Started'] += 1
            
    # Format dates
    result = []
    for entry in stats.values():
        entry['First Played'] = time.strftime('%Y-%m-%d %H:%M:%S', entry['First Played'])
        entry['Last Played'] = time.strftime('%Y-%m-%d %H:%M:%S', entry['Last Played'])
        result.append(entry)
        
    return result
