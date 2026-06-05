import math
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title='단위원을 통해 알아보는 sin함수와 cos함수',
    page_icon=':abcd:',
    layout='wide'
)

st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 90% !important;
        width: 90% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    .css-1d391kg .main .block-container {
        max-width: 90% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title('단위원을 통해 알아보는 sin함수와 cos함수')

angles = [math.radians(deg) for deg in range(0, 361)]
unit_circle = pd.DataFrame({
    'angle': angles,
    'x': [math.cos(angle) for angle in angles],
    'y': [math.sin(angle) for angle in angles],
})

# 호도법(라디안) 슬라이더를 페이지 너비 중앙에 배치하고 θ를 슬라이더 바로 옆에 표시
outer_left, outer_center, outer_right = st.columns([1, 2, 1])
with outer_center:
    label_col, slider_col = st.columns([0.08, 0.92])
    label_placeholder = label_col.empty()
    with slider_col:
        angle_rad = st.slider('', min_value=0.0, max_value=2 * math.pi, value=math.pi/4, step=0.01)
    label_placeholder.markdown(
        "<div style='display:flex; align-items:center; height:100%;'><h3 style='margin:0;'>θ</h3></div>",
        unsafe_allow_html=True
    )

angle_deg = math.degrees(angle_rad)
selected_point = pd.DataFrame({
    'x': [math.cos(angle_rad)],
    'y': [math.sin(angle_rad)],
})
radius_line = pd.DataFrame({
    'x': [0, math.cos(angle_rad)],
    'y': [0, math.sin(angle_rad)],
})

trig_data = pd.DataFrame({
    'angle': angles * 2,
    'value': [math.sin(angle) for angle in angles] + [math.cos(angle) for angle in angles],
    'function': ['sin함수'] * len(angles) + ['cos함수'] * len(angles),
})

col1, col2 = st.columns([1.15, 1.85], gap='large')

with col1:
    st.subheader('단위원(unit circle)')

    x_axis = alt.Chart(pd.DataFrame({'x': [-1.5, 1.5], 'y': [0, 0]})).mark_rule(color='gray', size=1)
    y_axis = alt.Chart(pd.DataFrame({'x': [0, 0], 'y': [-1.5, 1.5]})).mark_rule(color='gray', size=1)
    
    circle_chart = alt.Chart(unit_circle).mark_line(color='black', strokeWidth=3, interpolate='linear').encode(
        x=alt.X('x:Q', scale=alt.Scale(domain=[-1.5, 1.5], nice=False), axis=alt.Axis(title='x')),
        y=alt.Y('y:Q', scale=alt.Scale(domain=[-1.5, 1.5], nice=False), axis=alt.Axis(title='y')),
        order=alt.Order('angle:Q'),
    ).properties(height=450)

    radius_line_chart = alt.Chart(radius_line).mark_line(color='gray', strokeDash=[5, 5], strokeWidth=2).encode(
        x='x:Q',
        y='y:Q',
    )
    selected_point_chart = alt.Chart(selected_point).mark_circle(color='red', size=140).encode(
        x='x:Q',
        y='y:Q',
    )

    # SVG fallback (responsive)
    svg = f"""
    <div style="max-width:100%;">
    <svg width="100%" height="auto" viewBox="0 0 650 650" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="white" />
      <line x1="0" y1="325" x2="650" y2="325" stroke="gray" stroke-width="1" />
      <line x1="325" y1="0" x2="325" y2="650" stroke="gray" stroke-width="1" />
      <circle cx="325" cy="325" r="200" stroke="black" stroke-width="3" fill="none" />
      <!-- 선택점 -->
      <circle cx="{325 + math.cos(angle_rad)*200:.2f}" cy="{325 - math.sin(angle_rad)*200:.2f}" r="8" fill="red" />
    </svg>
    </div>
    """

    st.markdown(svg, unsafe_allow_html=True)

    st.altair_chart(
        alt.layer(x_axis, y_axis, circle_chart, radius_line_chart, selected_point_chart).resolve_scale(x='shared', y='shared'),
        use_container_width=True,
    )

with col2:
    st.subheader('sin함수와 cos함수')

    line_chart = alt.Chart(trig_data).mark_line().encode(
        x=alt.X('angle:Q', title='각도 (rad)'),
        y=alt.Y('value:Q', title='값'),
        color=alt.Color('function:N', title='함수'),
    ).properties(width=1200, height=550)

    st.altair_chart(line_chart, use_container_width=True)
