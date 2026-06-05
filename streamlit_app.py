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
    /* 슬라이더 높이 1.5배 증가 */
    [data-testid="stSlider"] input[type="range"] {
        height: 15px !important;
        width: 100% !important;
    }
    [data-testid="stSlider"] input[type="range"]::-webkit-slider-thumb {
        width: 30px !important;
        height: 30px !important;
    }
    [data-testid="stSlider"] input[type="range"]::-moz-range-thumb {
        width: 30px !important;
        height: 30px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title('단위원을 통해 알아보는 sin함수와 cos함수')

# 라디안을 π 형태의 문자열로 변환하는 함수
def format_radian_label(rad):
    """라디안을 가능한 한 π 형태로 표시"""
    special_angles = {
        0.0: '0',
        math.pi / 2: 'π/2',
        math.pi: 'π',
        3 * math.pi / 2: '3π/2',
        2 * math.pi: '2π',
    }
    for value, label in special_angles.items():
        if abs(rad - value) < 1e-3:
            return label

    pi_ratio = rad / math.pi
    
    # 자주 쓰이는 π 분수 형태를 먼저 찾는다
    for denom in [1, 2, 3, 4, 5, 6, 8, 12, 16, 24, 36]:
        numer = round(pi_ratio * denom)
        if abs(pi_ratio - numer / denom) < 1e-3:
            if numer == 0:
                return "0"
            if denom == 1:
                return "π" if numer == 1 else f"{numer}π"
            if numer == 1:
                return f"π/{denom}"
            return f"{numer}π/{denom}"
    
    return f"{rad:.2f}"

angles = [i * math.pi / 180 for i in range(0, 361)]
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
    label_placeholder.markdown(
        "<div style='display:flex; align-items:center; height:100%;'><h3 style='margin:0; transform: translateY(16px); font-size:28px;'>θ</h3></div>",
        unsafe_allow_html=True
    )

    # 슬라이더 위/아래 눈금 추가
    tick_labels = ['0', 'π/2=1.57', 'π=3.14', '3π/2=4.71', '2π=6.28']
    tick_positions = [9, 33, 55, 77, 102]  # 백분율 위치

    def render_slider_ticks():
        tick_html = '<div style="position:relative; width:100%; font-size:18px; color:#666; height:30px;">'
        for label, pos in zip(tick_labels, tick_positions):
            tick_html += f'<span style="position:absolute; left:{pos}%; transform:translateX(-50%);">{label}</span>'
        tick_html += '</div>'
        return tick_html

    st.markdown(render_slider_ticks(), unsafe_allow_html=True)
    with slider_col:
        angle_rad = st.slider('', min_value=0.0, max_value=2 * math.pi, value=math.pi/4, step=math.pi/180)

    # 현재 θ 값 표시
    current_theta = format_radian_label(angle_rad)
    st.markdown(
        f"<p style='text-align:center; font-size:24px; margin-top:12px; color:red;'><strong>θ = {current_theta}</strong></p>",
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
    'angle_normalized': [angle / math.pi for angle in angles * 2],
    'angle_label': [format_radian_label(angle) for angle in angles * 2],
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
    
    # 호(arc) 데이터: 단위원 데이터에서 0~angle_rad 범위의 점들을 필터링
    arc_data = unit_circle[unit_circle['angle'] <= angle_rad].copy()
    arc_chart = alt.Chart(arc_data).mark_line(color='red', strokeWidth=5).encode(
        x='x:Q',
        y='y:Q',
    )
    
    selected_point_chart = alt.Chart(selected_point).mark_circle(color='red', size=140).encode(
        x='x:Q',
        y='y:Q',
    )

    # SVG fallback (responsive)
    # 호의 끝점 계산
    arc_end_x = 325 + math.cos(angle_rad) * 200
    arc_end_y = 325 - math.sin(angle_rad) * 200
    # large-arc-flag: 각도가 π보다 크면 1, 아니면 0
    large_arc_flag = 1 if angle_rad > math.pi else 0
    
    svg = f"""
    <div style="max-width:100%;">
    <svg width="100%" height="auto" viewBox="0 0 650 650" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="white" />
      <line x1="0" y1="325" x2="650" y2="325" stroke="gray" stroke-width="1" />
      <line x1="325" y1="0" x2="325" y2="650" stroke="gray" stroke-width="1" />
      <circle cx="325" cy="325" r="200" stroke="black" stroke-width="3" fill="none" />
      <!-- 호 (0에서 현재 각도까지) -->
      <path d="M 525 325 A 200 200 0 {large_arc_flag} 1 {arc_end_x:.2f} {arc_end_y:.2f}" stroke="red" stroke-width="3" fill="none" />
      <!-- 선택점 -->
      <circle cx="{325 + math.cos(angle_rad)*200:.2f}" cy="{325 - math.sin(angle_rad)*200:.2f}" r="8" fill="red" />
    </svg>
    </div>
    """

    st.markdown(svg, unsafe_allow_html=True)

    st.altair_chart(
        alt.layer(x_axis, y_axis, circle_chart, radius_line_chart, selected_point_chart, arc_chart).resolve_scale(x='shared', y='shared'),
        use_container_width=True,
    )

with col2:
    st.subheader('sin함수와 cos함수')

    line_chart = alt.Chart(trig_data).mark_line().encode(
        x=alt.X(
            'angle_normalized:Q',
            title='θ',
            axis=alt.Axis(
                values=[0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2],
                labelExpr=(
                    "datum.value == 0 ? '0' : "
                    "datum.value == 0.25 ? 'π/4' : "
                    "datum.value == 0.5 ? 'π/2' : "
                    "datum.value == 0.75 ? '3π/4' : "
                    "datum.value == 1 ? 'π' : "
                    "datum.value == 1.25 ? '5π/4' : "
                    "datum.value == 1.5 ? '3π/2' : "
                    "datum.value == 1.75 ? '7π/4' : "
                    "datum.value == 2 ? '2π' : datum.value"
                ),
            )
        ),
        y=alt.Y('value:Q', title='값'),
        color=alt.Color('function:N', title='함수'),
        tooltip=['angle_label:N', 'value:Q', 'function:N']
    ).properties(width=1200, height=550)

    st.altair_chart(line_chart, use_container_width=True)
