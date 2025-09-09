from fastapi import FastAPI, HTTPException
from yt_dlp import YoutubeDL, DownloadError
import asyncio

app = FastAPI()
# channel dictionary for all channels in the LCU ATM
CHANNEL_IDS = {
    "UC7WRbUmD6W-dCP_UlDbhI4A": "LolcowTechTalk",
    "UCmxQ_3W5b9kSfpmROqGJ0rA": "LolcowLive",
    "UC2xdmM3rcLFD_iN46H8y-6w": "LolcowBalls",
    "UCUENzb0fUK-6uvLL3zD08Jw": "LolcowRewind",
    "UCBQgQPjVx4wgszEmGR5cPJg": "LolcowCafe",
    "UCOzrx6iM9qQ4lIzf7BbkuCQ": "LolcowQueens",
    "UChcQ2TIYiihd9B4H50eRVlQ": "LolcowAussy",
    "UCRh4qe6HGD10ZsyG56eUdHA": "LolcowMilkers",
    "UC9NU92OuAiSLvAarnqZEoUw": "LolcowTest",
    "UCW5AOoyYnirhluLJBpdKE9g": "LolcowDolls",
    "UCU3iQ0uiduxtArm9337dXug": "LolcowNerds",
    "UCAXmJMnzByOtsdOZKnnF8bQ": "LolcowChubby",
}
#function that checks whether or not a channel is live
def check_channel_live(channel_id):
    #live url for the channel 
    live_url = f"https://www.youtube.com/channel/{channel_id}/live"
    #makes where no video is downloaded

    class NoLogging:
        def debug(self, msg): pass
        def warning(self, msg): pass
        def error(self, msg): pass


    ydl_opts = {"quiet": True, "skip_download": True, "logger": NoLogging(),}

    
        
    try:

        with YoutubeDL(ydl_opts) as ydl:
            #grabs video info using yt_dlp
            info = ydl.extract_info(live_url, download=False)

            #if the live feed video is up it will return a status saying it's live,
            #the channel name, and the exact watch url for the video

            return {
                "is_live": info.get("is_live", False),
                "channel_name": info.get("channel") or info.get("uploader"),
                "watch_url": f"https://www.youtube.com/watch?v={info.get('id')}" if info.get("is_live", False) else None
            }
        #if it's not live, or there's an error it return None
    except (DownloadError, Exception) as e:
        print(f"⚠️ Error checking {channel_id}: {e}")
        return None

#dictionary for storing the latest livestatus of the channels
live_status_cache = {}
# function runs every minute forever unless turned off by the user 
# to update staus of the shows and whether they are up and running or offline 
# and store that info while keeping it updated every minute
async def background_live_checker():
    global live_status_cache
    while True:
        print("🔁 Checking all channels...")
        tasks = []
        for channel_id, channel_name in CHANNEL_IDS.items():
            task = asyncio.to_thread(check_channel_live, channel_id)
            tasks.append((channel_id, channel_name, task))
        results = await asyncio.gather(*(t[2] for t in tasks))


        for (channel_id, channel_name, _), status in zip(tasks, results):

            if status is not None:
                status["channel_id"] = channel_id
                status["channel_name"] = status.get("channel_name") or channel_name
                live_status_cache[channel_id] = status
                #if statement that prints out a console log
                #about whether or not a channel was online
                if status.get("is_live"):
                    print(f"✅ LIVE: {status['channel_name']}")
                    print(f"   🔗 {status['watch_url']}")
                #else statement that informms that the channel is offline
                else:
                    print(f"❌ OFFLINE: {channel_name}")
                
            
            else: 
                live_status_cache[channel_id] = None
                print(f"❌ OFFLINE: {channel_name} ({channel_id})")  # 👈 now this prints when status is None
                
            
        #after the entire channel_id list has been gone through
        #system doesn't do another check for 1 minute    
        await asyncio.sleep(60)

# asynchronus function that tells the background live checker to run in the background at start
## to start this app enter: "uvicorn main:app --reload" into your terminal ##
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_live_checker())

# function that returns the newly returned live status cache values
# so they can be accessed from a local host

##  To use this function enter: "localhost:8000/live-status/live" into the browser after starting the app##


@app.get("/live-status/live")
def get_currently_live_channels():
    return [
        {
            "channel_name": status.get("channel_name"),
            "channel_id": status.get("channel_id"),
            "watch_url": status.get("watch_url"),
        }
        for status in live_status_cache.values()
        if status and status.get("is_live")
    ]


@app.get("/live-status/all")
def get_all_channels_status():
    return {
        cid: status or {"is_live": False, "channel_name": name}
        for cid, name in CHANNEL_IDS.items()
        for status in [live_status_cache.get(cid)]
    }