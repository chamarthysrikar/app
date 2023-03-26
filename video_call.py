#Video Call Application

#Import the required packages
import streamlit as st
from streamlit_server_state import server_state, server_state_lock
from streamlit_webrtc import ClientSettings, WebRtcMode, webrtc_streamer
from streamlit_image_select import image_select

import av
import cv2

#Title
st.title("Audio Driven Talking Head Demo")

#Main Function
def main():
    if "webrtc_contexts" not in server_state:
        server_state["webrtc_contexts"] = []

    #Creates Columns
    column1,column2 =st.columns(2)

    with column1:
        #Client 1 video and audio streamer
        st.header("Client 1")
        selfStream = webrtc_streamer(
            key="self",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration={
                    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                },
            media_stream_constraints={"video": True, "audio": True},
            sendback_audio=False,
        )

        #Images for Talking head
        img = image_select(label="Choose a Talking Head", 
        images=[
        "images/obama.jpg",
        "images/hermione.jpg",
        "images/john.jpg",
        "images/dragonmom.jpg",
        ],
        captions=["Mr Obama", "Hermione", "John", "Daenerys"],
        )

    with server_state_lock["webrtc_contexts"]:
        rtc_session = server_state["webrtc_contexts"]
        if selfStream.state.playing and selfStream not in rtc_session:
            rtc_session.append(selfStream)
            server_state["webrtc_contexts"] = rtc_session
        elif not selfStream.state.playing and selfStream in rtc_session:
            rtc_session.remove(selfStream)
            server_state["webrtc_contexts"] = rtc_session

    streamActive=[]
    for stream in rtc_session:
        if stream!=selfStream and stream.state.playing:
            streamActive.append(stream)

    with column2:
        def callback(frame):
            img = frame.to_ndarray(format="bgr24")
            img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)
            return av.VideoFrame.from_ndarray(img, format="bgr24")

        #Client 2 video & audio streamer
        st.header("Client 2")
        for stream in streamActive:
            webrtc_streamer(
                key=str(id(stream)),
                mode=WebRtcMode.RECVONLY,
                rtc_configuration={
                        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                        },
                media_stream_constraints={
                        "video": True,
                        "audio": True,
                    },
                video_frame_callback=callback,
                source_audio_track=stream.output_audio_track,
                source_video_track=stream.output_video_track,
                desired_playing_state=stream.state.playing,
            )


if __name__ == "__main__":
    main()
