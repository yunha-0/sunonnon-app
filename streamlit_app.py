import math
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title='단위원을 통해 알아보는 sin함수와 cos함수',
    page_icon=':abcd:'
)

st.title('단위원을 통해 알아보는 sin함수와 cos함수')
st.write('단위원은 반지름이 1인 원입니다. 왼쪽에는 x축과 y축과 원을, 오른쪽에는 더 넓은 영역의 사인/코사인 그래프를 표시합니다.')

angles = [math.radians(deg) for deg in range(0, 361)]
unit_circle = pd.DataFrame({
    'x': [math.cos(angle) for angle in angles],
    'y': [math.sin(angle) for angle in angles],
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

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader('단위원(unit circle)')
    st.write('단위원은 반지름이 1인 원입니다.')
    st.write(f'선택한 각도: {angle_deg}°  |  cos: {math.cos(angle_rad):.3f}  |  sin: {math.sin(angle_rad):.3f}')

    circle_chart = alt.Chart(unit_circle).mark_line(color='black').encode(
        x=alt.X('x:Q', scale=alt.Scale(domain=[-1.3, 1.3]), axis=alt.Axis(title='x')),
        y=alt.Y('y:Q', scale=alt.Scale(domain=[-1.3, 1.3]), axis=alt.Axis(title='y')),
    ).properties(width=450, height=450)

    x_axis = alt.Chart(pd.DataFrame({'x': [-1.2, 1.2], 'y': [0, 0]})).mark_rule(color='gray')
    y_axis = alt.Chart(pd.DataFrame({'x': [0, 0], 'y': [-1.2, 1.2]})).mark_rule(color='gray')
    radius_line_chart = alt.Chart(radius_line).mark_line(color='gray', strokeDash=[5, 5]).encode(
        x='x:Q',
        y='y:Q',
    )
    selected_point_chart = alt.Chart(selected_point).mark_circle(color='red', size=120).encode(
        x='x:Q',
        y='y:Q',
    )

    st.altair_chart(alt.layer(circle_chart, x_axis, y_axis, radius_line_chart, selected_point_chart), use_container_width=True)

with col2:
    st.subheader('사인함수와 코사인함수')

    line_chart = alt.Chart(trig_data).mark_line().encode(
        x=alt.X('angle:Q', title='각도 (rad)'),
        y=alt.Y('value:Q', title='값'),
        color=alt.Color('function:N', title='함수'),
    ).properties(width=900, height=450)

    st.altair_chart(line_chart, use_container_width=True)
