import streamlit as st
from streamlit_webrtc import webrtc_streamer
from streamlit_webrtc import WebRtcMode
st.title("Audio Driven Talking demo")


col1, col2 = st.columns(2)


with col1:
    ctx=webrtc_streamer(key="sample")
with col2:
    webrtc_streamer(
            key=f"sound-{id(ctx)}",
            mode=WebRtcMode.RECVONLY,
            rtc_configuration={
                "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
            },
            media_stream_constraints={"video": True, "audio": True},
            source_video_track=ctx.input_video_track,
            desired_playing_state=ctx.state.playing,
        )

st.radio(
    "Choose a Image for Talking Head",
    ('Obama', 'Trump', 'Morgan'))

