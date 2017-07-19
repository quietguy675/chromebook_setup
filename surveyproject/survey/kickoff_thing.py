from vlc_threaded import VLC_Thread

thing = VLC_Thread()
print("Length (min):", thing.stage_media_and_get_time_left(media='/media/sd_card/media/WallE.m4v', position=0.99))
thing.start_vlc()
print("Done")
