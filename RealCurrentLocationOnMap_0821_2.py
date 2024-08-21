#주소검색을 통해 지도 이동

import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import GoogleV3

# Google Geocoding API 키 설정
api_key = "AIzaSyCW-4kxARbJUxL3jmOz5dR5D-AabKhDJdc"  # 여기에 당신의 Google API 키를 입력하세요.

# 사용자 위치 입력
st.sidebar.title("현위치 입력")
location_input = st.sidebar.text_input("위치 입력 (예: 서울, 대전, New York)", "대전")

# Geopy를 사용하여 입력된 위치의 좌표를 가져오기
geolocator = GoogleV3(api_key=api_key)
location = geolocator.geocode(location_input)

# Folium 지도 생성 (입력된 위치를 중심으로 설정)
if location:
    map_obj = folium.Map(
        location=[location.latitude, location.longitude],  # 입력된 위치의 중심 좌표
        zoom_start=12  # 줌 레벨 설정
    )

    # 현위치 마커 추가
    folium.Marker([location.latitude, location.longitude], tooltip="Current Location").add_to(map_obj)

    # Streamlit 앱에 지도 표시
    st_folium(map_obj, width=800, height=600)
else:
    st.error("위치를 찾을 수 없습니다. 다시 입력해 주세요.")
