import matplotlib.pyplot as plt
import numpy as np

def plot_top_items(data: dict, title: str, n: int = 10):
    """
    Plots a bar chart of the top n items from the dictionary.
    """
    top_items = list(data.items())[:n]
    labels = [item[0] for item in top_items]
    values = [item[1] for item in top_items]

    # Reverse for horizontal bar chart to have top item at the top
    labels.reverse()
    values.reverse()

    fig = plt.figure(figsize=(10, 8))
    plt.barh(labels, values, color='skyblue')
    plt.xlabel('Play Count')
    plt.title(title)
    plt.tight_layout()
    return fig

def plot_artist_trends(data: dict, title: str):
    """
    Plots a line chart for artist listening trends over years.
    """
    fig = plt.figure(figsize=(12, 8))

    # Get all unique years across all artists to set x-axis
    all_years = set()
    for year_data in data.values():
        all_years.update(year_data.keys())

    if not all_years:
        print("No data to plot.")
        return fig

    sorted_years = sorted(list(all_years))

    for artist, year_counts in data.items():
        # Fill in missing years with 0
        counts = [year_counts.get(year, 0) for year in sorted_years]
        plt.plot(sorted_years, counts, label=artist, marker='o')

    plt.xlabel('Year')
    plt.ylabel('Play Count')
    plt.title(title)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    return fig

def plot_platform_usage(data: dict, title: str):
    """
    Plots a pie chart for platform usage.
    """
    labels = list(data.keys())
    sizes = list(data.values())

    fig = plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(title)
    plt.tight_layout()
    return fig


def plot_listening_by_hour(data: dict, title: str):
    """
    Plots a bar chart for listening activity by hour of the day.
    """
    hours = list(data.keys())
    counts = list(data.values())

    fig = plt.figure(figsize=(10, 6))
    plt.bar(hours, counts, color='lightgreen')
    plt.xlabel('Hour of Day (0-23)')
    plt.ylabel('Play Count')
    plt.title(title)
    plt.xticks(hours)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    return fig

def plot_location_counts(data: dict, title: str):
    """
    Plots a bar chart for plays by location (country).
    """
    return plot_top_items(data, title, n=len(data))


def plot_longest_played_artist(data: dict, title: str, n: int = 10):
    """
    Plots a bar chart for longest played artists (in hours).
    """
    top_items = list(data.items())[:n]
    labels = [item[0] for item in top_items]
    # Convert timedelta to hours for plotting
    values = [item[1].total_seconds() / 3600 for item in top_items]

    labels.reverse()
    values.reverse()

    fig = plt.figure(figsize=(10, 8))
    plt.barh(labels, values, color='salmon')
    plt.xlabel('Hours Played')
    plt.title(title)
    plt.tight_layout()
    return fig


def plot_skipped_items(data: dict, title: str, n: int = 10):
    """
    Plots a bar chart for most skipped items.
    """
    top_items = list(data.items())[:n]
    labels = [item[0] for item in top_items]
    values = [item[1] for item in top_items]

    labels.reverse()
    values.reverse()

    fig = plt.figure(figsize=(10, 8))
    plt.barh(labels, values, color='orange')
    plt.xlabel('Skip Count')
    plt.title(title)
    plt.tight_layout()
    return fig

def plot_listening_by_day_of_week(data: dict, title: str):
    """
    Plots a bar chart for listening by day of week.
    """
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    counts = [data.get(day, 0) for day in days]

    fig = plt.figure(figsize=(10, 6))
    plt.bar(days, counts, color='mediumpurple')
    plt.xlabel('Day of Week')
    plt.ylabel('Play Count')
    plt.title(title)
    plt.tight_layout()
    return fig


def plot_discovery_rate(data: dict, title: str):
    """
    Plots a line chart for new artists discovered per month.
    """
    months = list(data.keys())
    counts = list(data.values())

    fig = plt.figure(figsize=(12, 6))
    plt.plot(months, counts, marker='o', linestyle='-', color='teal')
    plt.xlabel('Month')
    plt.ylabel('New Artists')
    plt.title(title)
    plt.xticks(rotation=45)

    # Reduce x-ticks if too many
    if len(months) > 20:
        plt.xticks(months[::int(len(months)/20)], rotation=45)

    plt.tight_layout()
    return fig


def plot_seasonal_listening(data: dict, title: str):
    """
    Plots a pie chart for seasonal listening.
    """
    labels = list(data.keys())
    sizes = list(data.values())
    colors = ['lightblue', 'lightgreen', 'gold', 'orange'] # Winter, Spring, Summer, Autumn

    fig = plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.axis('equal')
    plt.title(title)
    plt.tight_layout()
    return fig


def plot_day_night_split(data: dict, title: str):
    """
    Plots a pie chart for day vs night listening.
    """
    labels = list(data.keys())
    sizes = list(data.values())
    colors = ['gold', 'midnightblue']

    fig = plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.axis('equal')
    plt.title(title)
    plt.tight_layout()
    return fig

def plot_hourly_heatmap(data: list[list[int]], title: str):
    """
    Plots a heatmap of listening activity (Day of Week vs Hour of Day).
    """
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = [str(i) for i in range(24)]

    fig = plt.figure(figsize=(12, 6))
    plt.imshow(data, cmap='YlGnBu', aspect='auto')
    
    plt.xticks(range(len(hours)), hours)
    plt.yticks(range(len(days)), days)
    
    plt.xlabel('Hour of Day')
    plt.ylabel('Day of Week')
    plt.title(title)
    plt.colorbar(label='Play Count')
    
    plt.tight_layout()
    return fig

def plot_variety_score(data: dict, title: str):
    """
    Plots a line chart for Variety Score over years.
    """
    years = list(data.keys())
    scores = list(data.values())

    fig = plt.figure(figsize=(10, 6))
    plt.plot(years, scores, marker='o', linestyle='-', color='purple')
    plt.xlabel('Year')
    plt.ylabel('Variety Score (Unique Artists / Total Plays)')
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    return fig

def plot_calendar_heatmap(data: list[list[int]], years: list[int], months: list[str], title: str):
    """
    Plots Year vs Month heatmap.
    """
    fig = plt.figure(figsize=(10, len(years)*0.8 + 2))
    plt.imshow(data, cmap='Greens', aspect='auto')
    
    plt.xticks(range(len(months)), months)
    plt.yticks(range(len(years)), years)
    
    plt.xlabel('Month')
    plt.ylabel('Year')
    plt.title(title)
    plt.colorbar(label='Play Count')
    
    plt.tight_layout()
    return fig


def plot_picky_grid(data: list[list[float]], title: str):
    """
    Plots Day vs Hour Skip Rate heatmap.
    """
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = [str(i) for i in range(24)]

    fig = plt.figure(figsize=(12, 6))
    plt.imshow(data, cmap='Reds', aspect='auto')
    
    plt.xticks(range(len(hours)), hours)
    plt.yticks(range(len(days)), days)
    
    plt.xlabel('Hour of Day')
    plt.ylabel('Day of Week')
    plt.title(title)
    plt.colorbar(label='Skip Rate %')
    
    plt.tight_layout()
    return fig


def plot_device_habits(data: list[list[int]], platforms: list[str], title: str):
    """
    Plots Platform vs Hour heatmap.
    """
    hours = [str(i) for i in range(24)]

    fig = plt.figure(figsize=(12, len(platforms)*0.8 + 2))
    plt.imshow(data, cmap='Blues', aspect='auto')
    
    plt.xticks(range(len(hours)), hours)
    plt.yticks(range(len(platforms)), platforms)
    
    plt.xlabel('Hour of Day')
    plt.ylabel('Platform')
    plt.title(title)
    plt.colorbar(label='Play Count')
    
    plt.tight_layout()
    return fig


def plot_artist_eras(data: list[list[float]], artists: list[str], time_labels: list[str], title: str):
    """
    Plots Top Artists vs Time (Eras) heatmap.
    """
    # Dynamic height: 0.25 inches per artist, min 6, max 30 (to fit screen better)
    height = max(6, min(30, len(artists) * 0.25))
    fig = plt.figure(figsize=(14, height))
    
    plt.imshow(data, cmap='magma', aspect='auto', interpolation='nearest')
    
    # Reduce x-ticks
    step = max(1, len(time_labels) // 20)
    plt.xticks(range(0, len(time_labels), step), [time_labels[i] for i in range(0, len(time_labels), step)], rotation=45)
    
    # Smaller font for y-ticks if many artists
    fontsize = 10 if len(artists) < 30 else 6
    plt.yticks(range(len(artists)), artists, fontsize=fontsize)
    
    plt.xlabel('Time')
    plt.ylabel('Artist')
    plt.title(title)
    plt.colorbar(label='Relative Listening Intensity (Normalized per Artist)')
    
    plt.tight_layout()
    return fig

def plot_active_heatmap(data: list[list[int]], title: str):
    """
    Plots Active Starts (Day vs Hour) heatmap.
    """
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = [str(i) for i in range(24)]

    fig = plt.figure(figsize=(12, 6))
    plt.imshow(data, cmap='Greens', aspect='auto')
    
    plt.xticks(range(len(hours)), hours)
    plt.yticks(range(len(days)), days)
    
    plt.xlabel('Hour of Day')
    plt.ylabel('Day of Week')
    plt.title(title)
    plt.colorbar(label='Active Starts (Clicks)')
    
    plt.tight_layout()
    return fig


def plot_active_trend(data: dict[int, float], title: str):
    """
    Plots Active Listening % trend over years.
    """
    years = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 6))
    plt.plot(years, values, marker='o', linestyle='-', color='forestgreen', linewidth=2)
    
    plt.xlabel('Year')
    plt.ylabel('Active Listening %')
    plt.title(title)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    return fig

def plot_artist_radar(data: dict, title: str):
    """
    Plots a radar chart comparing artist traits.
    """
    labels = ['Loyalty', 'Discovery', 'Night Owl', 'Weekend', 'Active Choice']
    num_vars = len(labels)
    
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1] # Close the loop
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    colors = ['#FF5733', '#33FF57', '#3357FF', '#F333FF', '#FF33A8']
    
    for i, (artist, stats) in enumerate(data.items()):
        values = list(stats)
        values += values[:1] # Close the loop
        ax.plot(angles, values, linewidth=2, label=artist, color=colors[i % len(colors)])
        ax.fill(angles, values, alpha=0.1, color=colors[i % len(colors)])
        
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    
    ax.set_title(title, y=1.1)
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
    
    return fig

def create_text_pages(text: str, lines_per_page: int = 60):
    """
    Converts a long string of text into a list of matplotlib figures,
    each representing a page of text.
    """
    lines = text.split('\n')
    pages = []
    
    for i in range(0, len(lines), lines_per_page):
        chunk = lines[i:i + lines_per_page]
        page_text = '\n'.join(chunk)
        
        fig = plt.figure(figsize=(8.27, 11.69)) # A4 size
        plt.axis('off')
        # Use a monospace font to preserve alignment
        plt.text(0.05, 0.95, page_text, transform=fig.transFigure, 
                 fontsize=8, family='monospace', verticalalignment='top')
        pages.append(fig)
        
    return pages

def plot_longest_played_tracks(data: dict, title: str, n: int = 10):
    """
    Plots a bar chart for longest played tracks (in hours).
    """
    top_items = list(data.items())[:n]
    labels = [item[0] for item in top_items]
    values = [item[1].total_seconds() / 3600 for item in top_items]

    labels.reverse()
    values.reverse()

    fig = plt.figure(figsize=(10, 8))
    plt.barh(labels, values, color='mediumpurple')
    plt.xlabel('Hours Played')
    plt.title(title)
    plt.tight_layout()
    return fig

def plot_comfort_zone(percentage: float, title: str):
    """
    Plots a pie chart showing the Comfort Zone percentage.
    """
    labels = ['Top 10 Artists', 'Others']
    sizes = [percentage, 100 - percentage]
    colors = ['#1DB954', '#191414']  # Spotify Green and Black
    explode = (0.1, 0)  # explode the 1st slice

    fig = plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(title)
    plt.tight_layout()
    return fig
