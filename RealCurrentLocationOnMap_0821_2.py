# 지도상 현위치 추가

import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import GoogleV3
from streamlit.components.v1 import html

# Google Geocoding API 키 설정
api_key = "AIzaSyCW-4kxARbJUxL3jmOz5dR5D-AabKhDJdc"  # 여기에 당신의 Google API 키를 입력하세요.

# 사용자 위치 입력
st.sidebar.title("현위치 입력")
location_input = st.sidebar.text_input("위치 입력 (예: 서울, 대전, New York)", "대전")

# Geopy를 사용하여 입력된 위치의 좌표를 가져오기
geolocator = GoogleV3(api_key=api_key)
location = geolocator.geocode(location_input)

# JavaScript로 사용자의 현재 위치 가져오기
def get_user_location():
    st.markdown(
        """
        <script>
        function getLocation() {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
                    document.getElementById('lat').value = latitude;
                    document.getElementById('lon').value = longitude;
                    document.getElementById('location-form').submit();
                }
            );
        }
        </script>
        """,
        unsafe_allow_html=True
    )

    html(
        """
        <form id="location-form">
            <input type="hidden" id="lat" name="lat">
            <input type="hidden" id="lon" name="lon">
            <button onclick="getLocation()">현위치(Current Location)</button>
        </form>
        """,
        height=100,
    )

# 위치 좌표 가져오기
lat = st.experimental_get_query_params().get('lat', [None])[0]
lon = st.experimental_get_query_params().get('lon', [None])[0]

if lat and lon:
    location = (float(lat), float(lon))

# Folium 지도 생성 (입력된 위치 또는 현재 위치를 중심으로 설정)
if location:
    if isinstance(location, tuple):  # 사용자가 선택한 위치가 튜플인 경우
        latitude, longitude = location
    else:
        latitude, longitude = location.latitude, location.longitude

    map_obj = folium.Map(
        location=[latitude, longitude],  # 입력된 위치 또는 현재 위치의 중심 좌표
        zoom_start=12  # 줌 레벨 설정
    )

    # 현위치 마커 추가
    folium.Marker([latitude, longitude], tooltip="Current Location").add_to(map_obj)

    # Streamlit 앱에 지도 표시
    st_folium(map_obj, width=800, height=600)
else:
    st.error("위치를 찾을 수 없습니다. 다시 입력해 주세요.")

# 사용자 위치를 가져오는 버튼 표시
get_user_location()
