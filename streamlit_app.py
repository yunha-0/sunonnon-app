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
    'x': [math.cos(angle) for angle in angles],
    'y': [math.sin(angle) for angle in angles],
    'order': list(range(len(angles))),
})

angle_deg = st.slider('특정 각도 선택', 0, 360, 45)
angle_rad = math.radians(angle_deg)
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
    'function': ['sin'] * len(angles) + ['cos'] * len(angles),
})

col1, col2 = st.columns([1, 2], gap='large')

with col1:
    st.subheader('단위원(unit circle)')
    st.write('단위원은 반지름이 1인 원입니다.')
    st.write(f'선택한 각도: {angle_deg}°  |  cos: {math.cos(angle_rad):.3f}  |  sin: {math.sin(angle_rad):.3f}')

    circle_chart = alt.Chart(unit_circle).mark_line(color='black', strokeWidth=2, interpolate='linear').encode(
        x=alt.X('x:Q', scale=alt.Scale(domain=[-1.5, 1.5]), axis=alt.Axis(title='x')),
        y=alt.Y('y:Q', scale=alt.Scale(domain=[-1.5, 1.5]), axis=alt.Axis(title='y')),
        order='order:Q',
    ).properties(width=650, height=650)

    circle_points_chart = alt.Chart(unit_circle).mark_circle(color='black', size=30).encode(
        x='x:Q',
        y='y:Q',
    )

    x_axis = alt.Chart(pd.DataFrame({'x': [-1.5, 1.5], 'y': [0, 0]})).mark_rule(color='gray')
    y_axis = alt.Chart(pd.DataFrame({'x': [0, 0], 'y': [-1.5, 1.5]})).mark_rule(color='gray')
    radius_line_chart = alt.Chart(radius_line).mark_line(color='gray', strokeDash=[5, 5], strokeWidth=2).encode(
        x='x:Q',
        y='y:Q',
    )
    selected_point_chart = alt.Chart(selected_point).mark_circle(color='red', size=140).encode(
        x='x:Q',
        y='y:Q',
    )

    st.altair_chart(
        alt.layer(circle_chart, circle_points_chart, x_axis, y_axis, radius_line_chart, selected_point_chart)
           .resolve_scale(x='shared', y='shared'),
        use_container_width=True,
    )

with col2:
    st.subheader('사인함수와 코사인함수')

    line_chart = alt.Chart(trig_data).mark_line().encode(
        x=alt.X('angle:Q', title='각도 (rad)'),
        y=alt.Y('value:Q', title='값'),
        color=alt.Color('function:N', title='함수'),
    ).properties(width=1200, height=550)

    st.altair_chart(line_chart, use_container_width=True)
